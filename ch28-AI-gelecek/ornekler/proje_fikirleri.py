#!/usr/bin/env python3
"""AIMA kısımlarına göre portföy mini proje fikirleri.

Kapsam 1–2 haftalık tutulacak şekilde seçildi. Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import argparse
from typing import Dict, List

Fikir = Dict[str, str]

PROJELER: Dict[str, List[Fikir]] = {
    "I-giris": [
        {
            "ad": "PEAS kart kataloğu",
            "bolum": "ch01–ch02",
            "ozet": "5 farklı ajan için PEAS + ortam özellik tablosu; birini kodla (vakum benzeri).",
        },
    ],
    "II-arama": [
        {
            "ad": "Harita A* görselleştirici",
            "bolum": "ch03–ch04",
            "ozet": "Izgarada A* / açgözlü karşılaştırma; genişleyen sınırı animasyonla göster.",
        },
        {
            "ad": "XOX ötesi: 4x4 veya basit Nim",
            "bolum": "ch05",
            "ozet": "Minimax + alpha-beta; düğüm sayısı metrikleri.",
        },
        {
            "ad": "Harita boyama CSP",
            "bolum": "ch06",
            "ozet": "MRV / forward checking gösteren adım adım debugger.",
        },
    ],
    "III-mantik-plan": [
        {
            "ad": "Wumpus / ızgara KB",
            "bolum": "ch07–ch09",
            "ozet": "Önerme veya basit FOL kurallarıyla güvenli hücre çıkarımı.",
        },
        {
            "ad": "STRIPS oyuncak planlayıcı",
            "bolum": "ch11",
            "ozet": "Bloklar dünyası veya kargo; BFS / ileri arama.",
        },
    ],
    "IV-olasilik-karar": [
        {
            "ad": "Bayes ağı hastalık oyuncağı",
            "bolum": "ch12–ch13",
            "ozet": "3–5 düğümlü ağ; enumeration ile sorgu.",
        },
        {
            "ad": "HMM hava / robot izi",
            "bolum": "ch14",
            "ozet": "Filtre + Viterbi; Ch.26 lokalizasyonla bağ.",
        },
        {
            "ad": "Küçük grid MDP",
            "bolum": "ch16–ch17",
            "ozet": "Değer yineleme; politika haritası ısı haritası.",
        },
    ],
    "V-ogrenme": [
        {
            "ad": "Karar ağacı vs perceptron",
            "bolum": "ch19",
            "ozet": "Aynı toy veri; hata analizi yazısı.",
        },
        {
            "ad": "Numpy MLP XOR+",
            "bolum": "ch21",
            "ozet": "XOR’u geç; küçük bir sınıflandırma setine taşı.",
        },
        {
            "ad": "Q-öğrenme gridworld",
            "bolum": "ch22",
            "ozet": "ε-greedy eğrisi; engel ekle / çıkar ablazyonu.",
        },
    ],
    "VI-dil-goru-robot": [
        {
            "ad": "Mini duygu / spam sınıflandırıcı",
            "bolum": "ch23–ch24",
            "ozet": "BoW taban + basit gömü kosinüs; karışıklık matrisi.",
        },
        {
            "ad": "Kenar + histogram tanıma",
            "bolum": "ch25",
            "ozet": "Sentetik şekiller; konvolüsyon sezgisi raporu.",
        },
        {
            "ad": "Koridor lokalizasyon + potansiyel alan",
            "bolum": "ch26",
            "ozet": "Bu bölüm demolarını birleşik bir ‘robot sim’ CLI yap.",
        },
    ],
    "VII-etik-gelecek": [
        {
            "ad": "Model card + kontrol listesi",
            "bolum": "ch27–ch28",
            "ozet": "Bir projenize Ch.27 listesini uygulayıp kısa model card yazın.",
        },
    ],
}


def yazdir(kisim: str | None) -> None:
    print("Portföy mini proje fikirleri (1–2 haftalık kapsam)\n")
    for k, fikirler in PROJELER.items():
        if kisim and kisim != k:
            continue
        print(f"## {k}")
        for f in fikirler:
            print(f"  • {f['ad']}  [{f['bolum']}]")
            print(f"      {f['ozet']}")
        print()
    print("Seçim ipucu: bir zayıf bölüm + bir güçlü bölüm kombini iyi portföy hikâyesi verir.")
    print("aimacode: https://github.com/aimacode  |  aima: https://aima.cs.berkeley.edu/")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--kisim",
        choices=list(PROJELER.keys()),
        default=None,
        help="Yalnız bir müfredat kısmı",
    )
    args = p.parse_args()
    yazdir(args.kisim)


if __name__ == "__main__":
    main()
