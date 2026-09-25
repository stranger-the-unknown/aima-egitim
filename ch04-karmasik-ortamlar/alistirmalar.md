# Bölüm 4 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Yerel arama ne zaman?

Aşağıdaki iki senaryodan hangisi **yerel arama**ya daha uygun? Neden? (3–4 cümle)

1. Haritada A şehrinden B’ye en kısa yolu bulmak; yolu adım adım raporlamak istiyoruz.
2. 50 dersi 10 sınıfa, çakışma ve kapasite kısıtlarıyla yerleştirmek; hangi ara atamaların yapıldığı önemli değil, sadece geçerli bir final atama istiyoruz.

## A2 — Tepe tırmanma tuzakları

“Yerel maksimum”, “plato” ve “sırt”ı kendi örnek cümlelerinizle tanımlayın. Rastgele yeniden başlatma bu tuzakların hangisine doğrudan yardımcı olur? Hangisine tek başına yetmeyebilir?

## A3 — N-vezir deneyi

`ornekler/tepe_tirmanma_n_queens.py` çalıştırın:

```bash
python ornekler/tepe_tirmanma_n_queens.py --tohum 1
python ornekler/tepe_tirmanma_n_queens.py --yeniden-baslat 30 --tohum 1
```

1. Tek koşuda saldırı 0 oldu mu?
2. Yeniden başlatmada kaçıncı denemede (veya en iyi saldırı) ne çıktı?
3. Saldırı metriği ne sayıyor? Bir cümle.

## A4 — Simüle tavlama

`simule_tavlama_demo.py` için:

1. Sıcaklık yüksekken neden “kötü” bir tur kabul edilebilir?
2. `soguma` 0.5 olsaydı (çok hızlı soğuma) ne risk doğardı?
3. Rastgele tur maliyeti ile SA maliyetini kendi koşunuzda yazın.

## A5 — Çevrimiçi vs inanç

Kısa senaryo: Robot labirenti **ilk kez** keşfediyor; harita yok. Sensör yalnızca bitişik duvarları görüyor.

1. Bu **çevrimdışı** mı **çevrimiçi** arama?
2. “İnanç durumu” burada neyin kümesi olurdu?
