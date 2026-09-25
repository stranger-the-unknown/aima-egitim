#!/usr/bin/env python3
"""Kişisel çalışma yol haritası: AIMA kısımları → modern yığınlar.

Seçilen ilgi alanına göre önerilen bölüm tekrarı + stack notları basar.
Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import argparse
from typing import Dict, List

YOLLAR: Dict[str, Dict] = {
    "arama-planlama": {
        "baslik": "Arama, oyunlar, planlama",
        "aima": ["ch03", "ch04", "ch05", "ch06", "ch11"],
        "modern": [
            "Klasik: ağaç/graf arama, heuristik tasarımı",
            "Oyun: minimax / MCTS fikirleri → oyun AI demoları",
            "Planlama: PDDL / basit STRIPS; hareket planlama (Ch.26 köprüsü)",
        ],
        "sonraki": "Bir gridworld A* + basit oyun ajanı portföyü",
    },
    "olasilik-karar": {
        "baslik": "Olasılık, Bayes, karar, MDP",
        "aima": ["ch12", "ch13", "ch14", "ch16", "ch17", "ch18"],
        "modern": [
            "Bayes ağları / HMM sezgisi → probabilistic programming giriş",
            "Karar teorisi → iş analitiği / risk",
            "MDP / RL köprüsü → Ch.22",
        ],
        "sonraki": "Küçük HMM filtre + bandit / grid MDP notebook",
    },
    "ogrenme": {
        "baslik": "Denetimli, derin, pekiştirmeli öğrenme",
        "aima": ["ch19", "ch20", "ch21", "ch22"],
        "modern": [
            "sklearn ile taban çizgisi",
            "PyTorch / JAX ile minik MLP–CNN",
            "RL: gymnasium tarzı ortam + Q / policy gradient fikri",
        ],
        "sonraki": "Tek veri setinde taban + küçük ağ + hata analizi raporu",
    },
    "dil-goru": {
        "baslik": "Dil ve görü",
        "aima": ["ch23", "ch24", "ch25"],
        "modern": [
            "Klasik NLP: n-gram, BoW → tokenizers",
            "Transformer / gömü sezgisi (API veya küçük model)",
            "Görü: OpenCV temelleri + basit CNN sınıflandırıcı",
        ],
        "sonraki": "Kısa metin sınıflandırıcı + minik görüntü sınıflandırıcı",
    },
    "robotik-ajan": {
        "baslik": "Robotik ve ajan sistemleri",
        "aima": ["ch02", "ch14", "ch17", "ch22", "ch26"],
        "modern": [
            "Simülasyon: basit ızgara / PyBullet giriş (isteğe bağlı)",
            "ROS 2 kavramları (yüksek düzey)",
            "Araç kullanan LLM ajanları: yetki ve güvenlik (Ch.27)",
        ],
        "sonraki": "Lokalizasyon + potansiyel alan demolarını genişlet; güvenlik listesi ekle",
    },
    "etik-urun": {
        "baslik": "Etik, güvenlik, ürünleştirme",
        "aima": ["ch01", "ch27", "ch28"],
        "modern": [
            "Tehdit modeli + gizlilik by design",
            "Değerlendirme kartları / model card fikri",
            "İzleme, geri alma, insan-in-the-loop",
        ],
        "sonraki": "Bir proje için Ch.27 kontrol listesini doldurup README’ye ekle",
    },
}


def yazdir_yol(anahtar: str) -> None:
    y = YOLLAR[anahtar]
    print("=" * 60)
    print(y["baslik"])
    print("=" * 60)
    print("AIMA bölümleri (tekrar / derinleşme):", ", ".join(y["aima"]))
    print("\nModern yığın notları:")
    for m in y["modern"]:
        print(f"  • {m}")
    print(f"\nÖnerilen sonraki adım: {y['sonraki']}")
    print("Resmi kod: https://github.com/aimacode")
    print("Site: https://aima.cs.berkeley.edu/")


def yazdir_hepsi() -> None:
    print("AIMA → modern yığın yetenek haritası\n")
    for k in YOLLAR:
        yazdir_yol(k)
        print()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--yol",
        choices=list(YOLLAR.keys()) + ["hepsi"],
        default="hepsi",
        help="İlgi yolu",
    )
    args = p.parse_args()
    if args.yol == "hepsi":
        yazdir_hepsi()
        print("İpucu: python yetenek_haritasi.py --yol ogrenme")
    else:
        yazdir_yol(args.yol)


if __name__ == "__main__":
    main()
