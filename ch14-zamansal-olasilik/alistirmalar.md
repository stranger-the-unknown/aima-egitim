# Bölüm 14 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Geçiş vs duyucu

Bir cümleyle ayırt edin:

1. Geçiş modeli ne sorar?
2. Duyucu modeli ne sorar?

Kodda `GECIS` ve `P_SEMSIYE_VER_DURUM` hangi role karşılık gelir?

## A2 — Filtreleme adımı

`hmm_filtreleme.py` çalıştırın. Gözlem dizisinde **3. adım** (Şemsiye=F) sonrası `P(Yagmur=T)` yaklaşık kaç?
Neden bir önceki adıma göre düşüyor (bir cümle)?

## A3 — Üç soru

Filtreleme, kestirim (prediction) ve yumuşatma (smoothing) için her birine bir cümlelik “ne sorar?” yazın.

## A4 — Viterbi vs marjinal

```bash
python ornekler/viterbi_kucuk.py
```

Viterbi yolu ile marjinal argmax aynı mı? Farklıysa bu ne anlama gelir?

## A5 — Kalman sezgisi

HMM ayrık durum kullanır. Kalman filtresi hangi tür durumda “doğal kuzen”dir?
Predict–update döngüsü HMM ile ortak mı?
