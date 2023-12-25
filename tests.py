import unittest
import rename


class TestRename(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def test(self):
        skipped_files = [
            'abcd/[SRC]_Title_With_Many_Words_[720p_h264_AAC]_[Additional Info].tmp.bck.avi',
            'abcd/[SRC]_Title_With_Many_Words_[IDK]_[720p_h264_AAC]_[Additional Info].tmp.bck.avi'
        ]

        expected_result = [
            (
                'dira/[SRC]_Title_With_Many_Words_01_[720p_h264_AAC]_[Additional Info].mp4',
                'dira/S02E01.mp4'
            ),
            (
                'dirb/[SRC] Title With Many Words 02 [720p_h264_AAC]_[Additional Info].mkv',
                'dirb/S02E02.mkv'
            ),
            (
                'dir/subdir/[SRC] Title_With_Many_Words [03] [720p_h264_AAC]_[Additional Info].tmp.mp4',
                'dir/subdir/S02E03.mp4'
            ),
            (
                '[SRC]_Title_With_Many_Words_[04 of 12]_[720p_h264_AAC]_[Additional Info].tmp.bck.avi',
                'S02E04.avi'
            ),
            (
                'abcd/[SRC]_Title_With_Many_Words_[05_of_12]_[720p_h264_AAC]_[Additional Info].tmp.bck.avi',
                'abcd/S02E05.avi'
            ),
            (
                'dir/subdir/[SRC] Title_With_Many_Words [06].mp4',
                'dir/subdir/S02E06.mp4'
            ),
            (
                'Title_With_Many_Words [07].mp4',
                'S02E07.mp4'
            ),
            (
                'Title_With_Many_Words 2 [08].mp4',
                'S02E08.mp4'
            ),
            (
                'Title_With_Many_Words 2 S33E9.mp4',
                'S02E09.mp4'
            ),
            (
                'title.s01e10.some.info.[H264_AAC_128].mkv',
                'S02E10.mkv'
            ),
            (
                'title.s01e11.some.info_[H264_AAC_128].mkv',
                'S02E11.mkv'
            ),
            (
                'title.s01e12.mkv',
                'S02E12.mkv'
            ),
            (
                'title.1X13.mkv',
                'S02E13.mkv'
            ),
            (
                'title.1x14.mkv',
                'S02E14.mkv'
            ),
            (
                'S03E15.tmp.video.mkv',
                'S02E15.mkv'
            ),
            (
                's3e16.mkv',
                'S02E16.mkv'
            )
        ]

        paths = []
        for result_entry in expected_result:
            src, _ = result_entry
            paths += [src]

        result = rename.prepare_change_filenames(
            paths + skipped_files, season=2)

        self.assertEqual(result.rename_map, expected_result)
        self.assertEqual(result.skipped_files, skipped_files)

    def test_unique_destanation(self):
        test_data = [
            (
                'src1',
                'S01E01.mp4'
            ),
            (
                'src2',
                'S01E01.mp4'
            ),
            (
                'src3',
                'S01E02.mkv'
            ),
        ]

        res = rename.get_duplicated_destanations(test_data)
        self.assertEqual(res, [('S01E01.mp4', ['src1', 'src2'])])


if __name__ == '__main__':
    unittest.main()
