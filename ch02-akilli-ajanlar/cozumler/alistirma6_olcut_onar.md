# Çözüm — A6: Ölçütü kır, ölçütü onar

## 1. Hileci ajan neden kazanıyor?

"Süpürülen toz" ölçütü her başarılı `SUPUR` eylemine +1 veriyor. Hileci ajan:

1. A kirli → süpürür (+1), haznesi dolar.
2. A temiz, hazne dolu → tozu A'ya geri döker (`DOK`).
3. A yine kirli → yine süpürür (+1) … ve döngü sürer.

20 adımda 10 süpürme yapar, dürüst ajan ise yalnızca 2. Ölçüt **eylemi** (süpürme) ödüllendiriyor, **sonucu** (temiz zemin) değil. Hileci ajan da bu boşluğu kullanıyor. Üstelik B hiç temizlenmiyor.

## 2. Hareket cezası

`cozumler/alistirma6_olcut_onar.py` çıktısı:

```
dürüst (refleks)   →   29.0 puan
modele dayalı      →   37.5 puan
```

Dürüst refleks ajanı artık **en iyi değil**: İş bittikten sonra her adımda gidip geldiği için ceza topluyor. Modele dayalı ajan iki odanın temiz olduğunu bilince duruyor. Bu, notlardaki "varsayımları değiştir, rasyonel ajan değişir" örneğinin sayısal hâlidir.

## 3. "Temiz zemin" ölçütü de istismar edilebilir mi?

Evet, ölçüt **algılayıcıdan** okunuyorsa:

- Ajan kir algılayıcısını örten bir eylem bulursa ("kamerayı duvara çevir"), algılayıcı hep "temiz" der ve puan hep yüksek görünür.
- "Temiz" tanımı yalnızca görünen yüzeyi kapsıyorsa, tozu halının altına süpürmek puan kazandırır.

Bu durum hem ölçütün hem de ortam modelinin eksikliğidir. Ölçüt, **dünyanın gerçek durumunu** ölçmeli; ajanın değiştirebileceği bir göstergeyi değil. Pekiştirmeli öğrenmede buna **ödül hackleme** (*reward hacking*) veya **kablo sapma** (*wireheading*) denir (Bölüm 22 ve 27).
