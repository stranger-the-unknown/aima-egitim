#!/usr/bin/env python3
"""Konfigürasyon uzayı ve hareket planlama (kitaptaki 26.5.1, 26.5.2).

* C-uzayı engeli: C_obs = {q : A(q) ∩ O ≠ ∅}. Dönemeyen üçgen robot ve dikdörtgen engel için bu, engel ile
  robotun ters çevrilmiş biçiminin Minkowski toplamıdır: beş kenarlı bir çokgen (Şekil 26.11).
* İki eklemli kol: ileri kinematik φ(θ_omuz, θ_dirsek) ve ters kinematik (iki çözüm: dirsek yukarı/aşağı).
  İş uzayındaki basit bir dikey engel C-uzayında karmaşık bir biçim alır; C-uzayını açıkça kurmak yerine
  çarpışma denetleyicisiyle yoklarız (Şekil 26.12, 26.16).
* Izgara (hücre ayrıştırma) + en kısa yol: değer fonksiyonu = hedefe en kısa yolun maliyeti.
* Görünürlük çizgesi: çokgen engellerde en kısa yolu garanti eder (Şekil 26.14).
* Olasılıksal yol haritası (PRM, k-PRM) ve çift yönlü RRT + kısaltma (Şekil 26.17–26.19).
* Yörünge optimizasyonu: J = J_eff + λ J_obs, gradyan inişi; yalnızca J_eff için en iyi yol doğrudur (Şekil 26.20).

Çalıştırma:
    python hareket_planlama.py
"""
from __future__ import annotations

import heapq
import math

import numpy as np


# --- Yardımcılar ----------------------------------------------------------------------------------
def dis_kabuk(noktalar) -> list[tuple[float, float]]:
    """Andrew'un monoton zincir algoritması; saat yönünün tersine dış bükey kabuk."""
    P = sorted(set(map(tuple, noktalar)))
    capraz = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])  # noqa: E731
    alt, ust = [], []
    for p in P:
        while len(alt) >= 2 and capraz(alt[-2], alt[-1], p) <= 0:
            alt.pop()
        alt.append(p)
    for p in reversed(P):
        while len(ust) >= 2 and capraz(ust[-2], ust[-1], p) <= 0:
            ust.pop()
        ust.append(p)
    return alt[:-1] + ust[:-1]


def cokgen_alani(K) -> float:
    return 0.5 * abs(sum(K[i][0] * K[(i + 1) % len(K)][1] - K[(i + 1) % len(K)][0] * K[i][1] for i in range(len(K))))


def icinde_mi(nokta, K) -> bool:
    """Dış bükey, saat yönünün tersine sıralı çokgenin (kenarı dahil) içinde mi?"""
    x, y = nokta
    for i in range(len(K)):
        (x1, y1), (x2, y2) = K[i], K[(i + 1) % len(K)]
        if (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) < -1e-12:
            return False
    return True


def dis_bukeyler_kesisir(A, B) -> bool:
    """Ayıran eksen teoremi (dış bükey çokgenler; değmek kesişmek sayılır)."""
    for K in (A, B):
        for i in range(len(K)):
            ex, ey = K[(i + 1) % len(K)][0] - K[i][0], K[(i + 1) % len(K)][1] - K[i][1]
            n = (-ey, ex)
            pa = [n[0] * p[0] + n[1] * p[1] for p in A]
            pb = [n[0] * p[0] + n[1] * p[1] for p in B]
            if max(pa) < min(pb) - 1e-12 or max(pb) < min(pa) - 1e-12:
                return False
    return True


# --- Üçgen robotun C-uzayı engeli -----------------------------------------------------------------
UCGEN = [(0.0, 0.0), (2.0, 0.0), (0.0, 1.0)]           # dik açılı köşe referans noktası
ENGEL = [(4.0, 2.0), (6.0, 2.0), (6.0, 3.0), (4.0, 3.0)]


def c_engeli(robot=UCGEN, engel=ENGEL) -> list[tuple[float, float]]:
    """Dönmeyen robot için C_obs = O ⊕ (−A): bütün o − a farklarının dış bükey kabuğu."""
    return dis_kabuk([(o[0] - a[0], o[1] - a[1]) for o in engel for a in robot])


def ucgen_carpisir(q, robot=UCGEN, engel=ENGEL) -> bool:
    return dis_bukeyler_kesisir([(q[0] + a[0], q[1] + a[1]) for a in robot], engel)


# --- İki eklemli kol ------------------------------------------------------------------------------
L1, L2 = 1.0, 1.0


