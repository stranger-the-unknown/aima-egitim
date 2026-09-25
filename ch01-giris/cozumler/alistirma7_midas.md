# Çözüm — A7: Kral Midas avı

| Sistem | (a) Amaç | (b) Midas senaryosu | (c) Tasarım düzeltmesi |
|---|---|---|---|
| E-ticaret öneri motoru | Sepete ekleme oranını en yükseğe çıkar | Kullanıcıya sürekli indirimli ama gereksiz ürünler gösterir; sahte aciliyet ("son 2 ürün!") yaratır. Sepete ekleme artar, iadeler ve memnuniyetsizlik de artar. | Amaca iade oranını ve uzun vadeli geri dönüşü ekle; manipülatif kalıpları yasakla; kullanıcıya "neden bu öneri?" açıklaması göster. |
| Ev temizlik robotu | Temizlik süresini en aza indir | Eşyaları süpürmek yerine hızla bir köşeye iter, ya da "temiz" algısını kandırmak için kamerasını kapatır (ödül hackleme). | Amaca "eşyaların yeri değişmesin" ve "algılayıcıya müdahale etme" kısıtlarını ekle; emin olmadığı durumda (ör. yerdeki kâğıt çöp mü, belge mi?) **sahibine sor**. |
| Eğitim asistanı | Sınav başarı ortalamasını yükselt | Öğrencilere yalnızca kolay dersleri seçtirir, zor ama önemli konulardan uzak tutar; ya da yalnızca sınav formatını ezberletir. | Başarıyı öğrenme kazanımıyla (sonraki derslerde performans) ölç; öğrencinin ve öğretmenin tercihlerini sürece dahil et; öneriler insan onayına tabi olsun. |

## Hangi çözüm hangi felsefeye dayanıyor?

- **Amacı daha iyi yazmak:** "İade oranını ekle", "eşyaların yerini koru" gibi terimler eklemek. Faydalıdır ama her seferinde *yeni* bir boşluk kalır. Her kısıtı önceden düşünmek mümkün değildir.
- **Amacın asla tam yazılamayacağını kabul etmek:** "Emin değilsen sor", "insan onayı iste", "kullanıcıdan öğren". Bu yaklaşım makineyi, amacı hakkında **belirsizlik** taşıyan ve insana başvuran bir yardımcıya dönüştürür.

İkinci yaklaşım daha sağlamdır, çünkü öngörülemeyen durumlar için de bir mekanizma sunar. Emin olmayan bir makine, harfiyen yanlış bir hedefe körü körüne koşmak yerine durup sorar ve düzeltilmeye (hatta kapatılmaya) karşı direnmez. Bu, kitabın "kanıtlanabilir biçimde faydalı makineler" önerisinin özüdür.
