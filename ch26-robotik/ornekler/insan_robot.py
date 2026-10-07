#!/usr/bin/env python3
"""İnsanlar ve robotlar; tepkisel denetim (kitaptaki 26.8, 26.9).

* İnsan eylemini tahmin: İnsan amacına göre "gürültülü olarak en iyi" davranır:
  P(u_H | x, J_H) ∝ exp(−Q(x, u_H; J_H))   (26.8)
  Gözlenen her eylem amaç hakkındaki inancı günceller: b′(J_H) ∝ b(J_H) P(u_H | x, J_H)   (26.9)
* Taklit öğrenmesi (davranış klonlama) ve DAGGER: Yalnızca uzmanın gösterdiği durumlardan öğrenen politika,
  küçük hatalarla gösterilmemiş durumlara kayar ve oradan dönmeyi bilmez (ALVINN'deki sorun). DAGGER, öğrenilen
  politikanın ziyaret ettiği durumlar için uzmandan etiket toplar ve bütün veriyle yeniden eğitir.
* Tepkisel denetim: altı bacaklı robotun bir bacağını yöneten artırılmış sonlu durum makinesi (Şekil 26.32b):
  ileri salınımda takılırsa geri çek, daha yükseğe kaldır, yeniden dene. Üçlü yürüyüşte her an yerdeki üç ayak
  gövde merkezini içeren bir üçgen oluşturur (statik kararlılık).

Çalıştırma:
    python insan_robot.py
"""
from __future__ import annotations

import math

import numpy as np

# --- Amaç çıkarımı ---------------------------------------------------------------------------------
AMACLAR = {"mutfak": (0.0, 8.0), "pencere": (8.0, 8.0), "koridor": (0.0, 0.0)}
EYLEMLER = [(math.cos(a), math.sin(a)) for a in np.radians(np.arange(0, 360, 45))]


def q_degeri(x, u, amac) -> float:
    """Q(x, u; J): bir adımın maliyeti (1) + vardığın yerden amaca kalan uzaklık."""
    return 1.0 + math.dist((x[0] + u[0], x[1] + u[1]), amac)


def eylem_olasiliklari(x, amac, beta: float = 1.0) -> np.ndarray:
    """P(u | x, J) ∝ exp(−β Q). Kitaptaki denklemde β = 1; β büyüdükçe insan daha 'akılcı' varsayılır."""
    q = np.array([q_degeri(x, u, amac) for u in EYLEMLER])
    p = np.exp(-beta * (q - q.min()))
    return p / p.sum()


def inanc_guncelle(inanc: dict, x, u_indeks: int, beta: float = 1.0) -> dict:
    yeni = {a: b * eylem_olasiliklari(x, AMACLAR[a], beta)[u_indeks] for a, b in inanc.items()}
    z = sum(yeni.values())
    return {a: v / z for a, v in yeni.items()}


def amac_cikarimi(x0=(4.0, 3.0), eylemler=(1, 1, 1, 2, 1), beta: float = 1.0) -> list[dict]:
    """İnsan (4, 3)'ten çıkıp sırasıyla verilen yönlerde (indeks: 0 = doğu, 1 = kuzeydoğu, 2 = kuzey …) yürür."""
    inanc = {a: 1 / len(AMACLAR) for a in AMACLAR}
    x = x0
    gecmis = [dict(inanc)]
    for k in eylemler:
        inanc = inanc_guncelle(inanc, x, k, beta)
        x = (x[0] + EYLEMLER[k][0], x[1] + EYLEMLER[k][1])
        gecmis.append(dict(inanc))
    return gecmis


def sonraki_eylem_tahmini(x, inanc: dict, beta: float = 1.0) -> np.ndarray:
    """P(u_H | x) = Σ_J P(u_H | x, J) b(J): amaçlar üzerinden marjinalleştirme."""
    return sum(b * eylem_olasiliklari(x, AMACLAR[a], beta) for a, b in inanc.items())


# --- Davranış klonlama ve DAGGER ---------------------------------------------------------------------
RUZGAR = 0.3          # her adımda aracı yana iten sabit yan rüzgâr
SERIT = 0.5           # |y| > 0.5: şeritten çıktı


def uzman(y: np.ndarray) -> np.ndarray:
    """Uzman sürücü: rüzgârı karşılar ve sapmayı düzeltir."""
    return -RUZGAR - 0.5 * y


def surus(politika, adim: int, rng, gurultu: float = 0.05, y0: float = 0.0):
    """y_{t+1} = y_t + u_t + rüzgâr + gürültü. (ziyaret edilen durumlar, şeritten çıktı mı)."""
    y, durumlar = y0, []
    for _ in range(adim):
        durumlar.append(y)
        y = y + float(politika(np.array([y]))[0]) + RUZGAR + rng.normal(0, gurultu)
        if abs(y) > SERIT:
            return durumlar, True
    return durumlar, False


def dogrusal_politika(Y: np.ndarray, U: np.ndarray, ridge: float = 1e-6):
    """u = a·y + b, en küçük kareler (küçük ridge ile)."""
    X = np.stack([Y, np.ones_like(Y)], axis=1)
    a, b = np.linalg.solve(X.T @ X + ridge * np.eye(2), X.T @ U)
    return (lambda y: a * y + b), (float(a), float(b))


