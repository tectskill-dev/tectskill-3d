# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Leader texts in the viewport: lines one font height apart, except when
Thai tone marks stacked over one line would touch the below-vowels (ุ ู)
hanging from the line above — then just far enough apart not to."""
from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QFontMetrics  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

_app = QApplication.instance() or QApplication([])

from views.viewport import (_label_baselines, _label_font,  # noqa: E402
                            _label_line_ink)


def test_latin_lines_keep_one_font_height_apart():
    font = _label_font(9)
    fm = QFontMetrics(font)
    offs = _label_baselines(["Pileta de", "piedra basalto", "gyp"], fm, font)
    assert offs == [0.0, fm.height(), 2 * fm.height()]


def test_thai_lines_never_touch():
    font = _label_font(9)
    fm = QFontMetrics(font)
    lines = ["ปู่ผู้ดูแล", "ที่นี่ญี่ปุ่น", "ฤดูกาลน้ำ"]
    offs = _label_baselines(lines, fm, font)
    for i in range(len(lines) - 1):
        below = _label_line_ink(lines[i], font)[1]
        above = _label_line_ink(lines[i + 1], font)[0]
        assert offs[i + 1] - offs[i] >= below + above + 2.0 - 1e-9
        assert offs[i + 1] - offs[i] >= fm.height()


def test_labels_draw_in_the_bundled_face():
    from PySide6.QtGui import QFontInfo
    assert QFontInfo(_label_font(9)).family() == "Sarabun"
