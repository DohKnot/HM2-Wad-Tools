# HM2 Wad Tools
These are some python scripts that parse and extract things from Hotline Miami 2: Wrong Number's wad files.
> Written for python 3.7.4 and greater

## Overview:
- [**How to use the scripts**](#How-to-use)
  - wad_extract.py
  - meta_extract.py
- [**.wad Documentation**](#.wad-Files)
  - general structure
  - how to parse
- [**.meta Documentation**](#.meta-Files)
  - general structure
  - how to parse

## How to use

You can download the all files with the `clone or download` button

### wad_extract.py

This script is for extracting assets from a .wad file. You can supply specific files to extract or just do a general grab of all assets. You can also pass in a .patchwad file since they have the same format!

### meta_extract.py

TODO

### Note: All integers are in little endian form

## .wad Files

### How .wad files are structured:

- **header data**:
  - list of files and their locations within the file
  - list of directories of lists of file entry names *(unused)*
- **asset contents**:
  - all the files contents. Not realistically parsable without the header data

### How .wad files are parsed:

    - .wad file identifier -      16 byte byte array
    - number of files in wad (N) - 4 byte integer
    - repeat N times:
        - file name len (L) - 4 byte integer
        - file name -         L byte(s) string
        - file size -         8 byte integer
        - file offset -       8 byte integer
    - number of directories (D) - 4 byte integer
    - repeat D times:
      - dir name len (L) - 4 byte integer
      - dir name -         L byte(s) string
      - number of entries in directory (E) - 4 byte integer
      - repeat D times:
        - entry name len (L) - 4 byte integer
        - entry name -         L byte(s) string
        - entry type -         1 byte integer
    - content start - current position in file

## .meta Files

### How .meta files are structured:

- list of sprites:
  - list of images for every sprite

### How .meta files are parsed:

    - .meta file identifier - 16 byte byte array
    - game (hm1 or hm2) -      4 byte integer
    - unused - 4 byte integer
    - repeat until end of file:
      - sprite name len (L) - 1 byte integer
      - sprite name -         L byte(s) string
      - image count (N) -     4 byte integer
      - repeat N times:
        - width -  4 byte integer
        - height - 4 byte integer
        - x -      4 byte integer
        - y -      4 byte integer
        - uv -     4 4 byte floats (16 bytes total) (unused)
