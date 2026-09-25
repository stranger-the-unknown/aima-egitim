# Çözüm — A6: ELIZA'yı kır, sonra düzelt

## 1. Yeni kural

`KURALLAR` listesine, genel kuralların (soru işareti, evet/hayır) **önüne** ekle:

```python
(r"(.*?)(?:den|dan|ten|tan) korkuyorum", ["Bu korku ne zaman başladı?",
                                          "{0} seni en çok hangi durumda korkutuyor?"]),
```

Deneme: `Karanlıktan korkuyorum.` → `Bu korku ne zaman başladı?`

İkinci yanıtın `{0}` kısmında "karanlık" yerine ekli hâlin nasıl kalacağına dikkat et. Türkçe ek yapısı ELIZA'nın kopyala-yapıştır hilesini çabucak bozar.

## 2. Saçmalatan cümleler (örnekler)

| Cümle | Ne olur? | Zayıflık |
|---|---|---|
| `Kendimi iyi hissediyorum demek yalan olur.` | "Kendini iyi hissetmek sana neyi hatırlatıyor?" | **Olumsuzluk / kapsam:** Cümlenin asıl anlamı tam tersi. |
| `Babamın arabası bozuldu.` | Hiçbir aile kuralı tetiklenmez ("babamın" ≠ "babam") | **Ek yapısı:** Kelime sınırı + tam eşleşme, Türkçe çekimleri kaçırır. |
| `Yüz yüze konuşmak istiyorum.` | "Neden yüz yüze konuşmak istiyorsun?" (anlamlı görünür) ama `Ölmek istemiyorum.` genel cevaba düşer | **Olumsuzluk:** "istemiyorum" kalıba uymaz. |
| `Robot süpürgem çok iyi çalışıyor.` | "Makineler seni endişelendiriyor mu?" | **Bağlam:** Anahtar kelimeye tepki verir, duyguyu okuyamaz. |

## 3. Üç soruda ELIZA'yı ele verme stratejisi

- **Bilgi ve hafıza sorusu:** "Az önce sana annem hakkında ne demiştim?" ELIZA'nın sohbet hafızası yoktur.
- **Sağduyu / çözümleme sorusu (Winograd tarzı):** "Kupa bavula sığmadı çünkü o çok büyüktü. 'O' neyi kastediyor?" Bunu doğru yanıtlamak dünya bilgisi ister.
- **Basit bir hesap ya da talimat:** "Lütfen sadece 'mavi' kelimesiyle cevap ver." ELIZA talimatı izleyemez.

Bu sorular işe yarar çünkü **içeriği anlamayı** gerektirir. ELIZA ise yalnızca **biçimi** dönüştürür.

## 4. "Turing testini geçmek zekânın kanıtıdır" iddiasına karşı

Turing testi yalnızca kısa bir yazışmadaki *davranışı* ölçer. ELIZA gibi kalıp tabanlı programların 1960'larda bile bazı insanları kandırması, testin sonucunun sorgucunun becerisine, sohbetin süresine ve konunun sınırlarına çok bağlı olduğunu gösterir. Üstelik aynı davranış çok farklı iç süreçlerle üretilebilir: bir sözlükten bakmak ile gerçekten anlamak dışarıdan aynı görünebilir. Bu yüzden testi geçmek *yeterli* bir zekâ kanıtı değildir. AI araştırmasının çoğu da testi geçmeyi değil, tanımlı görevlerde rasyonel davranmayı hedefler. (Karşı görüşler ve Searle'ün Çin odası argümanı için bkz. Bölüm 27.)
