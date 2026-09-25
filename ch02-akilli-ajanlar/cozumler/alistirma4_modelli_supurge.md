# Çözüm — A4: Modele dayalı süpürge

## 1. Adım sayıları (Senaryo 1: A ve B kirli, ajan A'da, en fazla 10 adım)

- **Basit refleks:** 10 adımın tamamını kullanır. Süpür → Sağ → Süpür, sonrasında durmadan Sol/Sağ yapar ("mekik").
- **Modele dayalı:** 4 adım: Süpür → Sağ → Süpür → Bekle. Her yer temiz olduğunu *bildiği* anda durur (kod "Durma" mesajını yazar).

## 2. Belleğin rolü

Ajanın algısı yalnızca **bulunduğu odayı** gösterir. B'deyken A'nın temiz olup olmadığını görmez. Basit refleks ajanı bu bilgiye sahip olmadığı için "belki diğer oda kirlenmiştir" ihtimaline karşı sürekli gider gelir. Modele dayalı ajan, A'yı temizlediğini **hatırlar**; A hakkındaki en iyi tahmini "temiz" olarak kalır. Bu yüzden B temizlenince iki odanın da temiz olduğunu çıkarabilir ve bekler.

Bu, kısmi gözlemlenebilirliğin klasik sonucudur: **Görmediğin şeyi takip etmek için iç duruma ihtiyacın var.**

## 3. Üçüncü oda (C) için tasarım notu

- Bellek sözlüğüne `Konum.C: BILINMIYOR` ekle.
- Hareket modelini genişlet: A–B–C bir koridorsa Sol/Sağ komşuya geçer.
- Karar kuralı: Bulunduğun oda kirliyse süpür. Değilse **bellekte kirli veya bilinmeyen en yakın odaya** doğru ilerle. Tüm odalar bilinen-temiz ise bekle.
- **Dikkat:** Odalar zamanla yeniden kirlenebiliyorsa, "temiz" bilgisi eskir. O zaman her bilginin **ne zaman** gözlendiğini de sakla ve belirli bir süre sonra durumu "bilinmiyor"a düşür. Bu, Bölüm 14'teki geçiş modeli fikrinin basit bir hâlidir: dünya sen bakmazken de değişir.
