#!/usr/bin/env python3
"""Küçük bloklar dünyası: STRIPS-benzeri aksiyonlar + BFS planlayıcı.

Özgün eğitim örneği. Kitap metni / şekil kopyası değildir.
Durum = frozenset[str] liteller. Aksiyonlar somut (A, B, C, Masa).

Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

State = frozenset[str]


@dataclass(frozen=True)
class Aksiyon:
    ad: str
    onkosul: frozenset[str]
    sil: frozenset[str]
    ekle: frozenset[str]

    def uygulanabilir(self, s: State) -> bool:
        return self.onkosul <= s

    def uygula(self, s: State) -> State:
        return frozenset((s - self.sil) | self.ekle)

    def __str__(self) -> str:
        return self.ad


def bloklar_aksiyonlari(bloklar: Sequence[str]) -> List[Aksiyon]:
    """A, B, C ve Masa için somut Kaldir / Koy / MasayaKoy aksiyonları."""
    masa = "Masa"
    aksiyonlar: List[Aksiyon] = []
    yerler = list(bloklar) + [masa]

    for x in bloklar:
        aksiyonlar.append(
            Aksiyon(
                ad=f"MasayaKoy({x})",
                onkosul=frozenset({f"Tutuyor({x})"}),
                sil=frozenset({f"Tutuyor({x})"}),
                ekle=frozenset({f"On({x}, {masa})", "ElBos", f"Clear({x})"}),
            )
        )
        for y in yerler:
            if x == y:
                continue
            onkosul = {f"On({x}, {y})", f"Clear({x})", "ElBos"}
            sil = {f"On({x}, {y})", "ElBos"}
            ekle = {f"Tutuyor({x})"}
            if y != masa:
                ekle.add(f"Clear({y})")
            aksiyonlar.append(
                Aksiyon(
                    ad=f"Kaldir({x}, {y})",
                    onkosul=frozenset(onkosul),
                    sil=frozenset(sil),
                    ekle=frozenset(ekle),
                )
            )
            if y == masa:
                continue
            aksiyonlar.append(
                Aksiyon(
                    ad=f"Koy({x}, {y})",
                    onkosul=frozenset({f"Tutuyor({x})", f"Clear({y})"}),
                    sil=frozenset({f"Tutuyor({x})", f"Clear({y})"}),
                    ekle=frozenset({f"On({x}, {y})", "ElBos", f"Clear({x})"}),
                )
            )
    return aksiyonlar


def hedef_saglandi(s: State, hedef: State) -> bool:
    return hedef <= s


def bfs_plan(
    baslangic: State,
    hedef: State,
    aksiyonlar: Sequence[Aksiyon],
    max_durum: int = 50_000,
) -> Optional[List[Aksiyon]]:
    """Birim maliyet BFS: en kısa aksiyon dizisi."""
    if hedef_saglandi(baslangic, hedef):
        return []

    kuyruk: deque[Tuple[State, List[Aksiyon]]] = deque([(baslangic, [])])
    ziyaret: Set[State] = {baslangic}

    while kuyruk:
        s, yol = kuyruk.popleft()
        for a in aksiyonlar:
            if not a.uygulanabilir(s):
                continue
            s2 = a.uygula(s)
            if s2 in ziyaret:
                continue
            yol2 = yol + [a]
            if hedef_saglandi(s2, hedef):
                return yol2
            ziyaret.add(s2)
            if len(ziyaret) > max_durum:
                return None
            kuyruk.append((s2, yol2))
    return None


def yaz_durum(s: State, baslik: str = "Durum") -> None:
    print(f"{baslik}: {{{', '.join(sorted(s))}}}")


def demo() -> None:
    bloklar = ["A", "B", "C"]
    aksiyonlar = bloklar_aksiyonlari(bloklar)

    baslangic: State = frozenset(
        {
            "On(A, C)",
            "On(C, Masa)",
            "On(B, Masa)",
            "Clear(A)",
            "Clear(B)",
            "ElBos",
        }
    )
    hedef: State = frozenset(
        {
            "On(A, B)",
            "On(B, Masa)",
            "On(C, Masa)",
            "Clear(A)",
            "Clear(C)",
            "ElBos",
        }
    )

    print("=== Bloklar dünyası — STRIPS + BFS ===")
    yaz_durum(baslangic, "Başlangıç")
    yaz_durum(hedef, "Hedef   ")
    print(f"Somut aksiyon sayısı: {len(aksiyonlar)}")

    plan = bfs_plan(baslangic, hedef, aksiyonlar)
    if plan is None:
        print("Plan bulunamadı.")
        return

    print(f"\nPlan ({len(plan)} adım):")
    s = baslangic
    for i, a in enumerate(plan, 1):
        print(f"  {i}. {a}")
        s = a.uygula(s)
    yaz_durum(s, "\nSon durum")
    print(f"Hedef sağlandı? {hedef_saglandi(s, hedef)}")

    print("\n--- Senaryo 2: B'yi C'nin üstüne koy ---")
    b2: State = frozenset(
        {
            "On(A, Masa)",
            "On(B, Masa)",
            "On(C, Masa)",
            "Clear(A)",
            "Clear(B)",
            "Clear(C)",
            "ElBos",
        }
    )
    h2: State = frozenset({"On(B, C)", "ElBos"})
    plan2 = bfs_plan(b2, h2, aksiyonlar)
    if plan2 is None:
        print("Plan bulunamadı.")
    else:
        print(f"Plan ({len(plan2)} adım): " + " → ".join(str(a) for a in plan2))


if __name__ == "__main__":
    demo()