def ileri_kinematik(t1: float, t2: float):
    """(dirsek, el) konumları; açılar radyan, t2 dirseğin birinci kola göre açısı."""
    dirsek = (L1 * math.cos(t1), L1 * math.sin(t1))
    el = (dirsek[0] + L2 * math.cos(t1 + t2), dirsek[1] + L2 * math.sin(t1 + t2))
    return dirsek, el


def ters_kinematik(x: float, y: float) -> list[tuple[float, float]]:
    """φ(q) = (x, y) olan bütün q'lar (0, 1 ya da 2 çözüm)."""
    c2 = (x * x + y * y - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    if abs(c2) > 1 + 1e-12:
        return []
    cozumler = []
    for isaret in (1, -1):
        t2 = isaret * math.acos(max(-1.0, min(1.0, c2)))
        t1 = math.atan2(y, x) - math.atan2(L2 * math.sin(t2), L1 + L2 * math.cos(t2))
        cozumler.append((t1, t2))
    return cozumler if abs(c2) < 1 - 1e-12 else cozumler[:1]


def dogrular_kesisir(p1, p2, q1, q2) -> bool:
    d = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])  # noqa: E731
    d1, d2, d3, d4 = d(q1, q2, p1), d(q1, q2, p2), d(p1, p2, q1), d(p1, p2, q2)
    return (d1 * d2 <= 0) and (d3 * d4 <= 0)


ASILI_ENGEL = ((0.9, 1.0), (0.9, 2.5))                # tavandan sarkan dikey engel (bizim örneğimiz)


def kol_carpisir(t1: float, t2: float, engel=ASILI_ENGEL) -> bool:
    """Çarpışma denetleyicisi γ(q): masa (y < 0), kendine çarpma (|θ_dirsek| > 160°), sarkan engel."""
    dirsek, el = ileri_kinematik(t1, t2)
    if dirsek[1] < -1e-9 or el[1] < -1e-9 or abs(t2) > math.radians(160):
        return True
    return dogrular_kesisir((0, 0), dirsek, *engel) or dogrular_kesisir(dirsek, el, *engel)


def kol_c_uzayi(adim_derece: int = 5):
    """θ_omuz ∈ [0°, 180°], θ_dirsek ∈ [−180°, 180°) ızgarası; True = çarpışma."""
    t1 = np.arange(0, 181, adim_derece)
    t2 = np.arange(-180, 180, adim_derece)
    C = np.array([[kol_carpisir(math.radians(a), math.radians(b)) for b in t2] for a in t1])
    return t1, t2, C


def izgara_en_kisa(C: np.ndarray, bas: tuple[int, int], hedef: tuple[int, int]):
    """8 komşulu ızgarada Dijkstra: hedeften her hücreye maliyet (değer fonksiyonu) ve yol."""
    n, m = C.shape
    V = np.full(C.shape, np.inf)
    V[hedef] = 0.0
    kuyruk = [(0.0, hedef)]
    while kuyruk:
        d, (i, j) = heapq.heappop(kuyruk)
        if d > V[i, j]:
            continue
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                a, b = i + di, j + dj
                if (di or dj) and 0 <= a < n and 0 <= b < m and not C[a, b]:
                    nd = d + math.hypot(di, dj)
                    if nd < V[a, b]:
                        V[a, b] = nd
                        heapq.heappush(kuyruk, (nd, (a, b)))
    if not np.isfinite(V[bas]):
        return V, None
    yol, (i, j) = [bas], bas
    while (i, j) != hedef:
        komsu = [(V[i + di, j + dj] + math.hypot(di, dj), (i + di, j + dj))
                 for di in (-1, 0, 1) for dj in (-1, 0, 1)
                 if (di or dj) and 0 <= i + di < n and 0 <= j + dj < m]
        i, j = min(komsu)[1]
        yol.append((i, j))
    return V, yol


# --- 2B dünya: dikdörtgen engeller ------------------------------------------------------------------
DUNYA = (10.0, 6.0)
# (x1, y1, x2, y2); engeller dünya sınırının dışına taşar, böylece duvarla engel arasında sıfır genişlikli geçit kalmaz.
ENGELLER = [(2.0, -1.0, 3.0, 4.0), (6.0, 2.0, 7.0, 7.0)]
BASLA, HEDEF = (0.5, 0.5), (9.5, 5.5)


def serbest_nokta(p, engeller=ENGELLER, pay: float = 1e-9) -> bool:
    x, y = p
    if not (0 <= x <= DUNYA[0] and 0 <= y <= DUNYA[1]):
        return False
    return not any(x1 + pay < x < x2 - pay and y1 + pay < y < y2 - pay for x1, y1, x2, y2 in engeller)


