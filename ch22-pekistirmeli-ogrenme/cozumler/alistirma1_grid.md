# A1 çözümü — Gridworld Q

`q_ogrenme_grid.py` varsayılan 3×2 (veya benzeri küçük) ızgarada eğitir.

Beklenen gözlemler (seed’e göre hafif değişebilir):

- Hedef / yüksek ödüllü hücreye giden oklar (politika) genelde kısa yolu tercih eder.
- Negatif ödüllü veya tuzak hücreye giren eylemlerin Q değeri düşük kalır → açgözlü politika onlardan kaçınır.
- Yeterli epizot + makul ε sonrası Q tablosunda hedefe yakın (s,a) çiftleri daha yüksek görünür.

Kendi çıktınızda politika ızgarasını ve Q satırlarını notlara yapıştırıp “kaçınılan hücre / tercih edilen yön” diye iki cümle yazmanız yeterli.
