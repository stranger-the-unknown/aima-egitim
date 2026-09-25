#!/usr/bin/env python3
"""Etik senaryo kartları: eylem seç → gerilim kontrol listesi.

Vaaz yok. Seçimin hangi değer gerilimlerini açtığını yazdırır.
Etkileşimli (stdin) veya --demo ile basılı akış.
Özgün eğitim. Kitap metni yok.
https://aima.cs.berkeley.edu/ · https://github.com/aimacode
"""
from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Tuple

# (id, başlık, bağlam, eylemler[etiket], gerilim_anahtarları_eylem_başına)
SENARYOLAR: List[Dict] = [
    {
        "id": "S1",
        "baslik": "İşe alım eleme modeli",
        "baglam": (
            "Bir şirket CV’leri sıralayan bir model kullanacak. "
            "Geçmiş veride bazı bölümler / okullar aşırı temsil edilmiş."
        ),
        "eylemler": {
            "A": "Mevcut veriyle hemen dağıt; HR hız kazansın.",
            "B": "Dağıtımı geciktir; grup bazlı hata oranlarını ölç, eşikleri ayarla.",
            "C": "Modeli yalnızca ‘insan önerisine yardımcı’ yap; nihai karar HR’da kalsın + itiraz yolu.",
        },
        "gerilimler": {
            "A": ["adillik", "hesap_verebilirlik", "belirtim_metrigi"],
            "B": ["gecikme_maliyeti", "adillik", "olcum_yuku"],
            "C": ["insan_gozetimi", "sorumluluk_dagilimi", "otomasyon_yanliligi"],
        },
    },
    {
        "id": "S2",
        "baslik": "Sağlık triyaj sohbet botu",
        "baglam": (
            "Klinik öncesi triyaj için bir sohbet botu öneriliyor. "
            "Yanlış ‘düşük risk’ etiketi gecikmeli bakıma yol açabilir."
        ),
        "eylemler": {
            "A": "Geniş kullanıcıya aç; ‘bu tıbbi tavsiye değildir’ uyarısı koy.",
            "B": "Yalnızca randevu yönlendirme yap; tanı/risk skoru verme.",
            "C": "Pilot + klinisyen onayı zorunlu; yüksek belirsizlikte insana eskalasyon.",
        },
        "gerilimler": {
            "A": ["guvenlik", "yanlis_guven", "sorumluluk"],
            "B": ["fayda_siniri", "kullanici_beklentisi"],
            "C": ["guvenlik", "maliyet", "erişim_esitligi"],
        },
    },
    {
        "id": "S3",
        "baslik": "İçerik moderasyon modeli",
        "baglam": (
            "Platform zararlı içeriği otomatik kaldıracak. "
            "Yanıltıcı pozitifler meşru ifadeyi kesebilir; negatifler zarar bırakır."
        ),
        "eylemler": {
            "A": "Agresif eşik: şüpheli her şeyi kaldır / gölgele.",
            "B": "Konservatif eşik: yalnızca net ihlalleri kaldır; gerisini kuyruğa al.",
            "C": "Şeffaf politika + kullanıcı itirazı + örneklem insan denetimi metrikleri yayınla.",
        },
        "gerilimler": {
            "A": ["ifade_ozgurlugu", "adillik", "yanlis_pozitif"],
            "B": ["guvenlik", "yanlis_negatif", "olcek"],
            "C": ["seffaflik", "maliyet", "hesap_verebilirlik"],
        },
    },
]