def serbest_dogru(p, q, engeller=ENGELLER, ornek: int = 200) -> bool:
    """Basit planlayıcı B(p, q): doğru parçası dünyanın dışına çıkmıyor ve engellerin içinden geçmiyorsa başarılı."""
    t = np.linspace(0, 1, ornek)[1:-1, None]
    P = np.asarray(p, dtype=float) + t * (np.asarray(q, dtype=float) - np.asarray(p, dtype=float))
    x, y = P[:, 0], P[:, 1]
    if (x < 0).any() or (x > DUNYA[0]).any() or (y < 0).any() or (y > DUNYA[1]).any():
        return False
    for x1, y1, x2, y2 in engeller:
        if ((x1 + 1e-9 < x) & (x < x2 - 1e-9) & (y1 + 1e-9 < y) & (y < y2 - 1e-9)).any():
            return False
    return True


def dijkstra(dugumler, kenarlar, bas: int, hedef: int):
    uzak = {bas: 0.0}
    onceki = {}
    kuyruk = [(0.0, bas)]
    while kuyruk:
        d, u = heapq.heappop(kuyruk)
        if u == hedef:
            break
        if d > uzak.get(u, math.inf):
            continue
        for v in kenarlar.get(u, ()):
            nd = d + math.dist(dugumler[u], dugumler[v])
            if nd < uzak.get(v, math.inf):
                uzak[v], onceki[v] = nd, u
                heapq.heappush(kuyruk, (nd, v))
    if hedef not in uzak:
        return None, math.inf
    yol = [hedef]
    while yol[-1] != bas:
        yol.append(onceki[yol[-1]])
    return [dugumler[i] for i in reversed(yol)], uzak[hedef]


def gorunurluk_cizgesi(bas=BASLA, hedef=HEDEF, engeller=ENGELLER):
    dugumler = [bas, hedef] + [k for x1, y1, x2, y2 in engeller for k in ((x1, y1), (x2, y1), (x2, y2), (x1, y2))]
    dugumler = [d for d in dugumler if serbest_nokta(d, engeller)]
    kenarlar = {i: [] for i in range(len(dugumler))}
    for i in range(len(dugumler)):
        for j in range(i + 1, len(dugumler)):
            if serbest_dogru(dugumler[i], dugumler[j], engeller):
                kenarlar[i].append(j)
                kenarlar[j].append(i)
    return dijkstra(dugumler, kenarlar, 0, 1)


def prm(M: int, k: int = 5, tohum: int = 0, en_cok_tur: int = 20, bas=BASLA, hedef=HEDEF, engeller=ENGELLER):
    """k-PRM: M kilometre taşı örnekle (reddetme örneklemesi), her birini k en yakın komşusuna basit planlayıcıyla
    bağla, çizgede ara. Yol yoksa M taş daha ekle ve tekrarla (kitaptaki döngü).
    (yol, uzunluk, kullanılan taş sayısı)."""
    rng = np.random.default_rng(tohum)
    dugumler = [bas, hedef]
    for _ in range(en_cok_tur):
        hedef_sayi = len(dugumler) + M
        while len(dugumler) < hedef_sayi:
            p = (float(rng.uniform(0, DUNYA[0])), float(rng.uniform(0, DUNYA[1])))
            if serbest_nokta(p, engeller):
                dugumler.append(p)
        A = np.array(dugumler)
        kenarlar = {i: set() for i in range(len(dugumler))}
        for i in range(len(dugumler)):
            d = np.hypot(*(A - A[i]).T)
            for j in np.argsort(d)[1:k + 1]:
                if serbest_dogru(dugumler[i], dugumler[j], engeller):
                    kenarlar[i].add(int(j))
                    kenarlar[int(j)].add(i)
        yol, uzunluk = dijkstra(dugumler, kenarlar, 0, 1)
        if yol is not None:
            return yol, uzunluk, len(dugumler) - 2
    return None, math.inf, len(dugumler) - 2


def yol_uzunlugu(yol) -> float:
    return sum(math.dist(yol[i], yol[i + 1]) for i in range(len(yol) - 1))


