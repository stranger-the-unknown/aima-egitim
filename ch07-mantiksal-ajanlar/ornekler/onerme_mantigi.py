#!/usr/bin/env python3
"""Küçük önerme mantığı KB — Tell / Ask (doğruluk tablosu ile gerektirme).

Eğitim amaçlı; sembol sayısı küçük tutulur (2^n model).
Resmi referans: https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Set

# ---------------------------------------------------------------------------
# Basit ifade ağacı: atom | ('not', e) | ('and', e1, e2) | ('or', ...) | ('implies', ...)
# ---------------------------------------------------------------------------
Expr = str | tuple


def atom(name: str) -> str:
    return name


def NOT(e: Expr) -> Expr:
    return ("not", e)


def AND(a: Expr, b: Expr) -> Expr:
    return ("and", a, b)


def OR(a: Expr, b: Expr) -> Expr:
    return ("or", a, b)


def IMPLIES(a: Expr, b: Expr) -> Expr:
    return ("implies", a, b)


def semboller(e: Expr) -> Set[str]:
    if isinstance(e, str):
        return {e}
    op = e[0]
    if op == "not":
        return semboller(e[1])
    return semboller(e[1]) | semboller(e[2])


def degerlendir(e: Expr, model: Dict[str, bool]) -> bool:
    if isinstance(e, str):
        return model[e]
    op = e[0]
    if op == "not":
        return not degerlendir(e[1], model)
    if op == "and":
        return degerlendir(e[1], model) and degerlendir(e[2], model)
    if op == "or":
        return degerlendir(e[1], model) or degerlendir(e[2], model)
    if op == "implies":
        return (not degerlendir(e[1], model)) or degerlendir(e[2], model)
    raise ValueError(f"Bilinmeyen op: {op}")


def yaz(e: Expr) -> str:
    if isinstance(e, str):
        return e
    op = e[0]
    if op == "not":
        return f"¬{yaz(e[1])}"
    if op == "and":
        return f"({yaz(e[1])} ∧ {yaz(e[2])})"
    if op == "or":
        return f"({yaz(e[1])} ∨ {yaz(e[2])})"
    if op == "implies":
        return f"({yaz(e[1])} ⇒ {yaz(e[2])})"
    return str(e)


class BilgiTabani:
    def __init__(self) -> None:
        self.cumleler: List[Expr] = []

    def tell(self, e: Expr) -> None:
        self.cumleler.append(e)
        print(f"  Tell: {yaz(e)}")

    def tum_semboller(self, ekstra: Expr | None = None) -> List[str]:
        s: Set[str] = set()
        for c in self.cumleler:
            s |= semboller(c)
        if ekstra is not None:
            s |= semboller(ekstra)
        return sorted(s)

    def kb_and(self) -> Expr:
        """KB cümlelerinin tek bir ∧ ifadesi (boşsa True benzeri atom)."""
        if not self.cumleler:
            return atom("TRUE_EMPTY")
        acc = self.cumleler[0]
        for c in self.cumleler[1:]:
            acc = AND(acc, c)
        return acc

    def gerektirir(self, alpha: Expr) -> bool:
        """KB ⊨ alpha? Tüm modellerde KB doğruysa alpha da doğru mu?"""
        syms = self.tum_semboller(alpha)
        # Boş KB için özel: TRUE_EMPTY her modelde doğru say
        for bitler in itertools.product([False, True], repeat=len(syms)):
            model = dict(zip(syms, bitler))
            if "TRUE_EMPTY" in model:
                model["TRUE_EMPTY"] = True
            kb_ok = all(degerlendir(c, model) for c in self.cumleler) if self.cumleler else True
            if kb_ok and not degerlendir(alpha, model):
                return False
        return True

    def ask(self, alpha: Expr) -> bool:
        sonuc = self.gerektirir(alpha)
        print(f"  Ask: {yaz(alpha)}  →  {'EVET (KB gerektirir)' if sonuc else 'HAYIR (gerektirmez)'}")
        return sonuc

    def ask_yanlis_mi(self, alpha: Expr) -> bool:
        """KB ⊨ ¬alpha?"""
        return self.ask(NOT(alpha))


def demo() -> None:
    print("=== Önerme mantığı KB demosu ===\n")
    print("Senaryo: Yağmur (Y), IslakZemin (I), Bulut (B)")
    print("Kurallar: Y ⇒ I ,  B ∨ Y  (bulut veya yağmur bilgisi sadeleştirilmiş)\n")

    kb = BilgiTabani()
    Y, I, B = atom("Yagmur"), atom("IslakZemin"), atom("Bulut")

    print("— Bilgi ekleniyor —")
    kb.tell(IMPLIES(Y, I))
    kb.tell(OR(B, Y))
    kb.tell(Y)  # algı / gözlem: yağmur yağıyor

    print("\n— Sorgular —")
    kb.ask(I)  # ıslak zemin gerekir mi?
    kb.ask(B)  # bulut zorunlu mu? (hayır: Y doğruysa B ∨ Y için B gerekmez)
    kb.ask(OR(B, I))

    print("\n— Çelişki kontrolü: ¬I sorulunca —")
    kb.ask(NOT(I))  # KB ⊨ ¬I? Hayır

    print("\nModeller (özet): 3 sembol → 8 olası dünya; Tell sonrası")
    print("KB’nin doğru olduğu dünyalarda IslakZemin hep doğru → Ask(I)=EVET.")


def interactive_mini() -> None:
    """İkinci mini örnek: P, P⇒Q ⊢ Q (modus ponens semantik)."""
    print("\n=== Mini: modus ponens semantiği ===")
    kb = BilgiTabani()
    P, Q = atom("P"), atom("Q")
    kb.tell(P)
    kb.tell(IMPLIES(P, Q))
    kb.ask(Q)
    kb.ask(AND(P, Q))


if __name__ == "__main__":
    demo()
    interactive_mini()
