#!/usr/bin/env python3
"""Kitabın hırsız alarmı ağı (Judea Pearl'ün örneği).

    Burglary   Earthquake
          \\     /
           Alarm
          /     \\
    JohnCalls  MaryCalls

CPT'ler:  P(B) = 0.001, P(E) = 0.002
          P(A | B, E): tt 0.95, tf 0.94, ft 0.29, ff 0.001
          P(J | A): 0.90 / 0.05       P(M | A): 0.70 / 0.01

Not: Elimizdeki PDF'te Şekil 13.2'nin Alarm tablosu hatalı basılmış (MaryCalls sütunu
kopyalanmış: .70/.01/.70/.01). Kitabın 13.3'teki hesabı (0.00059224, 0.0014919 → 0.284)
ve Şekil 13.10 ise yukarıdaki standart değerlerle tutarlıdır; onları kullanıyoruz.

Kitaptaki sonuçlar (testlerle doğrulanır):
    P(j, m, a, ¬b, ¬e) = 0.90 × 0.70 × 0.001 × 0.999 × 0.998 ≈ 0.000628
    P(B | j, m) = α⟨0.00059224, 0.0014919⟩ ≈ ⟨0.284, 0.716⟩
    Düğüm sırası: B,E,A,J,M → 10 parametre; M,J,A,B,E → 13; M,J,E,B,A → 31

Çalıştırma:
    python hirsiz_alarmi.py
"""
from __future__ import annotations

import itertools

from bayes_agi import BayesAgi

T, F = True, False


def hirsiz_agi() -> BayesAgi:
    ag = BayesAgi()
    ag.ekle("Burglary", [], {(): 0.001})
    ag.ekle("Earthquake", [], {(): 0.002})
    ag.ekle("Alarm", ["Burglary", "Earthquake"], {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001})
    ag.ekle("JohnCalls", ["Alarm"], {(T,): 0.90, (F,): 0.05})
    ag.ekle("MaryCalls", ["Alarm"], {(T,): 0.70, (F,): 0.01})
    return ag


def minimal_ebeveynler(ag: BayesAgi, sira: list[str], tol: float = 1e-12) -> dict[str, tuple]:
    """Verilen sırayla ağ kurarken her düğüm için, öncüllerinden onu diğer öncüllerinden
    koşullu bağımsız kılan en küçük ebeveyn kümesini bul (tam ortak dağılımı kullanarak)."""
    ortak = ag.tam_ortak_tablo()
    idx = {x: i for i, x in enumerate(ag.degiskenler)}

    def marjinal(degiskenler):
        m: dict = {}
        for deg, p in ortak.items():
            k = tuple(deg[idx[x]] for x in degiskenler)
            m[k] = m.get(k, 0.0) + p
        return m

    def kosullu(x, kume):
        pay, payda = marjinal([x] + list(kume)), marjinal(list(kume))
        return {k: pay.get((True,) + k, 0.0) / v for k, v in payda.items() if v > 0}

    sonuc = {}
    for i, x in enumerate(sira):
        onculler = sira[:i]
        tam = kosullu(x, onculler)
        for boyut in range(len(onculler) + 1):
            bulundu = None
            for S in itertools.combinations(onculler, boyut):
                kısmi = kosullu(x, S)
                pos = [onculler.index(s) for s in S]
                if all(abs(p - kısmi[tuple(k[j] for j in pos)]) < tol for k, p in tam.items()):
                    bulundu = S
                    break
            if bulundu is not None:
                sonuc[x] = bulundu
                break
    return sonuc


def main() -> None:
    ag = hirsiz_agi()
    print("=== Ağın anlamı: ortak dağılım = CPT girdilerinin çarpımı ===")
    olay = {"JohnCalls": T, "MaryCalls": T, "Alarm": T, "Burglary": F, "Earthquake": F}
    print(f"  P(j, m, a, ¬b, ¬e) = 0.90 × 0.70 × 0.001 × 0.999 × 0.998 = {ag.ortak(olay):.6f}")
    print(f"  Parametre sayısı: {ag.parametre_sayisi()}  (tam ortak tablo: 2⁵ − 1 = 31)")

    print("\n=== P(Burglary | johnCalls, maryCalls) ===")
    ag.carpma_sayisi = 0
    ham = ag.numaralandirma("Burglary", {"JohnCalls": T, "MaryCalls": T}, ham=True)
    n_say = ag.carpma_sayisi
    print(f"  Numaralandırma (normalize etmeden): b → {ham[T]:.8f}, ¬b → {ham[F]:.7f}")
    sonuc = ag.numaralandirma("Burglary", {"JohnCalls": T, "MaryCalls": T})
    print(f"  Normalize: ⟨{sonuc[T]:.3f}, {sonuc[F]:.3f}⟩  → iki komşu da ararsa hırsızlık olasılığı ~%28")
    ag.carpma_sayisi = 0
    ve = ag.degisken_eleme("Burglary", {"JohnCalls": T, "MaryCalls": T})
    print(f"  Değişken eleme:     ⟨{ve[T]:.3f}, {ve[F]:.3f}⟩  (çarpma: numaralandırma {n_say}, eleme {ag.carpma_sayisi})")

    print("\n=== Başka sorgular ===")
    sorgular = [("Burglary", {"JohnCalls": T}), ("Burglary", {"MaryCalls": T}),
                ("Earthquake", {"JohnCalls": T, "MaryCalls": T}),
                ("Burglary", {"Alarm": T}), ("Burglary", {"Alarm": T, "Earthquake": T}),
                ("Burglary", {}), ("Burglary", {"JohnCalls": T, "MaryCalls": F})]
    for X, e in sorgular:
        kanit = ", ".join(f"{'' if v else '¬'}{k}" for k, v in e.items()) or "—"
        sorgu = f"P({X} | {kanit})"
        print(f"  {sorgu:<40} = {ag.degisken_eleme(X, e)[T]:.5f}")
    print("  Açıklayıp götürme: Alarm çaldığında hırsızlık olasılığı ~0.37. Deprem olduğu da")
    print("  öğrenilince alarmın açıklaması bulunur ve hırsızlık olasılığı ~0.003'e düşer.")

    print("\n=== İlgisiz değişkenler ===")
    print(f"  P(JohnCalls | burglary) = {ag.degisken_eleme('JohnCalls', {'Burglary': T})[T]:.4f}")
    print("  MaryCalls, sorgunun ya da kanıtın atası değil: eleme onu hiç hesaba katmaz (toplamı 1).")

    print("\n=== Markov örtüsü ===")
    for x in ag.degiskenler:
        print(f"  {x:<10}: {sorted(ag.markov_ortusu(x))}")

    print("\n=== Düğüm sırası ağın büyüklüğünü değiştirir ===")
    for sira in (["Burglary", "Earthquake", "Alarm", "JohnCalls", "MaryCalls"],
                 ["MaryCalls", "JohnCalls", "Alarm", "Burglary", "Earthquake"],
                 ["MaryCalls", "JohnCalls", "Earthquake", "Burglary", "Alarm"]):
        eb = minimal_ebeveynler(ag, sira)
        toplam = sum(2 ** len(v) for v in eb.values())
        print(f"  {' → '.join(s[0] for s in sira)}: {toplam:>2} parametre   "
              + "; ".join(f"{x[0]}←{''.join(p[0] for p in v) or '∅'}" for x, v in eb.items()))
    print("  Nedenler etkilerden önce gelirse ağ küçük ve anlaşılır olur (kitap: 10, 13, 31).")


if __name__ == "__main__":
    main()