def rrt_cift_yonlu(delta: float = 0.5, en_cok: int = 5000, tohum: int = 0, bas=BASLA, hedef=HEDEF, engeller=ENGELLER):
    """İki ağaç (başlangıçtan ve hedeften). Her rastgele kilometre taşı q için: q her iki ağacın en yakın
    düğümüne doğrudan bağlanabiliyorsa çözüm bulunmuştur; değilse her ağaç en yakın düğümünden q'ya doğru
    δ uzunluğunda bir kenarla büyütülür (engel yoksa)."""
    rng = np.random.default_rng(tohum)
    agaclar = [([bas], [None]), ([hedef], [None])]           # (düğümler, ebeveynler)
    for _ in range(en_cok):
        q = (float(rng.uniform(0, DUNYA[0])), float(rng.uniform(0, DUNYA[1])))
        if not serbest_nokta(q, engeller):
            continue
        en_yakin = [int(np.argmin(np.hypot(*(np.array(dugum) - q).T))) for dugum, _ in agaclar]
        baglanan = [serbest_dogru(dugum[i], q, engeller) for (dugum, _), i in zip(agaclar, en_yakin)]
        if not all(baglanan):
            for (dugum, ebeveyn), i in zip(agaclar, en_yakin):
                p = dugum[i]
                d = math.dist(p, q)
                yeni = q if d <= delta else (p[0] + delta * (q[0] - p[0]) / d, p[1] + delta * (q[1] - p[1]) / d)
                if serbest_dogru(p, yeni, engeller):
                    dugum.append(yeni)
                    ebeveyn.append(i)
            continue
        zincirler = []
        for (dugum, ebeveyn), i in zip(agaclar, en_yakin):
            zincir = []
            while i is not None:
                zincir.append(dugum[i])
                i = ebeveyn[i]
            zincirler.append(zincir)
        return list(reversed(zincirler[0])) + [q] + zincirler[1]
    return None


def kisalt(yol, deneme: int = 200, tohum: int = 0, engeller=ENGELLER):
    """Kısaltma: rastgele bir ara düğümü, komşularını doğrudan bağlayarak çıkarmayı dene."""
    rng = np.random.default_rng(tohum)
    yol = list(yol)
    for _ in range(deneme):
        if len(yol) <= 2:
            break
        i = int(rng.integers(1, len(yol) - 1))
        if serbest_dogru(yol[i - 1], yol[i + 1], engeller):
            del yol[i]
    return yol


# --- Yörünge optimizasyonu --------------------------------------------------------------------------
NOKTA_ENGELLER = [((3.5, 0.2), 1.5), ((6.5, -0.3), 1.5)]   # (merkez, maliyet bandının yarıçapı)


def engel_maliyeti(P: np.ndarray, engeller=NOKTA_ENGELLER) -> tuple[np.ndarray, np.ndarray]:
    """c(x) = Σ ½ max(0, r − ‖x − o‖)² ve gradyanı."""
    c, g = np.zeros(len(P)), np.zeros_like(P)
    for o, r in engeller:
        d = P - np.array(o)
        uz = np.linalg.norm(d, axis=1) + 1e-12
        ihlal = np.maximum(0.0, r - uz)
        c += 0.5 * ihlal ** 2
        g += (-ihlal / uz)[:, None] * d
    return c, g


def yorunge_optimizasyonu(N: int = 50, lam: float = 1000.0, adim: int = 6000, ogrenme: float = 0.005,
                          bas=(0.0, 0.0), hedef=(10.0, 0.0), baslangic=None, engeller=NOKTA_ENGELLER):
    """τ_0..τ_N (uçlar sabit). J_eff ≈ Σ ½ N ‖τᵢ₊₁ − τᵢ‖² (∫½‖τ̇‖²'nin ayrıklaştırılması),
    J_obs ≈ Σ c(τᵢ)/N (yol integralindeki ‖dφ/ds‖ çarpanını basitlik için atıyoruz)."""
    T = np.linspace(bas, hedef, N + 1) if baslangic is None else np.array(baslangic, dtype=float)
    for _ in range(adim):
        g_eff = np.zeros_like(T)
        g_eff[1:-1] = N * (2 * T[1:-1] - T[:-2] - T[2:])          # ≈ −τ̈ (Euler–Lagrange)
        _, g_obs = engel_maliyeti(T, engeller)
        g = g_eff + lam * g_obs / N
        g[0] = g[-1] = 0
        T -= ogrenme * g
    return T


def en_kucuk_aciklik(T: np.ndarray, engeller=NOKTA_ENGELLER) -> float:
    return float(min(np.linalg.norm(T - np.array(o), axis=1).min() for o, _ in engeller))


