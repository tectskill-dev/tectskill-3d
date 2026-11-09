# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""DXF layer names outside ASCII survive the export.

The writer used to encode the file as ASCII with ``errors="replace"``:
every Thai, accented-Spanish or CJK view title became ``???``, and views
with different titles collapsed into the same layer."""
from __future__ import annotations

import ezdxf
from ezdxf.lldxf.encoding import decode_dxf_unicode

from formats.dxf_out import save_dxf_layers


def _layers(path):
    doc = ezdxf.readfile(str(path))
    return {decode_dxf_unicode(layer.dxf.name) for layer in doc.layers}


def test_non_ascii_layer_names_read_back(tmp_path):
    path = tmp_path / "views.dxf"
    save_dxf_layers(path, [("รูปด้านทิศเหนือ", [(0, 0, 1, 1)]),
                           ("Elevación", [(0, 0, 2, 2)]),
                           ("北立面", [(0, 0, 3, 3)])])
    names = _layers(path)
    assert {"รูปด้านทิศเหนือ", "ELEVACIÓN", "北立面"} <= names
    assert not any("?" in n for n in names)


def test_different_titles_keep_different_layers(tmp_path):
    path = tmp_path / "views.dxf"
    save_dxf_layers(path, [("รูปตัด A-A", [(0, 0, 1, 1)]),
                           ("รูปตัด B-B", [(0, 0, 2, 2)])])
    names = _layers(path)
    assert "รูปตัด_A-A" in names and "รูปตัด_B-B" in names


def test_ascii_names_are_unchanged(tmp_path):
    path = tmp_path / "views.dxf"
    save_dxf_layers(path, [("north view", [(0, 0, 1, 1)])])
    assert "NORTH_VIEW" in _layers(path)
    assert "\\U+" not in path.read_text(encoding="ascii")
