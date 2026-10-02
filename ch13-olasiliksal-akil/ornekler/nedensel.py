#!/usr/bin/env python3
"""Nedensel ağlar ve do-işleci (kitaptaki 13.5), yağmurlama ağı üzerinde.

Gözlem ile müdahale farklıdır:
  * P(Rain | Sprinkler = true): Yağmurlamanın açık olduğunu GÖRDÜK. Yağmurlama genelde
    bulutsuz günlerde açılır, bu da yağmur olasılığını düşürür: 0.3.
  * P(Rain | do(Sprinkler = true)): Yağmurlamayı biz AÇTIK. Bulutlar ve yağmur bundan
    etkilenmez: P(Rain) = 0.5.
do(X = x), X'e gelen okları silen "sakatlanmış" ağda koşullamaya denktir.

Arka kapı ölçütü: Cloudy, Sprinkler'dan WetGrass'a giden arka kapı yolunu kapatır, bu yüzden
    P(w | do(s)) = Σ_c P(w | s, c) P(c)
yalnızca gözlemsel dağılımla (deney yapmadan) hesaplanabilir.

Çalıştırma:
    python nedensel.py
"""
from __future__ import annotations

from ornekleme import yagmurlama_agi

T, F = True, False


def arka_kapi_ayarlamasi(ag, z: str = "Cloudy", deger: bool = True) -> float:
    """P(WetGrass | do(Sprinkler = deger)) = Σ_z P(WetGrass | Sprinkler = deger, z) P(z)."""
    toplam = 0.0
    for v in (T, F):
        p_z = ag.numaralandirma(z, {})[v]
        toplam += ag.numaralandirma("WetGrass", {"Sprinkler": deger, z: v})[T] * p_z
    return toplam


def main() -> None:
    ag = yagmurlama_agi()
    mud = ag.mudahale("Sprinkler", True)

    print("=== Gözlem mi, müdahale mi? ===")
    print(f"  P(Rain)                         = {ag.numaralandirma('Rain', {})[T]:.3f}")
    print(f"  P(Rain | Sprinkler = true)      = {ag.numaralandirma('Rain', {'Sprinkler': T})[T]:.3f}  (gözlem)")
    print(f"  P(Rain | do(Sprinkler = true))  = {mud.numaralandirma('Rain', {})[T]:.3f}  (müdahale)")
    print(f"  P(Cloudy | Sprinkler = true)    = {ag.numaralandirma('Cloudy', {'Sprinkler': T})[T]:.3f}")
    print(f"  P(Cloudy | do(Sprinkler = true))= {mud.numaralandirma('Cloudy', {})[T]:.3f}")
    print("  Yağmurlamanın açık olduğunu görmek havanın bulutsuz olduğuna dair kanıttır. Ama onu")
    print("  açmak havayı değiştirmez: müdahale yalnızca Sprinkler'ın torunlarını etkiler.")

    print("\n=== Çimenin ıslak olma olasılığı ===")
    gozlem = ag.numaralandirma("WetGrass", {"Sprinkler": T})[T]
    mudahale = mud.numaralandirma("WetGrass", {})[T]
    print(f"  P(WetGrass | Sprinkler = true)     = {gozlem:.4f}")
    print(f"  P(WetGrass | do(Sprinkler = true)) = {mudahale:.4f}  (sakatlanmış ağ)")
    print(f"  Arka kapı ayarlaması Σ_c P(w|s,c)P(c) = {arka_kapi_ayarlamasi(ag, 'Cloudy'):.4f}  (yalnızca gözlemsel veri)")
    print(f"  Arka kapı ayarlaması Σ_r P(w|s,r)P(r) = {arka_kapi_ayarlamasi(ag, 'Rain'):.4f}  (Rain de kapıyı kapatır)")
    print("  Ayarlama sakatlanmış ağla aynı sonucu verir: Cloudy'yi (ya da Rain'i) hesaba katmak,")
    print("  'yağmurlama genelde güneşli günlerde açılır' olgusundan doğan yanlılığı ortadan kaldırır.")


if __name__ == "__main__":
    main()
