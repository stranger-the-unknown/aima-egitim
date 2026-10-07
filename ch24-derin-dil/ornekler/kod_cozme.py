#!/usr/bin/env python3
"""Kod çözme: açgözlü arama ve ışın araması (kitaptaki 24.3.2).

Kitaptaki örnek: "The front door is red" İspanyolcaya çevrilirken açgözlü kod çözücü "La" sonrası en olası
sözcük olarak "entrada"yı seçebilir; ama doğru çeviri "La puerta roja" türünden bir sıralama ister ve
"La entrada" ile başlayan hipotezlerin bütün devamları düşük olasılıklıdır, bu yüzden ışından "düşer".
Burada sözcük olasılıkları elle verilen küçük bir koşullu model (bizim varsayımımız) kullanılır.
Hipotezin puanı, sözcüklerin log-olasılıklarının toplamıdır. Kitaba göre günümüz sinirsel çeviri modelleri
4–8 ışın genişliği kullanır; eski istatistiksel modeller 100 ve üzeri.

Çalıştırma:
    python kod_cozme.py
"""
from __future__ import annotations

import math

# P(sonraki sözcük | önceki sözcükler) — elle verilmiş küçük bir model (varsayım). Anahtar: önceki sözcükler.
MODEL = {
    "": {"La": 0.9, "El": 0.1},
    "La": {"entrada": 0.5, "puerta": 0.45, "casa": 0.05},
    "La entrada": {"es": 0.4, "principal": 0.3, "</s>": 0.3},
    "La entrada es": {"roja": 0.3, "rojo": 0.3, "</s>": 0.4},
    "La entrada principal": {"es": 0.5, "</s>": 0.5},
    "La entrada principal es": {"roja": 0.5, "</s>": 0.5},
    "La puerta": {"de": 0.9, "es": 0.1},
    "La puerta de": {"entrada": 0.95, "casa": 0.05},
    "La puerta de entrada": {"es": 0.95, "</s>": 0.05},
    "La puerta de entrada es": {"roja": 0.95, "</s>": 0.05},
    "La puerta es": {"roja": 0.9, "</s>": 0.1},
    "El": {"portal": 0.6, "frente": 0.4},
    "El portal": {"es": 0.5, "</s>": 0.5},
    "El portal es": {"rojo": 0.9, "</s>": 0.1},
}


def sonraki(hipotez: tuple) -> dict:
    return MODEL.get(" ".join(hipotez[1:]), {"</s>": 1.0})


def acgozlu(en_cok: int = 8) -> tuple[list[str], float]:
    h, puan = ("<s>",), 0.0
    while h[-1] != "</s>" and len(h) < en_cok:
        dag = sonraki(h)
        w = max(dag, key=dag.get)
        puan += math.log(dag[w])
        h = h + (w,)
    return list(h[1:]), puan


def isin_aramasi(b: int = 2, en_cok: int = 8) -> tuple[list[str], float]:
    isin = [(0.0, ("<s>",))]
    biten = []
    for _ in range(en_cok):
        adaylar = []
        for puan, h in isin:
            for w, p in sonraki(h).items():
                adaylar.append((puan + math.log(p), h + (w,)))
        adaylar.sort(key=lambda t: -t[0])
        isin = []
        for puan, h in adaylar[:b]:
            (biten if h[-1] == "</s>" else isin).append((puan, h))
        if not isin:
            break
    en = max(biten + isin, key=lambda t: t[0])
    return list(en[1][1:]), en[0]


def main() -> None:
    g, pg = acgozlu()
    print(f"  açgözlü        : {' '.join(g):<40} log P = {pg:.3f}")
    for b in (1, 2, 4):
        s, ps = isin_aramasi(b)
        print(f"  ışın (b = {b})    : {' '.join(s):<40} log P = {ps:.3f}")
    print("  Açgözlü 'La entrada'yı seçer; ışın araması 'La puerta de entrada es roja'yı bulur:")
    print("  Kısa vadede en iyi görünen sözcük, bütün cümle için en iyi seçim olmayabilir.")


if __name__ == "__main__":
    main()
