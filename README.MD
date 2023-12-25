# plex-rename

![example workflow](https://github.com/max619/plex-rename/actions/workflows/python-app.yml/badge.svg)

This is an untility script for renaming episodes of series to Plex Media Server format

That script will rename series episodes in a following format:
```
Title_[12]_[SomeSite]_[WEBRip_1080p_HEVC].mkv -> S02E12.mkv
Title_[13]_[SomeSite]_[WEBRip_1080p_HEVC].mkv -> S02E13.mkv
Title_[24]_[SomeSite]_[WEBRip_1080p_HEVC].mkv -> S02E24.mkv
Title_[11]_[SomeSite]_[WEBRip_1080p_HEVC].mkv -> S02E11.mkv
Title_[10]_[SomeSite]_[WEBRip_1080p_HEVC].mkv -> S02E10.mkv
```

## Usage

```sh
rename.py [-h] [-y] [--dry] [--prefix PREFIX] [--season SEASON] dirpath
```
