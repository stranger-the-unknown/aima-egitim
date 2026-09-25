#!/usr/bin/env python3
"""ELIZA tarzı mini sohbet programı: "taklit etmek anlamak değildir".

Weizenbaum'un 1966 tarihli ELIZA'sı, birkaç kalıp ve zamir çevirme hilesiyle
insanlara "beni anlıyor" dedirtmişti. Bu dosya aynı fikri Türkçe ve çok küçük
ölçekte uygular. Amaç iki şeyi göstermek:

1. Yüzeysel kalıplar kısa bir sohbette şaşırtıcı derecede ikna edici olabilir.
2. Aynı kalıplar olumsuzluk, bağlam ve anlam gerektiren cümlelerde hemen çöker.
   Program hiçbir şey *anlamaz*; sadece metni yeniden düzenler.

Çalıştırma:
    python eliza_mini.py              # hazır diyalog + kırılma örnekleri
    python eliza_mini.py --etkilesim  # kendin yaz (çıkmak için: çıkış)
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field

# (kalıp, olası yanıtlar). {0} yakalanan grubun "yansıtılmış" hâlidir.
KURALLAR: list[tuple[str, list[str]]] = [
    (r"(.*) hissediyorum", ["Ne zamandır {0} hissediyorsun?",
                            "{0} hissetmek sana neyi hatırlatıyor?"]),
    (r"(.*) istiyorum", ["Neden {0} istiyorsun?",
                         "{0} olsaydı ne değişirdi?"]),
    (r".*\b(annem|babam|ailem|kardeşim)\b.*", ["Bana biraz {0} hakkında anlat.",
                                               "Ailenle ilişkin genel olarak nasıl?"]),
    (r".*\bçünkü\b.*", ["Gerçek neden bu mu?",
                        "Aklına başka hangi nedenler geliyor?"]),
    (r".*\b(bilgisayar\w*|makine\w*|robot\w*)\b.*", ["Makineler seni endişelendiriyor mu?",
                                                    "Neden makinelerden söz ettin?"]),
    (r".*\?", ["Bu soruyu neden soruyorsun?",
               "Sence cevabı ne olmalı?"]),
    (r"(evet|hayır)\b.*", ["Oldukça emin görünüyorsun.",
                           "Anlıyorum. Biraz açar mısın?"]),
]

VARSAYILAN = ["Devam et, dinliyorum.", "Bunu biraz daha anlatır mısın?",
              "Bu sana ne hissettiriyor?", "İlginç. Peki sonra ne oldu?"]

# Birinci tekil şahıs → ikinci tekil şahıs (ELIZA'nın temel hilesi)
YANSIMA = {
    "ben": "sen", "benim": "senin", "bana": "sana", "beni": "seni",
    "bende": "sende", "benden": "senden", "kendimi": "kendini",
    "kendime": "kendine", "kendim": "kendin",
    "annem": "annen", "babam": "baban", "ailem": "ailen", "kardeşim": "kardeşin",
}


def yansit(metin: str) -> str:
    """Zamirleri çevir: 'kendimi yalnız' → 'kendini yalnız'."""
    return " ".join(YANSIMA.get(k, k) for k in metin.split())


@dataclass
class Eliza:
    """Durumu yalnızca 'hangi yanıtı kaçıncı kez verdim' sayacından ibaret."""

    sayac: dict[int, int] = field(default_factory=dict)

    def _sec(self, anahtar: int, secenekler: list[str]) -> str:
        # Rastgele yerine sırayla seç: çıktı her çalıştırmada aynı olsun.
        i = self.sayac.get(anahtar, 0)
        self.sayac[anahtar] = i + 1
        return secenekler[i % len(secenekler)]

    def yanitla(self, cumle: str) -> str:
        temiz = cumle.strip().lower().rstrip(".!")
        for no, (kalip, yanitlar) in enumerate(KURALLAR):
            eslesme = re.search(kalip, temiz)
            if eslesme:
                parca = yansit(eslesme.group(1)) if eslesme.groups() else ""
                yanit = self._sec(no, yanitlar).format(parca.strip())
                return yanit[0].upper() + yanit[1:]
        return self._sec(-1, VARSAYILAN)


DIYALOG = [
    "Kendimi çok yalnız hissediyorum.",
    "Çünkü arkadaşlarım başka şehre taşındı.",
    "Annem de beni pek aramıyor.",
    "Sadece biraz daha mutlu olmak istiyorum.",
    "Evet, sanırım öyle.",
]

KIRILMALAR = [
    ("Hiçbir şey hissetmiyorum.", "olumsuzluğu yakalayamaz, genel cevaba düşer"),
    ("Kendimi iyi hissediyorum demek yalan olur.", "olumsuz anlamı kaçırır, cümleyi ters anlar"),
    ("Makine öğrenmesi dersini çok sevdim.", "'makine' kelimesine takılır, bağlamı kaçırır"),
    ("Sence ben kimim?", "soru olduğunu görür ama içeriğe dair hiçbir şey söyleyemez"),
]


def demo() -> None:
    print("=== ELIZA mini: hazır diyalog ===\n")
    eliza = Eliza()
    for cumle in DIYALOG:
        print(f"  Sen  : {cumle}")
        print(f"  ELIZA: {eliza.yanitla(cumle)}\n")

    print("=== Kırılma örnekleri: program hiçbir şey anlamıyor ===\n")
    for cumle, neden in KIRILMALAR:
        print(f"  Sen  : {cumle}")
        print(f"  ELIZA: {eliza.yanitla(cumle)}")
        print(f"         ↳ {neden}\n")

    print("Ders: Kısa bir sohbette ikna edici görünmek, anlamanın kanıtı değildir.")
    print("Turing testi davranışı ölçer; iç süreç hakkında hiçbir şey söylemez (bkz. Bölüm 27).")


def etkilesim() -> None:
    eliza = Eliza()
    print("ELIZA: Merhaba. Aklında ne var? (çıkmak için 'çıkış')")
    while True:
        try:
            cumle = input("Sen  : ")
        except EOFError:
            break
        if cumle.strip().lower() in {"çıkış", "cikis", "exit", "quit"}:
            break
        print(f"ELIZA: {eliza.yanitla(cumle)}")
    print("ELIZA: Görüşmek üzere.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--etkilesim", action="store_true", help="kendin sohbet et")
    args = ap.parse_args()
    etkilesim() if args.etkilesim else demo()


if __name__ == "__main__":
    main()
