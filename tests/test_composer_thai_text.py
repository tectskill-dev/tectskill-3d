# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Thai on the sheets: the bundled Sarabun face is what gets drawn, and the
label background covers stacked tone marks and below-vowels (ุ ู)."""
from tests.test_composer_etiqueta import _margins_mm


def test_generic_family_resolves_to_bundled_sarabun():
    from PySide6.QtGui import QFont, QFontInfo
    from core.fonts import resolve_family
    assert resolve_family("Sans Serif") == "Sarabun"
    assert resolve_family("") == "Sarabun"
    assert QFontInfo(QFont(resolve_family(""))).family() == "Sarabun"
    assert resolve_family("Noto Sans Thai") == "Noto Sans Thai"


def test_thai_ink_stays_inside_the_background():
    for text in ["รูปด้านทิศเหนือ", "ผู้ที่ปู่ญาติ", "ฤดูฝน\nบ้านพักอาศัย",
                 "โครงการก่อสร้างอาคารพักอาศัยสองชั้นพร้อมที่จอดรถ"]:
        top, bottom = _margins_mm(text)
        assert 0.2 <= top <= 1.6, (text, top)
        assert 0.2 <= bottom <= 1.2, (text, bottom)


def test_text_width_follows_the_family():
    import pytest
    from PySide6.QtGui import QFontDatabase
    from views.composer import _text_width_mm
    if "Tlwg Mono" not in QFontDatabase.families():
        pytest.skip("needs a second Thai face installed (fonts-thai-tlwg)")
    a = _text_width_mm("รูปด้านทิศเหนือ", 5.0)
    b = _text_width_mm("รูปด้านทิศเหนือ", 5.0, family="Tlwg Mono")
    assert a > 0 and abs(a - b) > 0.5
