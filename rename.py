'''
Module for renaming files to make them compilent with PLEX media server
'''

from os import path
import re


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