def main() -> None:
    print("=== C-uzayı engeli: dönmeyen üçgen robot + dikdörtgen engel ===")
    K = c_engeli()
    print(f"  C_obs köşeleri ({len(K)} kenar): {K}")
    print(f"  Alan: engel 2.0, robot 1.0, C_obs {cokgen_alani(K):.1f}")
    xs, ys = np.arange(0.05, 8, 0.1), np.arange(0.05, 5, 0.1)
    uyum = np.mean([ucgen_carpisir((x, y)) == icinde_mi((x, y), K) for x in xs for y in ys])
    print(f"  Izgarada çarpışma denetleyicisi ile Minkowski çokgeninin uyumu: %{100 * uyum:.1f}")

    print("\n=== İki eklemli kol: kinematik ===")
    d, e = ileri_kinematik(math.radians(30), math.radians(60))
    print(f"  φ(30°, 60°): dirsek {tuple(round(v, 3) for v in d)}, el {tuple(round(v, 3) for v in e)}")
    for t1, t2 in ters_kinematik(*e):
        print(f"  ters kinematik çözümü: ({math.degrees(t1):6.1f}°, {math.degrees(t2):6.1f}°) → "
              f"el {tuple(round(v, 3) for v in ileri_kinematik(t1, t2)[1])}")
    print(f"  Erişilemeyen (2.5, 0): {ters_kinematik(2.5, 0)};  tam uzanmış (2, 0): {ters_kinematik(2, 0)}")

    print("\n=== Kolun C-uzayı ve ızgarada planlama (5° hücreler) ===")
    t1, t2, C = kol_c_uzayi()
    print(f"  {C.size} hücrenin %{100 * C.mean():.0f}'i çarpışmalı")
    bas, hedef = (0, list(t2).index(0)), (list(t1).index(120), list(t2).index(0))
    duz = any(kol_carpisir(math.radians(a), 0.0) for a in range(0, 121, 5))
    print(f"  Başlangıç (0°, 0°) → hedef (120°, 0°); C-uzayında düz çizgi çarpışır mı? {duz}")
    V, yol = izgara_en_kisa(C, bas, hedef)
    dirsek = [t2[j] for _, j in yol]
    print(f"  Bulunan yol: {len(yol)} hücre, maliyet {V[bas]:.1f} adım; dirsek en çok {max(dirsek, key=abs)}°'ye bükülüyor")

    print("\n=== 2B dünya (iki dikdörtgen engel): görünürlük çizgesi, PRM, RRT ===")
    gy, gu = gorunurluk_cizgesi()
    print(f"  Görünürlük çizgesi: uzunluk {gu:.3f}, yol {gy}")
    for M in (10, 50):
        sonuc = [prm(M, tohum=t) for t in range(20)]
        tek_tur = sum(s[2] == M for s in sonuc)
        print(f"  k-PRM (k = 5), turda M = {M} taş: ilk turda başarı {tek_tur}/20; gereken taş ort. "
              f"{np.mean([s[2] for s in sonuc]):.0f}, en çok {max(s[2] for s in sonuc)}; "
              f"ort. uzunluk {np.mean([s[1] for s in sonuc]):.2f}")
    r = rrt_cift_yonlu()
    print(f"  Çift yönlü RRT: {len(r)} düğüm, uzunluk {yol_uzunlugu(r):.2f}; kısaltma sonrası "
          f"{yol_uzunlugu(kisalt(r)):.2f} (en iyi {gu:.2f})")

    print("\n=== Yörünge optimizasyonu: iki nokta engel (yarıçap 1.5 maliyet bandı) ===")
    duz = np.linspace((0, 0), (10, 0), 51)
    print(f"  Düz çizginin engellere en küçük uzaklığı: {en_kucuk_aciklik(duz):.2f}")
    T = yorunge_optimizasyonu()
    print(f"  Optimizasyon sonrası: en küçük uzaklık {en_kucuk_aciklik(T):.2f}, uzunluk {yol_uzunlugu(T):.2f}, "
          f"y aralığı [{T[:, 1].min():.2f}, {T[:, 1].max():.2f}] (birinci engelin altından, ikincinin üstünden)")
    kivrik = np.linspace((0, 0), (10, 0), 51) + np.stack([np.zeros(51), np.sin(np.linspace(0, 3 * np.pi, 51))], 1)
    T2 = yorunge_optimizasyonu(baslangic=kivrik, engeller=[])
    print(f"  Engelsiz, kıvrık başlangıç: uzunluk {yol_uzunlugu(kivrik):.2f} → {yol_uzunlugu(T2):.2f} (düz çizgi 10)")


if __name__ == "__main__":
    main()
