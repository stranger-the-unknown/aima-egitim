# Bölüm 22 — Pekiştirmeli öğrenme

AIMA 4. baskı (US) *Reinforcement Learning* temalarıyla uyumlu **özgün Türkçe** öğrenme paketi.
Ajan–ortam döngüsü, ödül / getiri, TD ve Q-öğrenme sezgisi, keşif–sömürü dengesi.
Saf numpy ile küçük gridworld Q-öğrenme ve epsilon-açgözlü bandit; kitap metni yok.

**Durum:** 🟢 hazır

## Öğrenme hedefleri

1. Ajan–ortam etkileşim döngüsünü (durum, eylem, ödül, sonraki durum) açıklamak.
2. Anlık ödül ile indirimli getiri (return) farkını bilmek.
3. TD / Q-öğrenme güncellemesinin sezgisini özetlemek (model bilmeden öğrenme).
4. Keşif (exploration) ile sömürü (exploitation) gerilimini örneklemek.
5. Küçük bir gridworld’de Q tablosu ve açgözlü politika üretmek; banditte ε-açgözlü denemek.

## Bu klasörde ne var?

| Dosya / klasör | İçerik |
|----------------|--------|
| `notlar.md` | Özgün Türkçe öğretim notları |
| `ornekler/q_ogrenme_grid.py` | 3×2 gridworld Q-öğrenme; Q ve politika yazdırır |
| `ornekler/epsilon_greedy_bandit.py` | Çok kollu bandit ε-açgözlü demo |
| `alistirmalar.md` | 5 özgün alıştırma |
| `cozumler/` | A1 ve A2 çözümleri |
| `quiz.md` | 5 soru + cevaplar |

## Nasıl çalış?

1. AIMA’da pekiştirmeli öğrenme bölümünü oku (yasal nüsha). Bölüm 17 MDP notlarını hatırla.
2. `notlar.md` ile pekiştir.
3. Örnekleri çalıştır:
   ```bash
   python ornekler/q_ogrenme_grid.py
   python ornekler/epsilon_greedy_bandit.py
   ```
4. Alıştırmalar → `cozumler/` → `quiz.md`.

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
