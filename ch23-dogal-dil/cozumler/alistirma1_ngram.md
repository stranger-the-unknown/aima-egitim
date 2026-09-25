# A1 çözümü — Bigram

`n_gram_mini.py` minik derlemden P(w'|w) tahmin eder (add-one yumuşatma varsa sıfır tamamen ölmez).

- Üretim: `<s>` ile başlayıp bigram’dan örnekleyerek kısa dizi basar; derlem küçük olduğu için tekrarlar / kısa kalıplar normaldir.
- Skor: derlemde görülen geçişler daha yüksek log-olasıılık alır.
- Hiç görülmemiş (veya çok seyrek) bigram: ham sayımda 0 → log skor −∞; yumuşatma ile küçük pozitif olasılık kalır ama yine düşük kalır.

Gözleminizi çıktıdan bir üretim satırı + bir skor satırı ile yazmanız yeterli.
