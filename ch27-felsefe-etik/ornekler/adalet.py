#!/usr/bin/env python3
"""Adalet ve yanlılık (kitaptaki 27.3.3). Bütün veriler yapaydır.

* İyi kalibre edilmiş bir risk puanı (aynı puanı alanların gerçek oranı gruptan bağımsız) ile fırsat eşitliği
  (yanlış pozitif / yanlış negatif oranlarının gruplar arasında eşit olması) taban oranlar farklıysa birlikte
  sağlanamaz (Kleinberg vd., 2016). COMPAS tartışması bu gerilimdir.
* Farkında olmayarak adalet: Korunan özniteliği silmek yetmez; model onu ilişkili bir vekilden (posta kodu)
  yeniden çıkarabilir — özellikle geçmişteki yanlı kararlarla etiketlenmiş veride.
* Örneklem boyu dengesizliği: Kısıtlı bir model (doğrusal regresyon) ortalama hatayı küçültmek için çoğunluğa
  uyar; azınlıkta hata büyük olur. Yeniden ağırlıklandırma (ya da azınlıktan fazla örnekleme) dengeyi değiştirir.

Çalıştırma:
    python adalet.py
"""
from __future__ import annotations

import numpy as np


# --- Kalibrasyon ve fırsat eşitliği ----------------------------------------------------------------
def kalibre_veri(n: int = 200_000, taban=(0.3, 0.5), tohum: int = 0):
    """Her kişinin gerçek riski r ~ Beta (grup ortalaması taban oran); puan = r (tam kalibre); y ~ Bernoulli(r).
    (grup, puan, sonuç)."""
    rng = np.random.default_rng(tohum)
    grup = rng.integers(0, 2, n)
    m = np.where(grup == 0, taban[0], taban[1])
    k = 4.0                                          # Beta(k·m, k·(1 − m)): ortalama m
    puan = rng.beta(k * m, k * (1 - m))
    y = (rng.random(n) < puan).astype(int)
    return grup, puan, y


def grup_olcutleri(grup, puan, y, esik) -> dict:
    """esik: tek sayı ya da (A eşiği, B eşiği). Her grup için oranlar."""
    esikler = (esik, esik) if np.isscalar(esik) else esik
    sonuc = {}
    for g, ad in ((0, "A"), (1, "B")):
        s, yy = puan[grup == g], y[grup == g]
        yuksek = s > esikler[g]
        bin_ = (s > 0.6) & (s <= 0.7)
        sonuc[ad] = {
            "taban oran": yy.mean(),
            "yüksek riskli oranı": yuksek.mean(),
            "yanlış pozitif": yuksek[yy == 0].mean(),
            "yanlış negatif": (~yuksek)[yy == 1].mean(),
            "puan 0.6–0.7 iken gerçek oran": yy[bin_].mean(),
            "yüksek riskli denenlerin gerçek oranı": yy[yuksek].mean(),
        }
    return sonuc


def esit_yp_esikleri(grup, puan, y, hedef_yp: float) -> tuple[float, float]:
    """Her grupta yanlış pozitif oranı hedef_yp olacak eşik."""
    return tuple(float(np.quantile(puan[(grup == g) & (y == 0)], 1 - hedef_yp)) for g in (0, 1))


# --- Farkında olmayarak adalet ----------------------------------------------------------------------
def lojistik(X: np.ndarray, y: np.ndarray, adim: int = 2000, ogrenme: float = 0.5) -> np.ndarray:
    Xb = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(Xb.shape[1])
    for _ in range(adim):
        p = 1 / (1 + np.exp(-Xb @ w))
        w -= ogrenme * Xb.T @ (p - y) / len(y)
    return w


def tahmin(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.hstack([X, np.ones((len(X), 1))]) @ w))


