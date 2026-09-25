# A1 çözümü — Lokalizasyon gözlemi

`grid_lokalizasyon.py` uniform inançla başlar; tüm serbest hücreler eşit olasılıklıdır.

İlk adımda sağa hareket + **A** gözlemi:

- Predict inancı sağa kaydırır (gürültüyle yayar).
- Update, A landmark’ı olan hücreyi (ve duyucu modeline göre komşuları) yükseltir; A olmayan hücreleri bastırır.

Sonuçta MAP genelde A’nın hücresine (veya çok yakınına) oturur; P değeri belirgin yükselir. Sonraki “yok” ve “B” gözlemleri inancı koridor boyunca gerçek yola doğru çeker.
