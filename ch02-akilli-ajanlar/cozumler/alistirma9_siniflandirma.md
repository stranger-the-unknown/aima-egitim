# Çözüm — A9: Ortam sınıflandırma meydan okuması

| Eksen | Wordle | Borsa alım-satım | Mars gezgini |
|---|---|---|---|
| Gözlem | **Kısmi** (gizli kelimeyi görmez) | **Kısmi** (diğer yatırımcıların niyeti, gelecek haberler) | **Kısmi** (algılayıcı menzili, toz, gecikme) |
| Ajan | **Tek** (kelime rakip değil) | **Çok** (diğer alıcılar/satıcılar; rekabetçi) | **Tek** (dünya ile iletişim hariç) |
| Belirlilik | **Deterministik** (renkler kurala göre) | **Stokastik** | **Stokastik** (tekerlek kayması, aşınma) |
| Epizot | **Ardışık** (her tahmin sonrakini etkiler) | **Ardışık** (portföy birikir) | **Ardışık** |
| Statik | **Statik** | **Dinamik** (fiyat sen düşünürken değişir) | **Dinamik** (ışık, sıcaklık, batarya) |
| Ayrık | **Ayrık** | Fiyat pratikte **sürekli**, emir sayısı ayrık | **Sürekli** |
| Bilinen | **Bilinen** (kurallar açık) | **Bilinmeyen** (piyasa dinamikleri) | Kısmen bilinen (fizik bilinir, arazi bilinmez) |

## "Duruma göre değişir" noktaları (örnek)

1. **Borsa: tek mi çok mu ajanlı?** Küçük bir yatırımcı için diğer katılımcılar pratikte "hava durumu" gibidir; yani ortamın rastgele bir parçasıdır ve tek ajanlı stokastik ortam modeli yeterli olabilir. Büyük bir fon için ise kendi emirleri fiyatı etkiler ve diğerleri buna tepki verir. O zaman ortam açıkça çok ajanlıdır ve oyun teorisi gerekir.
2. **Wordle: deterministik mi?** Oyunun kuralları deterministiktir. Ama ajan, gizli kelimeyi bilmediği için onu bir *olasılık dağılımı* olarak düşünürse (hangi kelimeler hâlâ mümkün?), problem ajanın gözünden stokastik gibi ele alınabilir. Bu belirsizlik belirliliğin değil, **kısmi gözlemlenebilirliğin** sonucudur. İkisini karıştırmamak gerekir.
3. **Mars gezgini: statik mi?** Tek bir fotoğrafı analiz ederken kısa süreler için statik kabul edilebilir. Ama Dünya ile iletişim gecikmesi dakikalar sürdüğü için uzun planlarda ortam açıkça dinamiktir: Karar beklerken batarya azalır, güneş batar.