def farkinda_olmama(n: int = 20_000, tohum: int = 0) -> dict:
    """Gerçek geri ödeme yeteneği x her iki grupta aynı dağılımlı. Geçmiş onay kararları B grubunu cezalandırmış
    (yanlı etiket). Vekil z (posta kodu) grupla güçlü ilişkili. Onay oranları (A, B)."""
    rng = np.random.default_rng(tohum)
    grup = rng.integers(0, 2, n)
    x = rng.normal(0, 1, n)
    z = (rng.random(n) < np.where(grup == 1, 0.8, 0.2)).astype(float)
    y = (x - 1.0 * grup + rng.normal(0, 0.5, n) > 0).astype(float)     # geçmişteki yanlı kararlar
    sonuc = {}
    for ad, X in (("x + grup", np.stack([x, grup], 1)), ("x + posta kodu (grup silindi)", np.stack([x, z], 1)),
                  ("yalnızca x", x[:, None])):
        onay = tahmin(lojistik(X, y), X) > 0.5
        sonuc[ad] = (float(onay[grup == 0].mean()), float(onay[grup == 1].mean()))
    return sonuc


# --- Örneklem boyu dengesizliği ------------------------------------------------------------------------
def orneklem_dengesizligi(n: int = 10_000, azinlik: float = 0.05, tohum: int = 0) -> dict:
    """Çoğunlukta y = x, azınlıkta y = 1 − x (+ gürültü). Tek doğrusal model. Grup başına ortalama kare hata."""
    rng = np.random.default_rng(tohum)
    grup = (rng.random(n) < azinlik).astype(int)
    x = rng.uniform(0, 1, n)
    y = np.where(grup == 0, x, 1 - x) + rng.normal(0, 0.05, n)
    X = np.stack([x, np.ones(n)], 1)
    sonuc = {}
    for ad, agirlik in (("ağırlıksız", np.ones(n)), ("gruplar eşit ağırlıklı", np.where(grup == 1, (1 - azinlik) / azinlik, 1.0))):
        W = np.sqrt(agirlik)[:, None]
        w = np.linalg.lstsq(X * W, y * W.ravel(), rcond=None)[0]
        hata = (X @ w - y) ** 2
        sonuc[ad] = (float(hata[grup == 0].mean()), float(hata[grup == 1].mean()))
    Xg = np.stack([x, np.ones(n), x * grup, grup], 1)                       # gruba özgü eğim ve sabit
    w = np.linalg.lstsq(Xg, y, rcond=None)[0]
    hata = (Xg @ w - y) ** 2
    sonuc["gruba özgü model"] = (float(hata[grup == 0].mean()), float(hata[grup == 1].mean()))
    return sonuc


def main() -> None:
    print("=== Kalibrasyon ve fırsat eşitliği (taban oranlar A: 0.3, B: 0.5; tek eşik 0.5) ===")
    g, s, y = kalibre_veri()
    o = grup_olcutleri(g, s, y, 0.5)
    for k in o["A"]:
        print(f"  {k:<38}: A {o['A'][k]:.3f}   B {o['B'][k]:.3f}")
    print("  Puan iki grupta da kalibre; ama B'de suç işlemeyenlerin çok daha büyük bir kısmı 'yüksek riskli' sayılıyor.")

    e = esit_yp_esikleri(g, s, y, 0.15)
    o = grup_olcutleri(g, s, y, e)
    print(f"\n  Yanlış pozitifleri eşitlemek için grup eşikleri: A {e[0]:.3f}, B {e[1]:.3f}")
    for k in ("yanlış pozitif", "yanlış negatif", "yüksek riskli denenlerin gerçek oranı"):
        print(f"  {k:<38}: A {o['A'][k]:.3f}   B {o['B'][k]:.3f}")
    print("  Hata oranları artık yakın; ama aynı puanı alan iki kişi gruplarına göre farklı karar alıyor ve")
    print("  'yüksek riskli' etiketi gruplarda farklı gerçek oranlara karşılık geliyor: Kararın kalibrasyonu bozuldu.")

    print("\n=== Farkında olmayarak adalet (yanlı geçmiş kararlarla eğitim) — onay oranları ===")
    for ad, (a, b) in farkinda_olmama().items():
        print(f"  {ad:<30}: A %{100 * a:4.1f}   B %{100 * b:4.1f}")
    print("  Grup sütununu silmek farkı küçültür ama gidermez: model posta kodunu vekil olarak kullanır.")

    print("\n=== Örneklem boyu dengesizliği (azınlık %5) — grup başına ortalama kare hata ===")
    for ad, (a, b) in orneklem_dengesizligi().items():
        print(f"  {ad:<24}: çoğunluk {a:.4f}   azınlık {b:.4f}")


if __name__ == "__main__":
    main()
