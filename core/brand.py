# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""The name this build shows its users.

TectSkill-3D is a Thai edition of IngeTrazo. Every message the interface
shows goes through :func:`core.i18n.tr`, which passes it through
:func:`brand` so «IngeTrazo» reads as :data:`APP_NAME` — in every
language, without forking 3 000 catalogue strings.

What is NOT renamed, on purpose:

* the settings, logs and extensions folders (``QSettings`` organisation and
  application name stay «IngeTrazo»), so preferences and installed
  extensions keep working and stay compatible with upstream;
* identifiers that are commands or file names (the Flatpak app id);
* the credits: whoever built IngeTrazo is credited as IngeTrazo
  (:func:`core.i18n.tr_raw`), as the GPL asks.
"""
from __future__ import annotations

#: The name shown in titles, menus, dialogs and messages.
APP_NAME = "TectSkill-3D"
#: Who publishes this edition, and where.
PUBLISHER = "TectSkill"
PUBLISHER_URL = "https://tectskill.com"
#: Where the source code of THIS edition can be downloaded (GPL-3.0 §6).
#: Put the address of your fork here, e.g. "https://github.com/<you>/ingetrazo".
#: Empty: the About dialog links only to upstream IngeTrazo.
SOURCE_URL = "https://github.com/tectskill-dev/tectskill-3d"

#: The language a first start opens in, whatever the Windows locale says
#: (most Thai PCs run an English Windows). A language picked later in
#: Window > Language still wins. Empty: follow the system locale.
DEFAULT_LANGUAGE = "th"

#: The upstream project this edition is built on.
UPSTREAM_NAME = "IngeTrazo"
UPSTREAM_URL = "https://github.com/ingelibre/ingetrazo"

#: Substrings holding «IngeTrazo» that are identifiers, not names: a
#: user types or pastes them, so they must stay exactly as they are.
_PROTECTED = ("com.ingetrazo.IngeTrazo",)


def brand(text: str) -> str:
    """``text`` with the upstream name replaced by :data:`APP_NAME`."""
    if not text or UPSTREAM_NAME not in text or APP_NAME == UPSTREAM_NAME:
        return text
    keep = {}
    for i, token in enumerate(_PROTECTED):
        if token in text:
            mark = f"\x00{i}\x00"
            keep[mark] = token
            text = text.replace(token, mark)
    text = text.replace(UPSTREAM_NAME, APP_NAME)
    for mark, token in keep.items():
        text = text.replace(mark, token)
    return text