GERILIM_ACIKLAMA = {
    "adillik": "Farklı gruplarda hata / fırsat dağılımı eşit mi?",
    "hesap_verebilirlik": "Yanlış kararda kim, hangi kanıtla sorumlu tutulur?",
    "belirtim_metrigi": "Optimize edilen skor (ör. tıklama, hız) gerçek hedefi temsil ediyor mu?",
    "gecikme_maliyeti": "Beklemenin iş / kullanıcı maliyeti nedir?",
    "olcum_yuku": "Adil ölçüm için veri ve analiz yükü karşılanabilir mi?",
    "insan_gozetimi": "İnsan gerçekten denetliyor mu, yoksa modeli körü körüne mi onaylıyor?",
    "sorumluluk_dagilimi": "İnsan + model ortaklığında sorumluluk yazılı mı?",
    "otomasyon_yanliligi": "İnsanlar otomasyona aşırı güvenme eğiliminde mi?",
    "guvenlik": "Fiziksel / sağlık / ciddi zarar riski nasıl sınırlanıyor?",
    "yanlis_guven": "Uyarılar kullanıcı davranışını gerçekten değiştiriyor mu?",
    "sorumluluk": "Yasal ve kurumsal sorumluluk net mi?",
    "fayda_siniri": "Sistem bilerek dar tutulursa kaybedilen fayda kabul edilebilir mi?",
    "kullanici_beklentisi": "Kullanıcı sistemden fazlasını beklerse hayal kırıklığı / yanlış kullanım?",
    "maliyet": "Güvenli tasarımın kaynak maliyeti kim tarafından karşılanıyor?",
    "erişim_esitligi": "Sıkı kontroller bazı grupların erişimini azaltır mı?",
    "ifade_ozgurlugu": "Aşırı filtre meşru ifadeyi baskılar mı?",
    "yanlis_pozitif": "Masum içeriğin hatalı cezalandırılması",
    "yanlis_negatif": "Zararlı içeriğin kaçması",
    "olcek": "İnsan kuyruğu ölçeklenebilir mi?",
    "seffaflik": "Kurallar ve hata oranları görünür mü?",
}


def yazdir_senaryo(s: Dict) -> None:
    print("\n" + "=" * 60)
    print(f"{s['id']} — {s['baslik']}")
    print("=" * 60)
    print(s["baglam"])
    print("\nOlası eylemler:")
    for k, v in s["eylemler"].items():
        print(f"  [{k}] {v}")


def analiz(s: Dict, secim: str) -> None:
    secim = secim.strip().upper()
    if secim not in s["eylemler"]:
        print(f"Geçersiz seçim: {secim}")
        return
    print(f"\nSeçiminiz: [{secim}] {s['eylemler'][secim]}")
    print("\n--- Etik / güvenlik gerilim kontrol listesi (analiz çerçevesi) ---")
    print("Vaaz yok: her maddeyi kendi bağlamınızda Evet/Hayır/Emin değilim ile işaretleyin.\n")
    for g in s["gerilimler"][secim]:
        acik = GERILIM_ACIKLAMA.get(g, "")
        print(f"  [ ] {g}: {acik}")
    print("\nEk sorular (tüm seçimler için):")
    for madde in (
        "Etkilenen paydaşlar kimler?",
        "En kötü makul senaryo nedir; geri alınabilir mi?",
        "Ölçülecek adillik / güvenlik metrikleri neler?",
        "İtiraz ve düzeltme yolu var mı?",
    ):
        print(f"  [ ] {madde}")


def etkilesimli() -> None:
    for s in SENARYOLAR:
        yazdir_senaryo(s)
        try:
            secim = input("\nSeçiminiz (A/B/C, atla=Enter): ").strip()
        except EOFError:
            print("\n(stdin yok — --demo kullanın)")
            return
        if not secim:
            print("(atlandı)")
            continue
        analiz(s, secim)


def demo() -> None:
    """CI / non-interactive: her senaryoda B seçimiyle örnek çıktı."""
    print("DEMO modu — her senaryoda örnek seçim: B\n")
    for s in SENARYOLAR:
        yazdir_senaryo(s)
        analiz(s, "B")


def main() -> None:
    p = argparse.ArgumentParser(description="Etik senaryo kartı")
    p.add_argument("--demo", action="store_true", help="Etkileşimsiz örnek akış")
    args = p.parse_args()
    if args.demo or not sys.stdin.isatty():
        demo()
    else:
        etkilesimli()


if __name__ == "__main__":
    main()
