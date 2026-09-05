#!/usr/bin/env python3
"""Regression tests for color.py. Run from anywhere: python3 <path>/test_color.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import color  # noqa: E402


def hexes(c):
    return color.to_hex(c.rgb)


class GrammarTests(unittest.TestCase):
    def test_short_hex_and_alpha_hex(self):
        self.assertEqual(color.parse("#777").hex, "#777777")
        c = color.parse("#0465afcc")
        self.assertEqual(c.hex, "#0465af")
        self.assertAlmostEqual(c.alpha, 0.8, places=2)

    def test_percent_and_hue_units_match_plain_numbers(self):
        a = color.parse("oklch(58% 40% 0.6944444444turn)")
        b = color.parse("oklch(0.58 0.16 250deg)")
        self.assertEqual(a.hex, b.hex)

    def test_alpha_slot_and_none(self):
        c = color.parse("oklch(1 0 0 / 0.10)")
        self.assertEqual(c.hex, "#ffffff")
        self.assertAlmostEqual(c.alpha, 0.10)
        self.assertEqual(color.parse("oklch(0.5 0.1 none)").hex, color.parse("oklch(0.5 0.1 0)").hex)

    def test_lightness_percent_is_not_unit_interval(self):
        self.assertEqual(color.parse("oklch(1% 0 0)").hex, "#000000")

    def test_bad_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            color.parse("hsl(220 90% 55%)")


class QuantizationTests(unittest.TestCase):
    def test_contrast_of_oklch_equals_contrast_of_its_hex(self):
        for spec in ("oklch(0.574 0.05 5)", "oklch(0.568 0 0)", "oklch(0.547 0.15 180)"):
            c = color.parse(spec)
            white = color.parse("#fff")
            self.assertAlmostEqual(color.wcag(c, white), color.wcag(color.parse(c.hex), white), places=9)


class GamutTests(unittest.TestCase):
    def test_out_of_gamut_reports_clipped_hex_and_max_chroma(self):
        c = color.parse("oklch(0.58 0.3 250)")
        self.assertIsNotNone(c.oog)
        self.assertEqual(c.hex, "#006dff")  # what the browser paints today
        self.assertLess(c.oog[3], 0.3)
        self.assertTrue(color.in_gamut(color.oklch_to_rgb(0.58, c.oog[3], 250)))

    def test_in_gamut_has_no_note(self):
        self.assertEqual(color.parse("oklch(0.58 0.16 250)").note(), "")

    def test_contrast_marks_out_of_gamut_verdicts(self):
        line = color.contrast_line(color.parse("#fff"), color.parse("oklch(0.58 0.3 250)"))
        self.assertIn("VERDICT UNRELIABLE", line)


class ContrastTests(unittest.TestCase):
    def test_documented_pairs(self):
        w = color.parse("#ffffff")
        self.assertAlmostEqual(color.wcag(color.parse("#777777"), w), 4.48, places=2)
        self.assertAlmostEqual(color.wcag(w, color.parse("#0465af")), 6.02, places=2)
        self.assertAlmostEqual(color.apca(color.parse("#000"), w), 106.0, places=0)

    def test_translucent_foreground_is_composited(self):
        fg, bg = color.parse("oklch(1 0 0 / 0.10)"), color.parse("oklch(0.24 0.015 250)")
        line = color.contrast_line(fg, bg)
        self.assertIn("composited", line)
        self.assertLess(color.wcag(color.composite(fg, bg), bg), color.wcag(color.parse("#fff"), bg))

    def test_translucent_background_is_rejected(self):
        with self.assertRaises(ValueError):
            color.composite(color.parse("#fff"), color.parse("#00000080"))


class CliTests(unittest.TestCase):
    def test_multiple_pairs(self):
        out = color.run(["contrast", "#777", "#fff", "#fff", "#0465af"])
        self.assertEqual(len(out), 2)

    def test_units_in_palette_and_ramp(self):
        self.assertEqual(len(color.run(["palette", "60%", "0.14", "25deg", "145"])), 2)
        self.assertEqual(len(color.run(["ramp", "250deg", "0.1", "50%", "0.3"])), 2)

    def test_missing_arguments_are_usage_errors(self):
        for argv in (["hex"], ["contrast", "#fff"], ["oklch", "0.5", "0.1"], ["palette", "0.6", "0.1"]):
            with self.assertRaises(ValueError):
                color.run(argv)


if __name__ == "__main__":
    unittest.main()
