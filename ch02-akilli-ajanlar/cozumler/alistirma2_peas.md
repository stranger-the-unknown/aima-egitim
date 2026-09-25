# Çözüm — A2: PEAS + ortam

## PEAS (örnek doldurma)

| | |
|--|--|
| **P** | Kullanıcı memnuniyeti, rezervasyon oranı, iptal azlığı, yanıt süresi |
| **E** | Restoranlar, müsait masalar, diğer kullanıcılar, trafik/hava |
| **A** | Öneri listesi gösterme, rezervasyon isteği gönderme, bildirim |
| **S** | GPS, kullanıcı tercihleri, API’den müsaitlik, puanlar |

## Ortam eksenleri

| Eksen | Sınıf | Gerekçe |
|-------|--------|---------|
| Gözlem | Kısmi | Tüm restoranların anlık iç durumu ve diğer kullanıcı niyetleri görünmez |
| Determinizm | Stokastik | Masa “müsait” görünüp anında dolabilir; ağ gecikmesi |
| Dinamiklik | Dinamik | Öneri üretilirken stok ve talepler değişebilir |
| Ajan | Çok | Diğer müşteriler ve restoran sistemleri de karar verir |
