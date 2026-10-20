# SPDX-License-Identifier: GPL-3.0-or-later
"""TectSkill-3D branding: the interface says the edition's name, the
credits and the identifiers keep IngeTrazo's."""
from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication  # noqa: E402

_app = QApplication.instance() or QApplication([])

from core.brand import APP_NAME, brand  # noqa: E402
from core.i18n import current_language, set_language, tr, tr_raw  # noqa: E402


def test_messages_carry_the_edition_name_in_every_language():
    before = current_language()
    try:
        for lang in ("en", "th", "es"):
            set_language(lang)
            assert APP_NAME in tr("About IngeTrazo")
            assert "IngeTrazo" not in tr("Quit IngeTrazo?")
    finally:
        set_language(before)


def test_identifiers_are_left_alone():
    cmd = "flatpak override --user com.ingetrazo.IngeTrazo"
    assert brand(cmd) == cmd
    assert brand("IngeTrazo and com.ingetrazo.IngeTrazo") == \
        f"{APP_NAME} and com.ingetrazo.IngeTrazo"


def test_credits_keep_the_upstream_name():
    role = "The macOS package: IngeTrazo for Mac."
    assert "IngeTrazo" in tr_raw(role)


def test_about_dialog_names_the_edition_and_credits_upstream():
    from PySide6.QtWidgets import QLabel
    from views.about_dialog import AboutDialog
    dlg = AboutDialog(None, "9.8.7")
    html = " ".join(lab.text() for lab in dlg.findChildren(QLabel))
    assert APP_NAME in dlg.windowTitle()
    assert APP_NAME in html and "Marco Sumari Tellez" in html
    assert "IngeTrazo" in html          # the program it is built on
    assert "github.com/ingelibre/ingetrazo" in html
    dlg.close()
