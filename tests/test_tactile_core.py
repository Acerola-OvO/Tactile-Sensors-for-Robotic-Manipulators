import unittest

import numpy as np

from software.tactile_core import (
    FrameAssembler,
    FrameFormatError,
    ProcessorConfig,
    TactileProcessor,
    median_baseline,
    parse_row,
)


class ParserTests(unittest.TestCase):
    def test_parse_valid_row(self):
        row = parse_row("1 2 3 4", columns=4)
        np.testing.assert_array_equal(row, np.array([1, 2, 3, 4], dtype=np.float32))

    def test_parse_blank_delimiter(self):
        self.assertIsNone(parse_row("   ", columns=4))

    def test_wrong_column_count(self):
        with self.assertRaises(FrameFormatError):
            parse_row("1 2 3", columns=4)

    def test_frame_assembly(self):
        assembler = FrameAssembler(rows=2, columns=2)
        self.assertIsNone(assembler.push("1 2"))
        self.assertIsNone(assembler.push("3 4"))
        frame = assembler.push("")
        np.testing.assert_array_equal(frame, np.array([[1, 2], [3, 4]], dtype=np.float32))


class ProcessingTests(unittest.TestCase):
    def test_median_baseline(self):
        frames = [np.zeros((2, 2)), np.ones((2, 2)), np.full((2, 2), 10)]
        np.testing.assert_array_equal(median_baseline(frames), np.ones((2, 2)))

    def test_fixed_normalization(self):
        processor = TactileProcessor(
            baseline=np.zeros((2, 2)),
            config=ProcessorConfig(threshold=0, clip_max=100, ema_alpha=1.0),
        )
        output = processor.process(np.array([[0, 50], [100, 200]], dtype=np.float32))
        np.testing.assert_allclose(output, np.array([[0, 0.5], [1, 1]], dtype=np.float32))


if __name__ == "__main__":
    unittest.main()
