#!/usr/bin/env python

# Regular expressions specific for TV series
series_re = [
    # S04E16
    '(?P<series>.*?)S(?P<season>\d{1,2})E(?P<episode>\d{1,2})',
    # 4x16
    '(?P<series>.*?)(?P<season>\d{1,2})x(?P<episode>\d{1,2})',
    # word 'season'
    '(?P<series>.*?)season[\.\_\- ]?(?P<season>\d{1,2})',
    # word 'episode'
    '(?P<series>.*?)episode[\.\_\- ]?(?P<episode>\d{1,2})'
]

# Regular expressions for movies
movie_re = [
    # dates (four digits starting with '19' or '20' in parenthesis)
    '(?P<title>.*?)\((?P<year>(19|20)\d{2})\)',
    # four digits without parenthesis between any non-digit characters
    '(?P<title>.*?)\D(?P<year>(19|20)\d{2})\D'
]

# Regular expressions to remove during parsing
exclude_re = [
    '[\[\(\{<].*?[\]\)\}>]',
    '480p',
    '720p',
    '1080p',
    'BrRip',
    'DVDRip',
    'XViD',
    'HDTV',
    'x264'
]

# Correct filenames
correct_re = [
    # Show S01E01
    '^(?!.*[\[\]\{\}\\<>]).*? S\d{1,2}E\d{1,2}',
    # Show S01E01 - Title
    '^(?!.*[\[\]\{\}\\<>]).*? S\d{1,2}E\d{1,2} - .*',
    # Movie (2015)
    '^(?!.*[\[\]\{\}\\<>]).*? \((19|20)\d{2}\)'
]
