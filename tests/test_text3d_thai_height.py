# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""What a 3D text's height measures (``height_ref``). With the whole-block
rule a Thai tone mark or below-vowel ate into the height: at 0.25 m «กขค»
had 0.25 m consonants but «บ้าน» only ~0.15 m. «Letter body» sizes the base
letter instead (ก for Thai, H otherwise); «Automatic» picks it for Thai."""
from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

_app = QApplication.instance() or QApplication([])

from core.text3d import (build_text_letters, build_text_mesh,  # noqa: E402
                         make_text_group, rebuild_text_group,
                         resolve_height_ref, text_params)


def _h(mesh):
    zs = [v.position.z() for v in mesh.vertices]
    return max(zs) - min(zs), min(zs)


def test_automatic_means_body_for_thai_and_block_otherwise():
    assert resolve_height_ref("บ้าน", "auto") == "body"
    assert resolve_height_ref("บ้าน HOUSE", "auto") == "body"
    assert resolve_height_ref("HOUSE", "auto") == "block"
    assert resolve_height_ref("บ้าน", "block") == "block"
    assert text_params("x")["height_ref"] == "auto"


@pytest.mark.parametrize("text, plain", [
    ("บ้าน", "าน"), ("ห้องน้ำ", "อง"), ("ผู้ที่ปู่", ""), ("กขค", "กขค")])
def test_thai_consonants_get_the_height_asked_for(text, plain):
    """Every mark-free letter of the word (``plain``) is as tall as asked —
    a round top overshoots a little — whatever stacks above or hangs below
    the rest; the lowest point still sits on the ground."""
    letters = build_text_letters(text, "", True, False, 0.25, 0.05, "auto")
    for ch, mesh in letters:
        if ch in plain:
            assert _h(mesh)[0] == pytest.approx(0.25, rel=0.03), ch
    assert _h(build_text_mesh(text, "", True, False, 0.25, 0.05,
                              "auto"))[1] == pytest.approx(0.0, abs=1e-9)


def test_latin_text_is_unchanged_by_automatic():
    a = build_text_mesh("HOUSE", "", True, False, 0.5, 0.05, "block")
    b = build_text_mesh("HOUSE", "", True, False, 0.5, 0.05, "auto")
    assert _h(a) == pytest.approx(_h(b))
    assert _h(b)[0] == pytest.approx(0.5)


def test_a_text_from_before_the_option_keeps_its_size():
    """A ``text3d`` record without ``height_ref`` was laid out by the block
    rule; re-laying it out (an edit command) must not resize it."""
    old = {k: v for k, v in text_params("บ้าน", height=0.25).items()
           if k != "height_ref"}
    g = make_text_group(old)
    assert "height_ref" not in g.text3d
    kids = rebuild_text_group(g, old)
    top = max(max(v.position.z() for v in k.mesh.vertices) for k in kids)
    assert top == pytest.approx(0.25)


def test_the_choice_round_trips_through_igz(tmp_path):
    from core.scene import Scene
    from formats import igz
    scene = Scene()
    scene.groups.append(make_text_group(
        text_params("บ้าน", height=0.25, height_ref="body")))
    p = tmp_path / "t.igz"
    igz.save_scene(scene, p)
    scene2 = Scene()
    igz.load_into(scene2, p)
    assert scene2.groups[0].text3d["height_ref"] == "body"
    assert scene2.groups[0].text3d == scene.groups[0].text3d


def _dialog(monkeypatch, params=None):
    from PySide6.QtWidgets import QComboBox, QDialog
    from views.main_window import MainWindow
    win = MainWindow()
    seen = {}

    def fake_exec(dlg):
        seen["ref"] = dlg.findChildren(QComboBox)[-1].currentData()
        return QDialog.Accepted
    try:
        monkeypatch.setattr(QDialog, "exec", fake_exec)
        out = win._text3d_dialog(params)
    finally:
        win._saved_version = win.viewport.scene.version
        win.close()
    return seen["ref"], out


def test_dialog_new_text_starts_automatic(monkeypatch):
    shown, out = _dialog(monkeypatch)
    assert shown == "auto" and out["height_ref"] == "auto"


def test_dialog_editing_an_old_text_shows_whole_text(monkeypatch):
    old = {k: v for k, v in text_params("บ้าน").items() if k != "height_ref"}
    shown, out = _dialog(monkeypatch, old)
    assert shown == "block" and out["height_ref"] == "block"
