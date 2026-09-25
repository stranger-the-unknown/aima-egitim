#!/usr/bin/env python3
"""Kurulum kontrolü: Python sürümü ve temel bağımlılıklar."""

from __future__ import annotations

import sys


def main() -> int:
    print("AIMA Eğitim — kurulum kontrolü")
    print("-" * 40)

    major, minor = sys.version_info[:2]
    print(f"Python: {sys.version.split()[0]}")
    if (major, minor) < (3, 10):
        print("HATA: Python 3.10+ gerekli.")
        return 1
    print("OK: Python sürümü uygun (3.10+).")

    eksikler: list[str] = []
    # numpy ve pytest zorunlu; matplotlib yalnızca isteğe bağlı grafikler için.
    for mod, zorunlu in (("numpy", True), ("pytest", True), ("matplotlib", False)):
        try:
            __import__(mod)
            print(f"OK: {mod} import edildi.")
        except ImportError:
            if zorunlu:
                print(f"EKSIK: {mod} — `pip install -r requirements.txt` çalıştırın.")
                eksikler.append(mod)
            else:
                print(f"UYARI: {mod} yok — grafikler atlanır, örnekler yine çalışır.")

    print("-" * 40)
    if eksikler:
        print(f"Sonuç: {len(eksikler)} paket eksik.")
        return 1
    print("Sonuç: Kurulum hazır. Testler: pytest  ·  Örnek: python ch01-giris/ornekler/vacuum_agent.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
