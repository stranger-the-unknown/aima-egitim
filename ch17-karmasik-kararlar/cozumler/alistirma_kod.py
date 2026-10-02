#!/usr/bin/env python3
"""Bölüm 17 alıştırmaları: kodlu çözümler (A2, A4, A5, A7, A8, A9, A10).

Çalıştırma (bölüm klasöründen):
    python cozumler/alistirma_kod.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ornekler"))

import dort_uc_dunya as d43  # noqa: E402
import haydut  # noqa: E402
import mdp  # noqa: E402
import pomdp  # noqa: E402


# --- A2: indirim ---------------------------------------------------------------
def a2() -> dict:
    """10 adımda +1'e varan geçmiş: 9 geçiş −0.04, 10. geçiş +1."""
    odul = [-0.04] * 9 + [1.0]
    return {f"γ = {g}": sum(g ** t * r for t, r in enumerate(odul)) for g in (1.0, 0.9, 0.5)}


# --- A4: dokuz politika ------------------------------------------------------------
def a4() -> list:
    return d43.kirilma_noktalari()


# --- A5: sonlu ufukta (3, 1) ---------------------------------------------------------
def a5(N: int = 60) -> dict:
    """Kalan adım sayısına göre (3, 1)'deki en iyi eylem; Sol'un en iyi olmaya başladığı ilk ufuk."""
    pol = d43.sonlu_ufuk(mdp.dort_uc(), N)
    eylemler = {k: pol[k - 1][(3, 1)] for k in range(1, N + 1)}
    ilk_sol = next(k for k, a in eylemler.items() if a == "Sol")
    return {"eylemler": eylemler, "ilk_sol": ilk_sol}


# --- A7: potansiyele dayanmayan "yaklaşma ödülü" ------------------------------------
def uzaklik(s) -> int:
    return abs(4 - s[0]) + abs(3 - s[1])


def yaklasma_odulu(m: mdp.MDP, bonus: float = 0.2) -> mdp.MDP:
    """Hedefe (4, 3) yaklaşan her geçişe +bonus; uzaklaşmaya ceza yok (potansiyele dayanmıyor)."""
    eski = m.odul
    return mdp.MDP(m.durumlar, m.eylemler, m.gecis,
                   lambda s, a, s2: eski(s, a, s2) + (bonus if uzaklik(s2) < uzaklik(s) else 0.0),
                   m.gama, m.uclar)


def a7(gama: float = 0.99) -> dict:
    m = mdp.dort_uc(gama=gama)
    U, _ = mdp.deger_yineleme(m, eps=1e-9)
    asil = m.acgozlu(U)
    kotu = yaklasma_odulu(m)
    U_k, _ = mdp.deger_yineleme(kotu, eps=1e-9)
    Phi = {s: (0.0 if s in m.uclar else -0.2 * uzaklik(s)) for s in m.durumlar}   # uçlarda Φ = 0 olmalı
    iyi = d43.sekillendir(m, Phi)
    U_i, _ = mdp.deger_yineleme(iyi, eps=1e-9)
    # Yaklaşma ödüllü politikayla (1, 1)'den başlayınca 1000 adımda bir uca varma olasılığı
    pi_k = kotu.acgozlu(U_k)
    dagilim = {(1, 1): 1.0}
    for _ in range(1000):
        yeni = {}
        for s, p in dagilim.items():
            for q, s2 in ([(1.0, s)] if s in m.uclar else m.gecis[(s, pi_k[s])]):
                yeni[s2] = yeni.get(s2, 0.0) + p * q
        dagilim = yeni
    return {
        "yaklaşma ödülüyle politika aynı mı": pi_k == asil,
        "yaklaşma ödülüyle U(1,1)": U_k[(1, 1)],
        "yaklaşma ödülüyle 1000 adımda uca varma olasılığı": sum(dagilim.get(s, 0.0) for s in m.uclar),
        "potansiyelle (Φ = −0.2 · uzaklık) politika aynı mı": iyi.acgozlu(U_i) == asil,
        "asıl U(1,1)": U[(1, 1)],
        "asıl politika": asil,
        "yaklaşma ödüllü politika": pi_k,
    }


# --- A8: Gittins indeksleri -----------------------------------------------------------
def a8() -> dict:
    g1, _ = haydut.deterministik_gittins([1, 0, 0, 10], 0.8)
    bern = {(s, f): (s / (s + f), haydut.bernoulli_gittins(s, f)) for s, f in ((2, 1), (4, 2), (8, 4), (16, 8))}
    return {"Gittins(1, 0, 0, 10; γ = 0.8)": g1, "Bernoulli": bern}


# --- A9: 4 × 3 POMDP'de inanç güncellemesi ---------------------------------------------
def duvar_sayisi(s) -> int:
    return sum(mdp.hareket(s, yon) == s for yon in mdp.YONLER)


