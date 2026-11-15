# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""The text font the sheets and the 3D Text tool use, shipped with the app.

The composer used to ask for the generic ``"Sans Serif"``, which every OS
resolves to a different face (DejaVu Sans, Arial, Helvetica…). For Thai
that face has no glyphs at all, so Qt silently fell back to whatever Thai
font the machine had — and every measurement (width, line height, the
background slab) was still taken from the Latin face, so the inked Thai
letters did not match what was measured: below-vowels (ุ ู) poked out
of the label's background and sheets looked different on every machine.

Sarabun (SIL OFL 1.1, ``resources/fonts/sarabun``) covers Thai and Latin
in one face with Thai-aware metrics, so the face that is measured is the
face that is drawn, identically on Linux, Windows and macOS.

Documents keep storing ``"Sans Serif"`` as the family (files stay
compatible with upstream IngeTrazo); :func:`resolve_family` maps that
generic name — and an empty one — to :data:`DEFAULT_FAMILY` at draw time.
"""
from __future__ import annotations

#: The face drawn wherever a document asks for the generic family.
DEFAULT_FAMILY = "Sarabun"

#: Family names that mean "the app's default text face", not a real font.
GENERIC_FAMILIES = frozenset({"", "sans serif", "sans-serif", "sans"})

_registered: bool | None = None


def register_bundled_fonts() -> bool:
    """Load the fonts under ``resources/fonts`` into Qt's font database.
    Idempotent; needs a QGuiApplication. Returns True when
    :data:`DEFAULT_FAMILY` is available afterwards (bundled or installed)."""
    global _registered
    if _registered is not None:
        return _registered
    from PySide6.QtGui import QFontDatabase, QGuiApplication
    if QGuiApplication.instance() is None:
        return False                      # try again once there is an app
    from core.paths import app_root
    folder = app_root() / "resources" / "fonts"
    for path in sorted(folder.rglob("*.[ot]tf")) if folder.is_dir() else []:
        QFontDatabase.addApplicationFont(str(path))
    _registered = DEFAULT_FAMILY in QFontDatabase.families()
    return _registered


def resolve_family(family: str | None) -> str:
    """The real family to draw ``family`` with: the bundled default for the
    generic names, the name itself otherwise."""
    name = (family or "").strip()
    if name.lower() in GENERIC_FAMILIES:
        return DEFAULT_FAMILY if register_bundled_fonts() else "Sans Serif"
    register_bundled_fonts()
    return name
