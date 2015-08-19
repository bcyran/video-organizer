#!/usr/bin/env python
# Video Organizer | GPL v2.0 | https://github.com/sajran/video-organizer

import os
import re
import argparse
from config import *


# Video class (movie or series episode)
class Video:

    def __init__(self, filename):
        self.filename = filename
        self.type = None
        self.title = None
        self.episode = None
        self.season = None
        self.series = None
        self.year = None
        self.id = None


# Cleanup string
def cleanup(string):
    # Remove unnecessary things from series name
    for regex in exclude_re:
        string = re.sub(regex, '', string, re.I)

    # Replace dots, underscores and dashes with spaces
    string = re.sub('[\.\_\-]', ' ', string)

    # Remove whitespaces from left and right side of string
    string = string.strip()

    return string


# Parse filenames
def parse_filename(video):
    # Search series-specific expressions in filename
    for regex in series_re:
        if re.search(regex, video.filename, re.I) is not None:
            video.type = 'series'
            break

    # Search movie-specific expressions in filename
    if video.type is None:
        for regex in movie_re:
            if re.search(regex, video.filename, re.I) is not None:
                video.type = 'movie'
                break

    # Extract series, season, episode
    if video.type == 'series':
        for regex in series_re:
            matches = re.match(regex, video.filename, re.I)
            if matches is not None:
                matches = matches.groupdict()
                break

        video.series = cleanup(matches['series'])
        video.season = int(matches['season'])
        video.episode = int(matches['episode'])

    # Extract movie title, year
    elif video.type == 'movie':
        for regex in movie_re:
            matches = re.match(regex, video.filename, re.I)
            if matches is not None:
                matches = matches.groupdict()
                break

        video.title = cleanup(matches['title'])
        video.year = int(matches['year'])

    # If there is no series-specific or movie-specific expressions in filename
    else:
        return False


# Iterate through files
def scan(dir):
    files = os.listdir(dir)
    for root, subs, files in os.walk(dir):
        for file in files:
            name, ext = os.path.splitext(file)
            video = Video(name)

            if parse_filename(video) != False:
                if video.type == 'series':
                    new_name = '{0} S{1:02d}E{2:02d}{3}'\
                        .format(video.series, video.season, video.episode, ext)
                else:
                    new_name = '{0} ({1}){2}'\
                        .format(video.title, video.year, ext)

                os.rename(os.path.join(root, file), os.path.join(root, new_name))
                print('Renamed: {0}'.format(file))
                print('to: {0}'.format(new_name).rjust(len(new_name) + 9))
            else:
                print('Failed to rename: {0}'.format(file))


# Main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        nargs='?',
                        default=os.getcwd(),
                        help='Path to directory with video files to rename')
    parser.add_argument('')
    args = parser.parse_args()

    scan(args.path)


if __name__ == '__main__':
    main()
