# Bölüm 4 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Yerel arama ne zaman? ★

Aşağıdaki iki senaryodan hangisi **yerel arama** için daha uygun? Neden? (3–4 cümle)

1. Haritada A şehrinden B'ye en kısa yolu bulmak; yolu adım adım raporlamak istiyoruz.
2. 50 dersi 10 sınıfa, çakışma ve kapasite kısıtlarıyla yerleştirmek. Ara atamalar önemli değil, yalnızca geçerli bir son atama istiyoruz.

## A2 — Tepe tırmanma tuzakları ★

"Yerel maksimum", "düzlük" ve "sırt" kavramlarını kendi örnek cümlelerinle tanımla. Rastgele yeniden başlatma bunlardan hangisine doğrudan yardımcı olur, hangisine tek başına yetmeyebilir?

## A3 — 8-vezir deneyi ★

```bash
python ornekler/tepe_tirmanma_n_queens.py --deney 2000
python ornekler/tepe_tirmanma_n_queens.py --yeniden-baslat 50
python ornekler/tepe_tirmanma_n_queens.py --yeniden-baslat 50 --yana 100
```

1. Deneydeki başarı oranlarını ve adım sayılarını kitaptaki değerlerle karşılaştır.
2. Yeniden başlatmalı sürümde beklenen toplam adım sayısını, "bir başarılı deneme + (1 − p)/p başarısız deneme" formülüyle hesapla (yana hamle olmadan ve 100 yana hamleyle).
3. h ne sayıyor? h = 0 neden bir çözümdür?

## A4 — Benzetilmiş tavlama ★★

`ornekler/simule_tavlama_demo.py` için:

1. Sıcaklık yüksekken "kötü" bir tur neden kabul edilebilir? ΔE = −2 için T = 10 ve T = 0,1'de kabul olasılıklarını hesapla.
2. `--soguma 0.5` ile çalıştır (çok hızlı soğuma). Ne oluyor, neden?
3. 30 şehirlik karşılaştırmada tavlama tepe tırmanmadan ortalamada kaç birim daha iyi? Bu farkı artırmak için hangi parametreyi değiştirirdin?

## A5 — Çevrimiçi arama ve inanç ★

Bir robot bir labirenti **ilk kez** keşfediyor; harita yok. Algılayıcı yalnızca bitişik duvarları görüyor.

1. Bu çevrimdışı mı, çevrimiçi arama mı?
2. Robot başlangıç konumunu da bilmiyorsa, "inanç durumu" neyin kümesi olur?
3. Robotun bir çukura düşebileceği (geri dönüşsüz) kareler varsa ne değişir?

## A6 — GA parametreleri (kod) ★★

`ornekler/genetik_8vezir.py` içindeki `genetik_algoritma` fonksiyonunu kullan.

1. Mutasyon olasılığı 0,0; 0,1; 0,6 ve seçim türü "orantılı" ve "turnuva" için 20'şer farklı tohumla çalıştır. Her ayar için 1000 nesil içindeki başarı oranını ve ortalama nesil sayısını tablo yap.
2. Mutasyon 0 iken ne oluyor? Neden?
3. Elitizmi kapat (`elit=0`). Sonuç nasıl değişiyor?

## A7 — Kaygan süpürge (kod) ★★★

`ornekler/and_or_supurge.py`'yi kopyalayıp süpürge dünyasını **kaygan** yap: Süpür deterministik (yalnızca bulunduğu kareyi temizler), ama Sağ ve Sol **bazen** ajanı yerinde bırakır.

1. SONUÇLAR(1, Sağ) nedir?
2. AND-OR araması durum 1'den bir plan bulabiliyor mu? Bulamıyorsa neden?
3. Durum 5 (ajan solda, yalnız sağ kirli) için "başarana kadar dene" türünden döngüsel bir plan yaz. Bu planın her zaman işe yaraması için hangi varsayım gerekir?

## A8 — Üç kareli algısız süpürge (kod) ★★

Süpürge dünyasını üç kareye (Sol, Orta, Sağ) genişlet. Ajan hiçbir şey algılamıyor ve Sol/Sağ eylemleri deterministik.

1. Kaç fiziksel durum var? Başlangıç inancı nedir?
2. `inanc_durumu_supurge.py`'deki BFS'i uyarlayarak en kısa algısız planı bul.
3. Planın uzunluğunu iki kareli durumla karşılaştır. Neden bu kadar uzun?

## A9 — Adım büyüklüğü (kod) ★★

`ornekler/havalimani_gradyan.py` içindeki `gradyan_inisi` fonksiyonunu α = 0,001; 0,01; 0,03; 0,1 için aynı başlangıçtan çalıştır.

1. Her α için 300 adım sonundaki f değerini yaz.
2. Hangi α "fazla büyük"? Nereden anladın?
3. Newton adımı neden α seçme derdini ortadan kaldırıyor?

## A10 — LRTA* ve sezgisel kalitesi ★★

`ornekler/lrta_yildiz.py`'deki labirentte:

1. h = 0 (bilgisiz) ile LRTA*'ı 15 deneme çalıştır. Kaçıncı denemede optimal yola oturuyor? Manhattan sezgiseliyle karşılaştır.
2. Manhattan uzaklığını 3 ile çarparsan (kabul edilemez sezgisel) ne olur? Ajan yine hedefi buluyor mu? Optimal yolu öğreniyor mu?
3. "Belirsizlik karşısında iyimserlik" bu deneyde nasıl kendini gösteriyor?
