'''

hm2 wad structure:
    metadata:
        hm2 wad file identifier - 16 bytes
        number of files in the wad (N) - 4 bytes
        repeat N times:
            file name len (L) - 4 bytes
            file name - L bytes
            file len - 8 bytes
            file offset - 8 bytes

        (not used but needs to get parsed)
        number of directories (D) - 4 bytes
        repeat D times:
            dir name len (L) - 4 bytes
            dir name - L bytes
            number of entries in directory (E) - 4 bytes
            repeat E times:
                entry name len (L) - 4 bytes
                entry name - L bytes
                entry type - 1 byte
    contents:
        global content start position - current position in file after metadata parse
        the rest of the file is just data. To find specific files in here use the parsed metadata

'''

import os

os.system('cls' if os.name == 'nt' else 'clear')
print('This script is used for parsing HM2 .wad files. The result is a folder containing hm2 files')

SRC_WAD = input('.wad file to extract from: ')
while not os.path.exists(SRC_WAD):
    SRC_WAD = input('.wad file to extract from: ')
FILES_TO_FIND = input('What files would you like to extract (comma separated or leave empty for all): ').strip().replace(' ', '').split(',')
DEST_DIR = input('Location to put these files: ')


def openf(*args, **kwargs):
    os.makedirs(os.path.dirname(args[0]), exist_ok=True)
    return open(*args, **kwargs)


with open(SRC_WAD, 'rb') as f:
    # header identifier
    f.read(0x10)

    # read file count
    file_count = int.from_bytes(f.read(0x04), 'little')
    print(file_count, 'files in wad')

    # file dic
    files = {}


    # loop for each file
    for i in range(file_count):
        # create file dic
        file = {}

        # read file name length
        file_name_len = int.from_bytes(f.read(0x04), 'little')

        # read file name base on length found
        file['name'] = f.read(file_name_len).decode('ascii')

        # read file length
        file['len'] = int.from_bytes(f.read(0x08), 'little')

        # read file offset
        file['offset'] = int.from_bytes(f.read(0x08), 'little')

        # add file to file dic
        files[os.path.basename(file['name'])] = file

    # parse directory table
    # see: https://github.com/TcT2k/HLMWadExplorer/blob/b19bc753dd1043d657ccc042daeb7c34d81ac1e2/WADArchive.cpp#L265
    # loop over directory
    dir_count = int.from_bytes(f.read(0x04), 'little')
    for i in range(dir_count):

        # read directory name len
        dir_name_len = int.from_bytes(f.read(0x04), 'little')

        # read directory name
        dir_name = f.read(dir_name_len).decode('ascii')

        # read directory entry count
        entry_count = int.from_bytes(f.read(0x04), 'little')
        # parse directory
        for i in range(entry_count):
            entry_name_len = int.from_bytes(f.read(0x04), 'little')
            entry_name = f.read(entry_name_len).decode('ascii')
            entry_type = int.from_bytes(f.read(0x01), 'little')

    # file contents offset
    contents_offset = f.tell()

    if ''.join(FILES_TO_FIND) == '':
        FILES_TO_FIND = files.keys()
    # extract files
    for key in FILES_TO_FIND:
        if key not in files:
            print(f'{key} not found!')
            continue
        file = files[key]
        # seek to files position in file
        f.seek(file['offset'] + contents_offset)
        # extract and export file's contents to a file
        with openf(DEST_DIR+'\\'+file['name'], 'wb') as out_f:
            out_f.write(f.read(file['len']))

        # print file data for funsies
        print(file['name']+': ', f"\t{hex(file['offset'])} - {hex(file['offset']+file['len'])}")
