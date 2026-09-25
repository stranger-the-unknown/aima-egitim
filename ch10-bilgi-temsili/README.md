# Bölüm 10 — Bilgi temsili

AIMA 4. baskı, Bilgi Temsili temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. **Kategori / nesne** sezgisini ve `is_a` kalıtımını açıklamak.
2. Ontolojileri hafifçe: ortak kelime dağarcığı + hiyerarşi ne işe yarar.
3. Olay / durum fikrini yüksek seviyede ayırt etmek (detaylı durum hesabı değil).
4. Varsayılan (default) / monotonic olmayan akıl yürütme sezgisini bir oyuncakla göstermek.
5. KR’nin amacını “ham FOL yığını”ndan ayırmak: yapı, yeniden kullanım, sorgulanabilirlik.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/ontoloji_mini.py` | Hayvan→Memeli→Kedi hiyerarşisi + `is_a` sorguları |
| `ornekler/varsayilan_akil.py` | Kuşlar uçar; penguen istisnası (default) |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da bilgi temsili / kategoriler bölümünü oku (yasal nüsha).
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/ontoloji_mini.py
   python ornekler/varsayilan_akil.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
