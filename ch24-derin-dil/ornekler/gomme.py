#!/usr/bin/env python3
"""Sözcük gömmeleri (kitaptaki 24.1, 24.5.1).

* One-hot vektörler sözcükler arasında benzerlik taşımaz: her çift aynı uzaklıkta.
* "Bir sözcüğü birlikte bulunduğu sözcüklerden tanırsın" (Firth): Birlikte geçme sayımlarından PPMI + SVD
  ile düşük boyutlu yoğun vektörler (word2vec / GloVe'un temel fikri). Benzer bağlamlarda geçen sözcükler
  yakın düşer.
* Benzetme (analoji): B − A + C'ye en yakın sözcük. Kitap: Athens → Greece ise Oslo → Norway.
  Burada başkent–ülke ilişkisinin bir yön olduğu küçük yapay gömmelerle gösterilir.
* Kosinüs benzerliği: cos(u, v) = u·v / (‖u‖ ‖v‖).

Çalıştırma:
    python gomme.py
"""
from __future__ import annotations

import numpy as np

DERLEM = """kedi süt içti . köpek süt içti . kedi fare kovaladı . köpek kedi kovaladı .
kedi mama yedi . köpek mama yedi . ali araba sürdü . ayşe araba sürdü . ali otobüs bekledi .
ayşe otobüs bekledi . araba yolda gitti . otobüs yolda gitti . kedi evde uyudu . köpek evde uyudu .
ali evde uyudu . ayşe evde uyudu . fare peynir yedi . fare evde uyudu .""".split()


def kosinus(u, v) -> float:
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12))


def birlikte_gecme(derlem: list[str], pencere: int = 2):
    sozcukler = sorted(set(derlem) - {"."})
    indeks = {w: i for i, w in enumerate(sozcukler)}
    M = np.zeros((len(sozcukler), len(sozcukler)))
    for i, w in enumerate(derlem):
        if w == ".":
            continue
        for j in range(max(0, i - pencere), min(len(derlem), i + pencere + 1)):
            if j != i and derlem[j] != ".":
                M[indeks[w], indeks[derlem[j]]] += 1
    return sozcukler, M


def ppmi_svd(M, boyut: int = 4):
    """Pozitif noktasal karşılıklı bilgi, sonra kesilmiş SVD."""
    toplam = M.sum()
    pw = M.sum(axis=1, keepdims=True) / toplam
    pc = M.sum(axis=0, keepdims=True) / toplam
    with np.errstate(divide="ignore"):
        pmi = np.log((M / toplam) / (pw * pc))
    ppmi = np.where(np.isfinite(pmi) & (pmi > 0), pmi, 0.0)
    U, S, _ = np.linalg.svd(ppmi)
    return U[:, :boyut] * S[:boyut]


def en_yakinlar(sozcuk: str, sozcukler, V, k: int = 3) -> list[tuple[str, float]]:
    i = sozcukler.index(sozcuk)
    puan = [(w, kosinus(V[i], V[j])) for j, w in enumerate(sozcukler) if j != i]
    return sorted(puan, key=lambda t: -t[1])[:k]


# --- Benzetmeler: yapay gömmeler ------------------------------------------------------------
def yapay_gommeler(tohum: int = 0, boyut: int = 20):
    """Her ülkenin rastgele bir vektörü var; başkent = ülke + ortak 'başkent' yönü + küçük gürültü."""
    rng = np.random.default_rng(tohum)
    ulkeler = {"Yunanistan": "Atina", "Norveç": "Oslo", "Türkiye": "Ankara", "Fransa": "Paris", "Japonya": "Tokyo"}
    baskent_yonu = rng.normal(0, 1, boyut)
    V = {}
    for ulke, baskent in ulkeler.items():
        v = rng.normal(0, 1, boyut)
        V[ulke] = v
        V[baskent] = v + baskent_yonu + rng.normal(0, 0.1, boyut)
    for w in ("elma", "masa", "kitap"):
        V[w] = rng.normal(0, 1, boyut)
    return V


def benzetme(V: dict, a: str, b: str, c: str) -> str:
    """a, b'ye neyse c, ?'ye odur: ? ≈ b − a + c (a, b, c hariç en yakın sözcük)."""
    hedef = V[b] - V[a] + V[c]
    adaylar = [w for w in V if w not in (a, b, c)]
    return max(adaylar, key=lambda w: kosinus(V[w], hedef))


def main() -> None:
    print("=== One-hot: her sözcük çifti eşit uzaklıkta ===")
    I = np.eye(4)
    print(f"  cos(kedi, köpek) = {kosinus(I[0], I[1])}, cos(kedi, araba) = {kosinus(I[0], I[2])}")

    print("\n=== Birlikte geçme + PPMI + SVD (küçük Türkçe derlem, 4 boyut) ===")
    sozcukler, M = birlikte_gecme(DERLEM)
    V = ppmi_svd(M)
    for w in ("kedi", "araba", "ali"):
        print(f"  {w:<6} en yakın: " + ", ".join(f"{u} ({s:.2f})" for u, s in en_yakinlar(w, sozcukler, V)))
    print(f"  cos(kedi, köpek) = {kosinus(V[sozcukler.index('kedi')], V[sozcukler.index('köpek')]):.2f}, "
          f"cos(kedi, otobüs) = {kosinus(V[sozcukler.index('kedi')], V[sozcukler.index('otobüs')]):.2f}")

    print("\n=== Benzetmeler (yapay gömmeler: başkent = ülke + ortak yön) ===")
    G = yapay_gommeler()
    for a, b, c in (("Atina", "Yunanistan", "Oslo"), ("Yunanistan", "Atina", "Türkiye"), ("Fransa", "Paris", "Japonya")):
        print(f"  {a} → {b} ise {c} → {benzetme(G, a, b, c)}")


if __name__ == "__main__":
    main()
