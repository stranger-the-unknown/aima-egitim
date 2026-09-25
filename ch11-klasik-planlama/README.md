# Bölüm 11 — Otomatik planlama

> AIMA 4. baskı, Bölüm 11 · *Automated Planning*

## Öğrenme hedefleri

1. Bir planlama problemini PDDL ile tanımlamak: başlangıç, hedef, eylem şemaları.
2. İleri ve geri aramayı, planlama grafiğini ve SAT tabanlı planlamayı karşılaştırmak.
3. Gevşetilmiş problemlerden alana bağımsız sezgiseller türetmek (h_max, h_add, seviye toplamı).
4. Hiyerarşik planlamanın neden büyük problemlerde işe yaradığını açıklamak.
5. Kritik yol yöntemiyle çizelge hesaplamak ve kaynak kısıtlarının etkisini göstermek.

## Çalışma sırası

1. Kitapta Bölüm 11'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/planlama.py` | Kütüphane: eylem şemaları, temellendirme, ileri arama (BFS / A*), h_max, h_add, planlama grafiği seviyeleri, geri arama için ilgili eylemler |
| `ornekler/kitap_problemleri.py` | Hava kargo, yedek lastik, bloklar dünyası; sezgisel karşılaştırması; Sussman anomalisi |
| `ornekler/kritik_yol.py` | İki arabalık montaj: kritik yol yöntemi (85 dk), kaynak kısıtlarıyla çizelge (115 dk) |
| `ornekler/hiyerarsik_plan.py` | Üst düzey eylemler ve inceltmeler; özyineli Yürü inceltmesi |
| `ornekler/strips_bloklar.py` | Elli bloklar dünyası (Kaldır / Koy / MasayaKoy) + BFS |
| `ornekler/aksiyon_semasi.py` | Eylem şemalarını okunaklı yazdırma |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A4, A6–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch11_planlama.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Hava kargo planı | 6 adım (iki Load, iki Fly, iki Unload) | ✔ |
| Yedek lastik planı | Remove(Flat,Axle), Remove(Spare,Trunk), PutOn(Spare,Axle) | ✔ |
| Bloklar dünyası planı | MoveToTable(C,A), Move(B,Table,C), Move(A,Table,B) | ✔ |
| Sussman anomalisi | Alt hedefler tek tek çözülünce hedef sağlanmaz | ✔ |
| Kritik yol (kaynaksız) | 85 dk; [ES, LS] değerleri; üst işin bolluğu 15 | ✔ |
| Kaynak kısıtlarıyla | 115 dk | ✔ |
