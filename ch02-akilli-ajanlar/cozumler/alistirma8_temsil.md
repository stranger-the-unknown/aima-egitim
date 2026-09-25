# Çözüm — A8: Temsil türleri

| # | Görev | Temsil | Gerekçe |
|---|---|---|---|
| 1 | Metroda en kısa yol | **Atomik** | Durum yalnızca "hangi istasyondayım". İstasyonun iç yapısı arama için önemsiz; sadece komşuluk ve mesafe gerekir (Bölüm 3). |
| 2 | Çakışmasız sınav takvimi | **Ayrışık** | Her sınav bir *değişken*, değeri bir zaman dilimi. Kısıtlar değişkenler arasında ("aynı öğrenci iki sınava girmez"). Bu bir CSP'dir (Bölüm 6). |
| 3 | Aile ve okul ilişkileri | **Yapılandırılmış** | Nesneler (Ali, Ayşe, anne, kardeş) ve ilişkiler (`Anne(x,y)`, `Öğretmen(x,y)`) var. İlişkilerin birleşimi ("annesinin kardeşi") birinci derece mantık ister (Bölüm 8). |
| 4 | Belirtilerden hastalık olasılığı | **Ayrışık** | Ateş, öksürük, test sonucu ve hastalık birer *rastgele değişken*. Aralarındaki bağımlılıklar bir Bayes ağıyla modellenir (Bölüm 13). |

**Sınır durumlar:**
- 4. soru, **birden çok hasta** ve aralarındaki bulaşma ilişkileri eklenirse yapılandırılmış hâle gelir (birinci derece olasılık modelleri, Bölüm 15).
- 1. soru, "aktarma sayısı", "saat" ve "kalabalık" gibi öznitelikler eklenirse ayrışık bir temsile kayar.

**Genel kural:** Problemin çözümü için gereken *en az* ifade gücüne sahip temsili seç. Fazlası, akıl yürütmeyi ve öğrenmeyi gereksiz yere pahalı yapar.
