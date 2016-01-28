# Video Organizer
Python script that changes names of video files (series and movies) to more readable.

This script is __not finished__ but last time I checked it worked fine.

## Usage
```
usage: video_organizer.py [-h] [-i type] [-cs directory] [-cm directory] [-m]
                          [-s] [-c]
                          [path]

positional arguments:
  path                  path to directory with video files to rename

optional arguments:
  -h, --help            show this help message and exit
  -i type, --ignore type
                        ignore one type of videos (series/movies
  -cs directory, --copy-series directory
                        copy series episodes to given directory; when using
                        this option files in original directory will NOT be
                        renamed
  -cm directory, --copy-movies directory
                        copy movies to given directory; when using this option
                        files in original directory will NOT be renamed
  -m, --move            move videos instead of copying
  -s, --stats           count how many files of each type you have in your
                        library
  -c, --cache           use this option if your filenames are repeating (e.g.
                        subtitles)
```
