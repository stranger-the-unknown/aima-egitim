# A2 çözümü — Dikkat skoru

`dikkat_skoru.py` küçük Q ve K matrislerinden skor = Q @ K.T (isteğe bağlı √d ölçeği) hesaplar; satır softmaksı α üretir.

- Her satırın elemanları ≥ 0 ve toplamı ≈ 1 olmalıdır (softmaks tanımı).
- En yüksek α, o sorguda en büyük (ölçeklenmiş) nokta çarpımına sahip anahtara aittir: “en uyumlu anahtar”.
- V ile çarpım bu ağırlıklı ortalamayı bağlam vektörüne çevirir; demoda V basitleştirilmiş / basılabilir.

Gözlem: bir sorgu satırı + o satırın argmax anahtarı yeterli.
