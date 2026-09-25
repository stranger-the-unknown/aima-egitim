# Bölüm 18 — Çok ajanlı karar verme: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: birden fazla akıllı ajanın etkileşimini oyun teorisi diliyle modellemek.

---

## 1. Tek ajan → çok ajan

Bölüm 16–17 tek karar vericiyi (MEU, MDP) ele aldı.  
Burada **birden fazla ajan** aynı ortamda seçim yapar; her birinin faydası diğerlerinin eylemlerine de bağlıdır.

```text
ajan A seçer a   +   ajan B seçer b   →   (u_A(a,b), u_B(a,b))
```

Rakip arama (Bölüm 5) sıfır toplamlı özel bir durumdu; genel oyun teorisi sıfır toplamı zorunlu kılmaz.

---

## 2. Normal form (stratejik form)

Bir oyun üçlüyle özetlenir:

| Parça | Anlam |
|-------|--------|
| Oyuncular | N = {1,…,n} |
| Strateji kümeleri | her i için Sᵢ |
| Ödeme (fayda) | uᵢ : S₁ × … × Sₙ → ℝ |

İki oyunculu sonlu oyunlarda ödemeler **matris** (veya çift matris) olarak yazılır.  
Satır oyuncu 1, sütun oyuncu 2; her hücrede (u₁, u₂).

---

## 3. Baskın strateji ve en iyi yanıt

- **Baskın strateji:** Diğerinin ne yaptığına bakılmaksızın, sizin için her zaman en az diğer stratejiniz kadar iyi (sıkı baskın: her zaman daha iyi).
- **En iyi yanıt (best response):** Rakibin sabit stratejisine karşı sizin faydanızı maksimize eden seçim.

Mahkûm İkilemi’nde her iki taraf için “ihanet” baskın stratejidir; ortak “işbirliği” Pareto daha iyi olsa da bireysel teşvik ihanete iter.

---

## 4. Nash dengesi (sezgi)

Strateji profili (s₁*, …, sₙ*) **saf Nash** ise: hiç kimse tek taraflı saparak kendi faydasını artıramaz.  
Yani her oyuncu, diğerleri s* oynarken kendi sᵢ*’sine en iyi yanıt vermektedir.

- Mahkûm İkilemi: tek saf Nash = (ihanet, ihanet).
- Koordinasyon / Stag Hunt: birden fazla saf Nash olabilir (risk vs getiri gerilimi).
- Tavuk (Chicken): “düz git / saptır” senaryosu; çarpışma kötü, “ustalık” ödüllü.

Karma Nash (olasılıklı strateji) bu bölümde yalnızca isim düzeyinde: saf denge yoksa veya risk paylaşımı istenirse devreye girer.

---

## 5. İşbirlikçi vs işbirlikçi olmayan

| | İşbirlikçi olmayan | İşbirlikçi |
|--|-------------------|------------|
| Anlaşma | bağlayıcı sözleşme yok | koalisyon / sözleşme mümkün |
| Odak | Nash, baskın strateji | ortak fayda, pazarlık, transfer |
| Örnek | Mahkûm İkilemi (klasik) | ekip planlama, ortak kaynak |

Çok ajanlı AI’de protokoller bazen “işbirliğini teşvik eden kurallar” ekler (ödül paylaşımı, itibar).

---

## 6. Oy ve sosyal seçim (üst düzey)

Birçok bireysel tercih → tek toplumsal karar:

- Çoğunluk oyu, Borda sayısı, Condorcet yöntemi gibi kurallar.
- Farklı kurallar farklı kazanan üretebilir; “adil / tutarlı” tüm özellikleri bir arada tutmak zordur (klasik imkansızlık sezgisi — ayrıntı kitaba).
- Ajan tasarımı: oylama kurallarını manipülasyona dirençli seçmek ayrı bir mühendislik problemi.

`mahkum_ikilemi.py` ve `nash_2x2.py` ödemeleri ve saf Nash’i sayısal basar.

---

## 7. Ajan bakışı

1. Oyuncuları, eylemleri ve ödemeleri yaz (normal form).
2. Baskın strateji / en iyi yanıt ara.
3. Saf Nash var mı? Birden fazla mı?
4. İşbirliği mümkün mü, yoksa teşvik uyumsuzluğu mu?
5. Toplumsal karar gerekiyorsa oy kuralını bilinçli seç.

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
