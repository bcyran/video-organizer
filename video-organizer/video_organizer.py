#!/usr/bin/env python
# Video Organizer | GPL v2.0 | https://github.com/sajran/video-organizer

import os
import re
import argparse
import shutil
from config import *


# Video class (movie or series episode)
class Video:

    def __init__(self, filename):
        self.filename = filename
        self.new_filename = None
        self.type = None
        self.title = None
        self.episode = None
        self.season = None
        self.series = None
        self.year = None


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


# Check if the filename is correct
def validate(name):
    for regex in correct_re:
        if re.search(regex, name, re.I) is not None:
            return True
    return False


# Copy file
def copy(video, root, args):
    s_dir = args.s_dir
    m_dir = args.m_dir
    path = os.path.join(root, video.filename)

    # If file is series episode
    if video.type == 'series' and s_dir:
        season_name = 'S' + str(video.season).zfill(2)
        new_dir = os.path.join(s_dir, video.series, season_name)
        new_path = os.path.join(new_dir, video.new_filename)
    # If file is movie
    elif video.type == 'movie' and m_dir:
        name = video.title + ' (' + str(video.year) + ')'
        new_dir = os.path.join(m_dir, name)
        new_path = os.path.join(new_dir, video.new_filename)
    else:
        return

    # If new directory doesn't exist create it
    try:
        os.makedirs(new_dir, exist_ok=True)
    except OSError:
        return False

    # Copy file or move if it's enabled
    if args.move:
        shutil.move(path, new_path)
    else:
        shutil.copy2(path, new_path)
    return new_path


# Generate new filename
def generate_filename(video):
    ext = os.path.splitext(video.filename)[1]

    # If video is series episode
    if video.type == 'series':
        new_filename = '{0} S{1:02d}E{2:02d}{3}'\
            .format(video.series, video.season, video.episode, ext)
    # If video is movie
    else:
        new_filename = '{0} ({1}){2}'\
            .format(video.title, video.year, ext)
    video.new_filename = new_filename


# Rename file
def rename(video, root):
    path = os.path.join(root, video.filename)
    new_path = os.path.join(root, video.new_filename)
    try:
        os.rename(path, new_path)
    except OSError:
        return False
    return True


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
        return True

    # Extract movie title, year
    elif video.type == 'movie':
        for regex in movie_re:
            matches = re.match(regex, video.filename, re.I)
            if matches is not None:
                matches = matches.groupdict()
                break

        video.title = cleanup(matches['title'])
        video.year = int(matches['year'])
        return True

    # If there is no series-specific or movie-specific expressions in filename
    else:
        return False


# Find files, send to parser and rename
def scan(dir, args):
    # If cache is enabled this will be overwritten
    cache = False
    # Iterate through files in given directory
    files = os.listdir(dir)
    for root, subs, files in os.walk(dir):

        # If cache is enabled sort files in alphabetical order
        if args.cache:
            files.sort()

        for file in files:
            video = Video(file)

            name, ext = os.path.splitext(video.filename)

            # If filename is correct, skip to next file
            if validate(name):
                print('Skipped: {0}'.format(video.filename))
                continue

            # If current name is cached
            if cache and os.path.splitext(cache.filename)[0] == name:
                video.new_filename = os.path.splitext(cache.new_filename)[0] + ext
                video.type = cache.type
                video.title = cache.title
                video.episode = cache.episode
                video.season = cache.season
                video.series = cache.series
                video.year = cache.year
            # If it's not
            else:
                # If parsing was successful generate new name
                if parse_filename(video):
                    generate_filename(video)
                # If not, show info and skip to next file
                else:
                    print(' Failed: {0}'.format(file))
                    continue

            # If video type is ignored skip to next file
            if args.ignore == video.type:
                continue

            # If copying is enabled copy file
            if (args.s_dir and video.type == 'series') or\
               (args.m_dir and video.type == 'movie'):
                new_path = copy(video, root, args)
                if new_path:
                    print('Renamed: {0}'.format(video.filename))
                    print('     to: {0}'.format(video.new_filename))
                    if args.move:
                        print('  Moved: {0}'.format(new_path))
                    else:
                        print(' Copied: {0}'.format(new_path))
            # Rename file if copying is disabled
            else:
                if rename(video, root):
                    print('Renamed: {0}'.format(video.filename))
                    print('     to: {0}'.format(video.new_filename))

            # If cache is enabled save new name
            if args.cache:
                cache = video


# Main
def main():
    # Init argument parser
    parser = argparse.ArgumentParser()

    # Path argument
    parser.add_argument('path',
                        nargs='?',
                        default=os.getcwd(),
                        help='path to directory with video files to rename')
    # Cache argument
    parser.add_argument('-c',
                        '--cache',
                        action='store_true',
                        help='use this option if your filenames are repeating \
                        (e.g. subtitles)')
    # Copy series
    parser.add_argument('-cs',
                        '--copy-series',
                        dest='s_dir',
                        metavar='directory',
                        help='copy series episodes to given directory; when using this \
                        option files in original directory will NOT be renamed')
    # Copy movies
    parser.add_argument('-cm',
                        '--copy-movies',
                        dest='m_dir',
                        metavar='directory',
                        help='copy movies to given directory; when using this \
                        option files in original directory will NOT be renamed')
    # Move instead of copying
    parser.add_argument('-m',
                        '--move',
                        action='store_true',
                        help='move videos instead of copying')
    # Ignore one type of files
    parser.add_argument('-i',
                        '--ignore',
                        metavar='type',
                        help='ignore one type of videos (series/movies')

    args = parser.parse_args()

    # Run scan in given path
    scan(args.path, args)


if __name__ == '__main__':
    main()
