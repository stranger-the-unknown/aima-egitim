#!/usr/bin/env python3
"""Bölüm 27 alıştırmaları: kodlu çözümler (A3–A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import adalet as ad  # noqa: E402
import guvenlik as gv  # noqa: E402
import mahremiyet as mh  # noqa: E402


# --- A3: yeniden tanımlama -------------------------------------------------------------------------
def a3() -> dict:
    sonuc = {}
    for n in (1_000, 10_000, 100_000):
        T = mh.yapay_nufus(n)
        K = 365 * 80 * 2                                   # olası (doğum günü, cinsiyet) çifti
        sonuc[n] = (round(mh.tekil_oran(T), 3), round(math.exp(-(n - 1) / K), 3), mh.k_degeri(mh.genellestir(T, 365)))
    return sonuc


# --- A4: diferansiyel mahremiyet ------------------------------------------------------------------------
def a4() -> dict:
    sonuc = {"maaş": mh.fark_saldirisi(81_234, 12, 81_199, 13)}
    for eps in (0.1, 0.5, 1.0, 2.0, 5.0):
        sonuc[eps] = (round(mh.sayim_fark_saldirisi(eps), 3), round(math.exp(eps) / (1 + math.exp(eps)), 3))
    return sonuc


# --- A5: güvenli toplama ve ayrılan kullanıcı -------------------------------------------------------------
def a5() -> dict:
    rng = np.random.default_rng(3)
    P = rng.normal(0, 1, (4, 2))
    maskeli, toplam = mh.guvenli_toplama(P)
    eksik = maskeli[:3].sum(axis=0)                        # 4. kullanıcı yanıt vermedi
    return {"gerçek toplam (ilk 3)": P[:3].sum(axis=0).round(3), "maskeli toplam (ilk 3)": eksik.round(1),
            "tam toplam doğru": bool(np.allclose(toplam, P.sum(axis=0)))}


# --- A6: taban oranlar ve imkânsızlık ----------------------------------------------------------------------
def a6() -> dict:
    sonuc = {}
    for taban in ((0.3, 0.3), (0.3, 0.5), (0.2, 0.6)):
        g, s, y = ad.kalibre_veri(taban=taban, n=100_000)
        o = ad.grup_olcutleri(g, s, y, 0.5)
        sonuc[taban] = {k: (round(float(o["A"][k]), 3), round(float(o["B"][k]), 3))
                        for k in ("yanlış pozitif", "yanlış negatif", "puan 0.6–0.7 iken gerçek oran")}
    return sonuc


# --- A7: vekilin gücü -------------------------------------------------------------------------------------
def vekil_deneyi(guc: float, n: int = 20_000, tohum: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(tohum)
    grup = rng.integers(0, 2, n)
    x = rng.normal(0, 1, n)
    z = (rng.random(n) < np.where(grup == 1, guc, 1 - guc)).astype(float)
    y = (x - 1.0 * grup + rng.normal(0, 0.5, n) > 0).astype(float)
    X = np.stack([x, z], 1)
    onay = ad.tahmin(ad.lojistik(X, y, adim=1000), X) > 0.5
    return float(onay[grup == 0].mean()), float(onay[grup == 1].mean())


def a7() -> dict:
    return {guc: tuple(round(v, 3) for v in vekil_deneyi(guc)) for guc in (0.5, 0.8, 0.95)}


# --- A8: azınlık payı ----------------------------------------------------------------------------------------
def a8() -> dict:
    return {pay: tuple(round(v, 4) for v in ad.orneklem_dengesizligi(azinlik=pay)["ağırlıksız"])
            for pay in (0.01, 0.05, 0.2, 0.5)}


# --- A9: düşük etki eşiği ve şartname oyunu ------------------------------------------------------------------
def a9() -> dict:
    esik = {lam: gv.dusuk_etkili_yol(lam)[1:] for lam in (1.5, 2.5, 3.0)}
    oyun = {g: gv.calistir(gv.en_iyi_politika("temizlenen kir başına +1", gamma=g), adim=8) for g in (0.0, 0.95)}
    return {"düşük etki": esik, "şartname oyunu": oyun}


# --- A10: sorma eşiği ------------------------------------------------------------------------------------------
def sorma_esigi(insan_dogrulugu: float, adim: int = 100_000) -> float:
    """'Uygula'nın 'sor'dan iyi olmaya başladığı en küçük p (ızgara üzerinde)."""
    for p in np.linspace(0.5, 1.0, adim):
        r = gv.sor_ya_da_uygula(p, insan_dogrulugu=insan_dogrulugu)
        if r["uygula"] >= r["sor"]:
            return float(p)
    return 1.0


def a10() -> dict:
    return {q: round(sorma_esigi(q), 4) for q in (1.0, 0.95, 0.8)} | {"tekillik": gv.tekillik_hizi()}


def main() -> None:
    print("=== A3: tek başına kalan kayıtlar (bir posta kodu) ===")
    for n, (gozlem, kuram, k) in a3().items():
        print(f"  n = {n:>7}: gözlenen {gozlem}, e^(−n/K) ≈ {kuram}; yalnızca doğum yılı tutulunca k = {k}")

    print("\n=== A4: fark saldırısı ve ε ===")
    r = a4()
    print(f"  maaş: {r.pop('maaş'):.0f}")
    for eps, (basari, sinir) in r.items():
        print(f"  ε = {eps:>3}: saldırının başarısı {basari}, kuramsal üst sınır e^ε/(1 + e^ε) = {sinir}")

    print("\n=== A5: güvenli toplama ===")
    for k, v in a5().items():
        print(f"  {k}: {v}")

    print("\n=== A6: taban oranlar (A, B) → (A, B) değerleri ===")
    for taban, d in a6().items():
        print(f"  {taban}: " + "; ".join(f"{k} {v}" for k, v in d.items()))

    print("\n=== A7: vekilin gücü P(z = 1 | B) → onay oranları (A, B) ===")
    for guc, v in a7().items():
        print(f"  {guc}: {v}")

    print("\n=== A8: azınlık payı → ağırlıksız modelde (çoğunluk, azınlık) hata ===")
    for pay, v in a8().items():
        print(f"  %{100 * pay:.0f}: {v}")

    print("\n=== A9 ===")
    r = a9()
    for lam, (adim, bozuk) in r["düşük etki"].items():
        print(f"  λ = {lam}: {adim} adım, bozulan {bozuk or 'yok'}")
    for g, iz in r["şartname oyunu"].items():
        print(f"  γ = {g}: {' '.join(iz)}")

    print("\n=== A10 ===")
    for k, v in a10().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
