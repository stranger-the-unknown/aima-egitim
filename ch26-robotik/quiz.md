# Bölüm 26 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Robotikte algı–eylem döngüsünün üç ana adımı nedir?

**S2.** Konfigürasyon uzayı (C-space) neyi temsil eder?

**S3.** Lokalizasyon ile haritalama arasındaki fark nedir?

**S4.** Yol planlama ile kontrolü bir cümlede ayırın.

**S5.** Potansiyel alan yönteminin tipik zayıf yanı nedir?

---

## Cevaplar

**S1.** Algıla → durumu tahmin et → eylem uygula (tekrarla).

**S2.** Robotun tüm serbestlik derecelerinin (konum, eklem açıları vb.) oluşturduğu uzay; çarpışmasız / çarpışmalı bölgeler burada tanımlanır.

**S3.** Lokalizasyon: harita biliniyorken konum tahmini. Haritalama: konum (kabaca) biliniyorken çevre modeli. SLAM ikisini birlikte yapar.

**S4.** Planlama “nereye / hangi yoldan?”; kontrol “bu an motorlara hangi komut?” sorusuna cevap verir.

**S5.** Yerel minimum (veya dar geçitte sıkışma); global optimum / tamamlanmışlık garantisi yoktur.