def cikma_orani(politika, rng, deneme: int = 200, adim: int = 100) -> float:
    return float(np.mean([surus(politika, adim, rng)[1] for _ in range(deneme)]))


def klonlama_ve_dagger(tur: int = 3, tohum: int = 0) -> dict:
    rng = np.random.default_rng(tohum)
    # Uzman gösterimi gürültüsüz ve tam şerit ortasında: bütün durumlar y = 0.
    Y = np.zeros(50)
    U = uzman(Y)
    pi, katsayi = dogrusal_politika(Y, U)
    sonuc = {"klonlama": (katsayi, cikma_orani(pi, rng))}
    for k in range(1, tur + 1):
        yeni = []
        for _ in range(20):
            durumlar, _ = surus(pi, 100, rng)
            yeni.extend(durumlar)
        Y = np.concatenate([Y, yeni])
        U = np.concatenate([U, uzman(np.array(yeni))])           # uzman, politikanın gittiği yerleri etiketler
        pi, katsayi = dogrusal_politika(Y, U)
        sonuc[f"DAGGER {k}"] = (katsayi, cikma_orani(pi, rng))
    return sonuc


# --- Tepkisel bacak denetçisi ve üçlü yürüyüş -----------------------------------------------------------
def bacak_afsm(engeller: list[float], baslangic_yukseklik: float = 1.0, artis: float = 1.0) -> list[tuple]:
    """Her adım için (engel yüksekliği, deneme sayısı, son kaldırma yüksekliği, durum izi).
    S1: geri it (destek) → S2: kaldır → S3: ileri salla (takılırsa: geri çek, daha yükseğe kaldır, S3) → S4: indir."""
    sonuc = []
    for engel in engeller:
        h, deneme, iz = baslangic_yukseklik, 0, ["S1", "S2"]
        while True:
            deneme += 1
            iz.append("S3")
            if h > engel:                    # salınım engelin üstünden geçti
                break
            iz.append("takıldı")
            h += artis
        iz.append("S4")
        sonuc.append((engel, deneme, h, "→".join(iz)))
    return sonuc


AYAKLAR = {"SolÖn": (-1.0, 1.0), "SolOrta": (-1.2, 0.0), "SolArka": (-1.0, -1.0),
           "SağÖn": (1.0, 1.0), "SağOrta": (1.2, 0.0), "SağArka": (1.0, -1.0)}


def merkez_destekte_mi(yerdeki: list[str], merkez=(0.0, 0.0)) -> bool:
    """Gövde merkezi yerdeki ayakların oluşturduğu üçgenin içinde (sınır hariç) mi?"""
    a, b, c = (AYAKLAR[k] for k in yerdeki)
    def isaret(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    d1, d2, d3 = isaret(a, b, merkez), isaret(b, c, merkez), isaret(c, a, merkez)
    return (d1 > 0 and d2 > 0 and d3 > 0) or (d1 < 0 and d2 < 0 and d3 < 0)


def main() -> None:
    print("=== Amaç çıkarımı (26.8–26.9): insan (4, 3)'ten kuzeydoğuya yürüyor ===")
    yonler = ("doğu", "kuzeydoğu", "kuzey", "kuzeybatı", "batı", "güneybatı", "güney", "güneydoğu")
    for k, b in enumerate(amac_cikarimi()):
        print(f"  {k} adım sonra: " + ", ".join(f"{a} {p:.2f}" for a, p in b.items()))
    son = amac_cikarimi()[-1]
    x = (4.0 + sum(EYLEMLER[k][0] for k in (1, 1, 1, 2, 1)), 3.0 + sum(EYLEMLER[k][1] for k in (1, 1, 1, 2, 1)))
    t = sonraki_eylem_tahmini(x, son)
    print(f"  Bir sonraki eylem için en olası: {yonler[int(np.argmax(t))]} ({t.max():.2f})")

    print("\n=== Davranış klonlama ve DAGGER (yan rüzgârlı şeritte kalma) ===")
    for ad, ((a, b), oran) in klonlama_ve_dagger().items():
        print(f"  {ad:<10}: u = {a:+.2f}·y {b:+.2f};  100 adımda şeritten çıkma oranı %{100 * oran:.0f}")
    print("  Gösterimde hiç sapma olmadığı için klonlanan politika düzeltmeyi öğrenmez (eğim ≈ 0);")
    print("  DAGGER, politikanın kendi ziyaret ettiği durumlarda uzmana sorar ve eğimi (−0.5) öğrenir.")

    print("\n=== Tepkisel bacak denetçisi (AFSM) ===")
    for engel, deneme, h, iz in bacak_afsm([0.0, 2.5, 0.5, 4.2]):
        print(f"  engel {engel}: {deneme} deneme, son yükseklik {h}  [{iz}]")

    print("\n=== Statik kararlılık ===")
    for ad, yer in (("üçlü yürüyüş, faz 1", ["SağÖn", "SağArka", "SolOrta"]),
                    ("üçlü yürüyüş, faz 2", ["SolÖn", "SolArka", "SağOrta"]),
                    ("yalnızca sol ayaklar yerde", ["SolÖn", "SolOrta", "SolArka"])):
        print(f"  {ad:<27}: merkez destek üçgeninde mi? {merkez_destekte_mi(yer)}")


if __name__ == "__main__":
    main()
