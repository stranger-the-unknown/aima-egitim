#!/usr/bin/env python3
"""Bayes ağı CPT'lerini Türkçe başlıklarla yazdırma.

Özgün eğitim örneği (ofis: Yangın / Sigara / Alarm / MüdürArar).
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

# CPT: ebeveyn değer demeti -> P(düğüm=True)
# Boolean ağ; False olasılığı = 1 - True


def yazdir_oncel(ad: str, p_true: float) -> None:
    print(f"── CPT: {ad} (kök / önsel) ──")
    print(f"  P({ad}=T) = {p_true:.4f}")
    print(f"  P({ad}=F) = {1 - p_true:.4f}")
    print()


def yazdir_cpt(
    ad: str,
    ebeveynler: Sequence[str],
    tablo: Dict[Tuple[bool, ...], float],
) -> None:
    print(f"── CPT: {ad} | {', '.join(ebeveynler)} ──")
    header = " | ".join(f"{e:>8}" for e in ebeveynler) + f" | P({ad}=T)"
    print("  " + header)
    print("  " + "-" * len(header))
    for key in sorted(tablo.keys(), key=lambda k: tuple(0 if x else 1 for x in k)):
        cells = " | ".join(f"{'T' if v else 'F':>8}" for v in key)
        print(f"  {cells} | {tablo[key]:.4f}")
    print()


def main() -> None:
    print("Ofis alarm ağı — CPT gösterimi (özgün eğitim)\n")
    print("Yapı: Yangin → Alarm ← SigaraDumanı ; Alarm → MudurArar\n")

    yazdir_oncel("Yangin", 0.01)
    yazdir_oncel("SigaraDumanı", 0.05)

    alarm_cpt = {
        (True, True): 0.95,
        (True, False): 0.88,
        (False, True): 0.70,
        (False, False): 0.001,
    }
    yazdir_cpt("Alarm", ["Yangin", "SigaraDumanı"], alarm_cpt)

    mudur_cpt = {
        (True,): 0.80,
        (False,): 0.05,
    }
    yazdir_cpt("MudurArar", ["Alarm"], mudur_cpt)

    print("Joint faktörizasyon:")
    print("  P(Y,S,A,M) = P(Y)·P(S)·P(A|Y,S)·P(M|A)")


if __name__ == "__main__":
    main()
