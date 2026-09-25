# Bölüm 22 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Pekiştirmeli öğrenmede ajan ortama ne gönderir, ortam ajanına tipik olarak ne döner?

**S2.** Getiri (return) ile anlık ödül farkı nedir?

**S3.** Q-öğrenme güncellemesinde `max_{a'} Q(s', a')` neyi temsil eder?

**S4.** ε-açgözlü politikada ε’nun rolü nedir?

**S5.** Model-free RL’de “model” ne anlama gelir ve neden “free” denir?

---

## Cevaplar

**S1.** Ajan eylem gönderir; ortam genelde ödül ve sonraki durumu (gözlemi) döner.

**S2.** Ödül tek adımlık sinyal; getiri bundan sonraki indirimli ödül toplamıdır.

**S3.** Sonraki durumda açgözlü (en yüksek Q’lu) devam varsayımıyla hedef değeri.

**S4.** Olasılık ε ile rastgele keşif; 1−ε ile mevcut en iyi eylemi sömürme.

**S5.** Model = geçiş / ödül fonksiyonunun açık bilgisi; model-free ajan T ve R’yi bilmeden deneyimden öğrenir.