def duvar_bitleri(s) -> tuple:
    """Kuzey, Güney, Doğu, Batı yönlerinde duvar (ya da engel) var mı?"""
    return tuple(mdp.hareket(s, yon) == s for yon in ("Yukarı", "Aşağı", "Sağ", "Sol"))


def a9(dogruluk: float = 0.9, eps: float = 0.1) -> dict:
    """Düzgün inançtan (9 uç olmayan durum) Sol yap, sonra algıla. İki algılayıcı:
    (a) komşu duvar SAYISI (1 ya da 2), dogruluk olasılıkla doğru; gözlem '1 duvar'.
    (b) 4 bitlik algılayıcı (kitap s. 476): her yöndeki duvarı ayrı ayrı, her bit ε olasılıkla yanlış;
        gözlem 'yalnızca güneyde duvar'."""
    m = mdp.dort_uc()
    tahmin = {s: 0.0 for s in m.durumlar}
    for s in m.durumlar:
        if s not in m.uclar:
            for q, s2 in m.gecis[(s, "Sol")]:
                tahmin[s2] += q / 9

    def guncelle(P_e):
        ham = {s: (0.0 if s in m.uclar else P_e(s)) * tahmin[s] for s in m.durumlar}  # uca düşen algılamaz
        z = sum(ham.values())
        return {s: v / z for s, v in ham.items() if v > 0}

    gozlem = (False, True, False, False)
    return {
        "duvar sayıları": {s: duvar_sayisi(s) for s in m.durumlar if s not in m.uclar},
        "sayı algılayıcısı": guncelle(lambda s: dogruluk if duvar_sayisi(s) == 1 else 1 - dogruluk),
        "4 bit algılayıcı": guncelle(lambda s: math.prod(
            1 - eps if bit == g else eps for bit, g in zip(duvar_bitleri(s), gozlem))),
    }


# --- A10: algılayıcı doğruluğu ve bilginin değeri ------------------------------------------
def a10(derinlik: int = 8) -> dict:
    sonuc, eski = {}, pomdp.DOGRULUK
    try:
        for dogruluk in (0.5, 0.6, 0.9, 1.0):
            pomdp.DOGRULUK = dogruluk
            U = pomdp.deger_yineleme(derinlik)[-1]
            sonuc[dogruluk] = {bB: pomdp.fayda(U, bB)[0] for bB in (0.0, 0.5, 1.0)}
    finally:
        pomdp.DOGRULUK = eski
    return sonuc


def main() -> None:
    print("=== A2: 10 adımlık geçmişin faydası ===")
    for k, v in a2().items():
        print(f"  {k}: {v:.4f}")

    print("\n=== A4: r < 0 için en iyi politikalar ===")
    noktalar = a4()
    print(f"  Kırılma noktaları: {[n for n, _ in noktalar]}  →  {len(noktalar) + 1} politika")

    print("\n=== A5: sonlu ufukta (3, 1) ===")
    s = a5()
    print("  " + ", ".join(f"{k}: {a}" for k, a in list(s["eylemler"].items())[:16]))
    print(f"  Sol ilk kez {s['ilk_sol']} adım kalınca en iyi oluyor.")

    print("\n=== A7: potansiyele dayanmayan yaklaşma ödülü (γ = 0.99) ===")
    s = a7()
    for k in list(s)[:5]:
        v = s[k]
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")
    print("  Asıl politika:")
    print(mdp.ciz(pi=s["asıl politika"], girinti="      "))
    print("  Yaklaşma ödüllü politika:")
    print(mdp.ciz(pi=s["yaklaşma ödüllü politika"], girinti="      "))

    print("\n=== A8: Gittins indeksleri ===")
    s = a8()
    print(f"  1, 0, 0, 10, 0, ... (γ = 0.8): {s['Gittins(1, 0, 0, 10; γ = 0.8)']:.4f}")
    for (sb, fb), (tahmin, g) in s["Bernoulli"].items():
        print(f"  Bernoulli ({sb:>2}, {fb:>2}): tahmin {tahmin:.4f}, Gittins {g:.4f}, keşif bonusu {g - tahmin:.4f}")

    print("\n=== A9: 4 × 3 POMDP, düzgün inanç + Sol ===")
    s = a9()
    print(f"  Komşu duvar sayısı: {s['duvar sayıları']}")
    for ad, gozlem in (("sayı algılayıcısı", "'1 duvar', doğruluk 0.9"), ("4 bit algılayıcı", "'yalnızca güneyde duvar', ε = 0.1")):
        en_olasi = sorted(s[ad].items(), key=lambda x: -x[1])[:4]
        print(f"  {ad} ({gozlem}): " + ", ".join(f"{st}: {v:.3f}" for st, v in en_olasi))

    print("\n=== A10: algılayıcı doğruluğu ve U(b), derinlik 8 ===")
    for dogruluk, u in a10().items():
        print(f"  doğruluk {dogruluk}: U(b(B)=0) = {u[0.0]:.3f}, U(0.5) = {u[0.5]:.3f}, U(1) = {u[1.0]:.3f}")


if __name__ == "__main__":
    main()
