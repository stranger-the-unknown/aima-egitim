#!/usr/bin/env python3
"""Minik naif Bayes: el sayımlarıyla spam / ham sınıflandırma.

Özgün eğitim örneği. sklearn yok; sayımlar elle / sözlükle.
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple

# --- Eğitim verisi (Türkçe kısa mesajlar) ---
EGITIM: List[Tuple[str, str]] = [
    ("spam", "bedava kredi hemen kazan"),
    ("spam", "kazan hediye tıkla bedava"),
    ("spam", "kredi onaylandı tıkla hemen"),
    ("ham", "toplantı yarın saat üçte"),
    ("ham", "proje raporu yarın teslim"),
    ("ham", "öğle yemeği saat ikide"),
    ("ham", "rapor toplantı notları hazır"),
    ("spam", "bedava hediye kazan onay"),
]

# Laplace (add-one) yumuşatma
ALPHA = 1.0


def tokenize(metin: str) -> List[str]:
    return [w for w in metin.lower().split() if w]


def egit(veri: Sequence[Tuple[str, str]]) -> dict:
    sinif_say: Dict[str, int] = defaultdict(int)
    kelime_say: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    sozluk: set[str] = set()

    for sinif, metin in veri:
        sinif_say[sinif] += 1
        for w in tokenize(metin):
            kelime_say[sinif][w] += 1
            sozluk.add(w)

    n = sum(sinif_say.values())
    onsel = {c: sinif_say[c] / n for c in sinif_say}
    # her sınıfta toplam token
    toplam_token = {c: sum(kelime_say[c].values()) for c in sinif_say}
    return {
        "onsel": onsel,
        "kelime_say": {c: dict(kelime_say[c]) for c in kelime_say},
        "toplam_token": toplam_token,
        "sozluk": sozluk,
        "siniflar": list(sinif_say.keys()),
    }


def log_skor(model: dict, metin: str, sinif: str) -> float:
    """log P(C) + Σ log P(w|C)  (çarpım taşmasını önlemek için log)."""
    import math

    V = len(model["sozluk"])
    skor = math.log(model["onsel"][sinif])
    toplam = model["toplam_token"][sinif]
    sayimlar = model["kelime_say"][sinif]
    for w in tokenize(metin):
        # bilinmeyen kelime: sadece sozlukte yoksa yine Laplace ile küçük olasılık
        cnt = sayimlar.get(w, 0)
        p = (cnt + ALPHA) / (toplam + ALPHA * V)
        skor += math.log(p)
    return skor


def tahmin(model: dict, metin: str) -> Tuple[str, Dict[str, float]]:
    import math

    ham = {c: log_skor(model, metin, c) for c in model["siniflar"]}
    # log-skorları kabaca olasılığa çevir (softmax)
    m = max(ham.values())
    exps = {c: math.exp(v - m) for c, v in ham.items()}
    z = sum(exps.values())
    probs = {c: exps[c] / z for c in exps}
    best = max(probs, key=probs.get)  # type: ignore[arg-type]
    return best, probs


def yazdir_model(model: dict) -> None:
    print("Önseller:")
    for c, p in model["onsel"].items():
        print(f"  P({c}) = {p:.3f}")
    print(f"Sözlük boyutu |V| = {len(model['sozluk'])}")
    print("Örnek koşullu sayımlar (spam):")
    for w, n in sorted(model["kelime_say"]["spam"].items(), key=lambda x: -x[1])[:6]:
        print(f"  count('{w}' | spam) = {n}")
    print()


def main() -> None:
    print("Naif Bayes mini — el sayımları (özgün eğitim)\n")
    model = egit(EGITIM)
    yazdir_model(model)

    testler = [
        "bedava kredi kazan",
        "yarın toplantı raporu",
        "hediye tıkla hemen",
        "öğle yemeği notları",
    ]
    print("Tahminler:")
    for t in testler:
        etiket, probs = tahmin(model, t)
        pstr = ", ".join(f"{c}={probs[c]:.3f}" for c in sorted(probs))
        print(f"  '{t}'")
        print(f"    → {etiket}   ({pstr})")
    print()
    print("Not: özellikler (kelimeler) sınıfa göre koşullu bağımsız varsayılır.")


if __name__ == "__main__":
    main()
