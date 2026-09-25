# Bölüm 5 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Minimax sezgisi

Küçük bir ağaç düşünün: Kök MAX; iki çocuk MIN; her MIN’in iki yaprağı var. Yaprağın utility’leri soldan sağa: 3, 5, 2, 9.

1. Sol MIN düğümünün değeri nedir? Sağ MIN?
2. Kök MAX hangi çocuğu seçer? Utility kaç olur?
3. “Rakip en iyi oynar” varsayımı burada nerede kullanıldı?

## A2 — Alpha-beta fikri

Alpha-beta, minimax ile **aynı hamleyi** mi üretir yoksa yaklaşık mı? Budama neyi “keser”? α ve β’yı birer cümleyle tanımlayın.

## A3 — XOX ajan-ajan

```bash
python ornekler/minimax_tictactoe.py --mod ajan-ajan
python ornekler/minimax_tictactoe.py --mod ajan-ajan --alpha-beta
```

1. Oyun nasıl bitti? Neden bu sonuç “doğal”?
2. İlk turda incelenen düğüm sayısını iki koşuda karşılaştırın (çıktıdaki ≈ değer).

## A4 — Pozisyondan hamle

```bash
python ornekler/minimax_tictactoe.py --mod en-iyi --tahta "X.O.X.O.."
```

Sıra kimde? Önerilen hücre ve beklenen utility nedir? Utility +1/0/−1 anlamını yazın.

## A5 — Değerlendirme fonksiyonu

Satrançta derinlik 4’te kesip `eval` kullanıyorsunuz. Bu neden **kusurlu karar**? “Ufuk etkisi”ni kendi cümlelerinizle bir örnekle açıklayın (taş kaybı bir hamle ötede görünmesin gibi).
