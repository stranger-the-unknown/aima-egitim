"""Test yardımcıları: bölüm klasörlerindeki scriptleri modül olarak yükler.

Bölüm klasörlerinin adlarında tire olduğu için normal `import` çalışmaz;
bu yüzden dosyayı yolundan yüklüyoruz.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

KOK = Path(__file__).resolve().parents[1]


def yukle(goreli_yol: str) -> ModuleType:
    """`ch03-cozum-arama/ornekler/romania_arama.py` gibi bir yolu modül olarak yükle."""
    yol = KOK / goreli_yol
    ad = "_".join(yol.with_suffix("").parts[-3:]).replace("-", "_")
    if ad in sys.modules:
        return sys.modules[ad]
    spec = importlib.util.spec_from_file_location(ad, yol)
    assert spec and spec.loader, f"yüklenemedi: {yol}"
    modul = importlib.util.module_from_spec(spec)
    sys.modules[ad] = modul  # dataclass vb. için gerekli
    # Script kendi klasöründeki yardımcıları import edebilsin
    sys.path.insert(0, str(yol.parent))
    try:
        spec.loader.exec_module(modul)
    finally:
        sys.path.remove(str(yol.parent))
    return modul
