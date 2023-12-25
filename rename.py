'''
Module for renaming files to make them compilent with PLEX media server
'''

from os import path, listdir, rename as rename_file
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
    '^(\\[[\\S _\\.]+?\\])?[ _]?(.+)[ _\\.]((\\[((\\d{1,2})([ _]of[ _]\\d{1,2}[ _\\.]?)?)\\])|(\\d{1,2})|([Ss]\\d{1,2}[Ee](\\d{1,2}))|(\\d{1,2}[Xx](\\d{1,2})))([ _\\.]\\[.+?\\])*\\.(.*)$')

__simple_season_and_episode_regex = re.compile(
    '.*[Ss]\\d{1,2}[Ee](\\d{1,2}).*')


def __get_episode_number(filename: str) -> int | None:
    match = __simple_season_and_episode_regex.match(filename)
    if match is not None:
        episode = match.group(1)
        return int(episode)

    match = __episode_regex.match(filename)
    if match is not None:
        episode = match.group(6) if match.group(6) is not None else match.group(8) if match.group(
            8) is not None else match.group(10) if match.group(10) is not None else match.group(12)
        return int(episode)

    return None


def prepare_change_filenames(paths: list[str], season=1, prefix=None, prefx_separator='_') -> ChangeFileNamesResult:
    rename_map = []
    rename_map_filenames = []
    skipped_files = []

    for p in paths:
        dir = path.dirname(p)
        _, extension = path.splitext(p)
        filename = path.basename(p)

        episode = __get_episode_number(filename)
        if episode is None:
            skipped_files += [p]
            continue

        new_name = 'S%02dE%02d%s' % (season, episode, extension)

        if prefix is not None:
            new_name = '%s%s%s' % (prefix, prefx_separator, new_name)

        rename_map_filenames += [(filename, new_name)]
        rename_map += [(p, path.join(dir, new_name))]

    return ChangeFileNamesResult(rename_map, rename_map_filenames, skipped_files)


def prepare_change_filenames_in_dir(dir: str, season=1, prefix=None, prefx_separator='_') -> ChangeFileNamesResult:
    files = []
    for f in listdir(dir):
        full_path = path.join(dir, f)
        if path.isfile(full_path):
            files += [full_path]

    return prepare_change_filenames(files, season=season, prefix=prefix, prefx_separator=prefx_separator)


def get_duplicated_destanations(srcToDest: list[(str, str)]) -> list[(str, list[str])]:
    unique_map: dict[str, list[str]] = dict()

    for src, dest in srcToDest:
        unique_map.setdefault(dest, [])
        unique_map[dest] += [src]

    duplicates: list[str, list[str]] = []

    for key in unique_map.keys():
        if len(unique_map[key]) > 1:
            duplicates += [(key, unique_map[key])]

    return duplicates


def __build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='rename.py',
                                     description='Utility for renaming files to make them compilent with PLEX media server')

    parser.add_argument('dirpath')
    parser.add_argument('-y', '--run', action='store_true')
    parser.add_argument('--dry', action='store_true')
    parser.add_argument('--prefix')
    parser.add_argument('--season')

    return parser


if __name__ == '__main__':
    parser = __build_argparser()

    args = parser.parse_args()
    season = int(args.season) if args.season is not None else 1

    result = prepare_change_filenames_in_dir(
        args.dirpath, season, prefix=args.prefix)

    print('Will rename following files like so:')
    for src, dst in result.rename_map_filenames:
        print('%s -> %s' % (src, dst))

    print('\n\nFollowing files will be skipped:')
    for p in result.skipped_files:
        print(p)

    duplicates = get_duplicated_destanations(result.rename_map)
    if len(duplicates) > 0:
        print('\n\nFound duplicates:')
        for dst, sources in duplicates:
            print('Target "%s" is duplicated by:' % dst)
            for src in sources:
                print(src)

        exit(1)

    if args.dry:
        exit(0)

    if args.run is not True:
        print('\n\nRename? (Y/N):')
        userInput = input()
        if userInput.upper() != 'Y':
            print('Aborting')
            exit(1)

    print('\nRenaming')

    for src, dst in result.rename_map:
        print('Moving %s -> %s' % (src, dst))
        rename_file(src, dst)
