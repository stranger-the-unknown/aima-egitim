# Bölüm 22 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Gridworld Q

```bash
python ornekler/q_ogrenme_grid.py
```

Eğitim sonrası açgözlü politikada hedef hücresine giden yollar mantıklı mı? Engel / ceza hücresinden kaçınılıyor mu? Kısa gözlem yazın.

## A2 — Bandit ε

```bash
python ornekler/epsilon_greedy_bandit.py
```

ε = 0.1 ile ortalama ödül nasıl ilerliyor? ε = 0 (saf açgözlü) ve ε = 0.5 ile kısa karşılaştırma yapın (kodda `epsilon` değiştirerek).

## A3 — Ödül vs getiri

Bir epizotta ödüller: +1, 0, +2, −1 ve γ = 0.9. t=0’daki getiriyi (G_0) hesaplayın.

## A4 — Keşif–sömürü

Yeni bir ortamda ε’yu sürekli 0 tutarsanız ne risk vardır? Sürekli 1 tutarsanız? Birer cümle.

## A5 — α ve γ

Q-öğrenmede α’yı çok büyütürseniz / çok küçültürseniz tipik sorun nedir? γ → 1’e yaklaşınca ajanın “ufku” nasıl değişir? (3–5 cümle)
