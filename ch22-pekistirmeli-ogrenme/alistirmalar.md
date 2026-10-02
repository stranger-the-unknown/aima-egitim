# Bölüm 22 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Ödül-kalan ★

Kitabın 2. ve 3. denemelerinde (notlar §2) (1,1), (2,3) ve (3,2) için ödül-kalan örneklerini elle hesapla.

## A2 — Üç denemeden doğrudan kestirim (kod) ★

Üç denemenin hepsini kullanarak her durumun doğrudan fayda kestirimini bul ve gerçek faydalarla karşılaştır. (1,1)'in tahmini neden bu kadar düşük?

## A3 — Üç denemeden model (kod) ★★

Üç denemeden ADP'nin öğrendiği geçiş modelini çıkar. Hangi tahminler gerçek değerlerden (0.8 / 0.1 / 0.1) en çok sapıyor? Bu model bir politikayı değerlendirmek için yeterli mi?

## A4 — TD'yi elle izle ★★

U(1,3) = 0.84, U(2,3) = 0.96 ve α = 0.1. (1,3) → (2,3) geçişi (ödül −0.04) gözlenince U(1,3) ne olur? Aynı geçiş art arda 10 kez gözlenirse U(1,3) hangi değere yaklaşır? Gerçek U(1,3) 0.8516 iken bu neden sorun değildir?

## A5 — Q-öğrenme ve SARSA ★★

Q(s, a) = 0.5, α = 0.5, γ = 1, r = −0.04. Ardıl s′'de Q(s′, a₁) = 0.9, Q(s′, a₂) = 0.2 ve ajan keşif amacıyla a₂'yi seçiyor.
1. Q-öğrenme ve SARSA güncellemelerinden sonra Q(s, a) nedir?
2. Hangisi keşif politikasının değerini öğrenir? Uçurum kenarında yürüyen bir robot için hangisi daha temkinli politikalar üretir?

## A6 — Nₑ'nin etkisi (kod) ★★

Keşifçi ADP'yi Nₑ = 1, 5, 20 ile çalıştır. 20 ve 100 denemedeki politika kayıplarını karşılaştır. Çok küçük ve çok büyük Nₑ'nin sakıncası nedir?

## A7 — İşlev yaklaşımını elle ★★

Û_θ(x, y) = θ₀ + θ₁x + θ₂y, θ = (0.5, 0.2, 0.1), α = 0.1. (1,1) için gözlenen ödül-kalan 0.4. Delta kuralıyla yeni θ'yı bul. Û(3,3) nasıl değişti? Bu iyi bir şey mi?

## A8 — Özellik eklemek (kod) ★★

4 × 3 dünyanın gerçek faydalarını en küçük karelerle (1, x, y); (1, x, y, hedefe Manhattan uzaklığı); (1, x, y, uzaklık, "−1'e komşu mu?") özellikleriyle temsil et. RMS hataları karşılaştır. Uzaklık özelliği neden işe yaramıyor?

## A9 — REINFORCE'ta öğrenme hızı (kod) ★★★

Tablo biçimli softmax politikayla REINFORCE'u α = 0.01, 0.05, 0.2 ile 1500 bölüm çalıştır. Sonuçları yorumla. Politika gradyanı yöntemlerinin varyansını azaltmak için neler yapılabilir?

## A10 — Taklit mi, ters RL mi? ★★★

Bir uzman sürücünün kayıtları var. (a) Davranış klonlama ve (b) ters pekiştirmeli öğrenme yaklaşımlarının her biri için:
1. Ne öğrenilir?
2. Öğretmenin hiç girmediği bir durumda (ör. yolda beklenmedik bir engel) ne olur?
3. Hangisi öğretmenden daha iyi sürüş öğrenebilir? Neden?
