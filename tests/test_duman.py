"""Duman testi: depodaki her çalıştırılabilir script hatasız bitmeli.

Kitap değerlerini doğrulayan testler `test_chNN_*.py` dosyalarındadır.
"""
from __future__ import annotations

import os
import subprocess
import sys

import pytest

from yardimci import KOK

SCRIPTLER = sorted(
    p for p in KOK.glob("ch*/**/*.py") if "__pycache__" not in p.parts
)


@pytest.mark.parametrize("yol", SCRIPTLER, ids=lambda p: str(p.relative_to(KOK)).replace("\\", "/"))
def test_script_calisir(yol):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8", MPLBACKEND="Agg")
    sonuc = subprocess.run(
        [sys.executable, str(yol)],
        cwd=yol.parent,
        env=ortam,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
    )
    assert sonuc.returncode == 0, sonuc.stderr[-2000:]
    assert sonuc.stdout.strip(), "script hiçbir şey yazdırmadı"
