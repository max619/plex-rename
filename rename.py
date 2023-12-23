'''
Module for renaming files to make them compilent with PLEX media server
'''

from os import path, listdir
import re
import argparse


class ChangeFileNamesResult:
    rename_map: list[(str, str)]
    rename_map_filenames: list[(str, str)]
    skipped_files: list[(str)]

    def __init__(self, rename_map: list[(str, str)], rename_map_filenames: list[(str, str)], skipped_files: list[str]):
        self.rename_map = rename_map
        self.rename_map_filenames = rename_map_filenames
        self.skipped_files = skipped_files


__episode_regex = re.compile(
    '^(\\[[\\S _]+?\\])?[ _]?(.+?)[ _]\\[?((\\d{1,2})([ _]of[ _]\\d{1,2}[ _]?)?)\\]?([ _]\\[.+?\\])*\\.(.*)$')


def prepare_change_filenames(paths: list[str], season=1) -> ChangeFileNamesResult:
    rename_map = []
    rename_map_filenames = []
    skipped_files = []

    for p in paths:
        dir = path.dirname(p)
        _, extension = path.splitext(p)
        filename = path.basename(p)

        match = __episode_regex.match(filename)
        if match is None:
            skipped_files += [p]
            continue

        episode = int(match.group(4))

        new_name = 'S%02dE%02d%s' % (season, episode, extension)

        rename_map_filenames += [(filename, new_name)]
        rename_map += [(p, path.join(dir, new_name))]

    return ChangeFileNamesResult(rename_map, rename_map_filenames, skipped_files)


def prepare_change_filenames_in_dir(dir: str, season=1) -> ChangeFileNamesResult:
    files = []
    for f in listdir(dir):
        full_path = path.join(dir, f)
        if path.isfile(full_path):
            files += [full_path]

    return prepare_change_filenames(files, season)


def __build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='rename.py',
                                     description='Utility for renaming files to make them compilent with PLEX media server')

    parser.add_argument('dirpath')
    parser.add_argument('-y', '--run', action='store_true')
    parser.add_argument('--dry', action='store_true')
    parser.add_argument('--season')

    return parser


if __name__ == '__main__':
    parser = __build_argparser()

    args = parser.parse_args()
    season = int(args.season) if args.season is not None else 1

    result = prepare_change_filenames_in_dir(args.dirpath, season)

    print('Will rename following files like so:')
    for src, dst in result.rename_map_filenames:
        print('%s -> %s' % (src, dst))

    print('\n\nFollowing files will be skipped:')
    for p in result.skipped_files:
        print(p)

    if args.dry:
        exit(0)

    if args.run is not True:
        print('\n\nRename? (Y/N):')
        userInput = input()
        if userInput.upper() != 'Y':
            print('Aborting')
            exit(1)

    print('\nRenaming')
