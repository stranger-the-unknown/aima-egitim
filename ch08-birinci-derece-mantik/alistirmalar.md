# Bölüm 8 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — FOL ve önerme mantığı ★

"Her çalışan bir ofiste oturur" bilgisini:
1. Yalnızca önerme sembolleriyle (en az 3 çalışan varsayarak) nasıl temsil edersin? Zorluk nedir?
2. Tek bir FOL cümlesiyle nasıl yazarsın?

## A2 — Niceleyici sırası ★

Aşağıdaki iki cümleyi Türkçe yorumla ve farklı olduklarını bir model ile göster:
1. ∀x ∃y Bağlı(x, y)
2. ∃y ∀x Bağlı(x, y)

## A3 — Ata ilişkisi ★

```bash
python ornekler/fol_sozluk.py
```

1. Ata(Leyla, Ece) hangi kural adımlarıyla türetilir?
2. ASK Ata(Ece, Leyla) neden HAYIR?
3. "HAYIR" yanıtı mantıksal olarak ne anlama gelir: "yanlış olduğu kanıtlandı" mı, "kanıtlanamadı" mı? Hangi anlam varsayımıyla ikisi aynı olur?

## A4 — İki klasik hata ★

```bash
python ornekler/fol_model.py
```

1. ∀x Kral(x) ∧ Kişi(x) modelde neden yanlış?
2. ∃x Taç(x) ⇒ Başında(x, John) neden "hiçbir şey söylemeyen" bir cümledir? Hangi tek nesne onu doğru yapmaya yeter?
3. İki cümlenin doğru hâllerini yaz.

## A5 — Tuzak teşhisi ★

Şu kural yanlış mı? Neden?

∀x ∀y (Ebeveyn(x, y) ∧ Ata(x, y))   — "Her ebeveyn aynı zamanda atadır" denmek istenmişti.

## A6 — Türkçeden FOL'a ★★

Aşağıdakileri FOL'a çevir (uygun yüklemleri sen tanımla):
1. Her öğrencinin en az bir danışmanı vardır.
2. Bazı dersleri hiçbir öğrenci almaz.
3. Ali'nin tam olarak iki kardeşi vardır.
4. Kendini tıraş etmeyen herkesi, yalnızca onları, berber tıraş eder.
5. Hiçbir iki öğrenci aynı numarayı taşımaz.

## A7 — Yeğen, enişte, yenge (kod) ★★

`ornekler/akrabalik_turkce.py`'ye Eş(x, y) ilişkisini ekle (simetrik). Şunları FOL ile tanımla ve kodla:
1. Yeğen(x, y): x, y'nin kardeşinin çocuğudur.
2. Enişte(x, y): x, y'nin halasının, teyzesinin ya da kız kardeşinin kocasıdır.
3. Yenge(x, y): x, y'nin amcasının, dayısının ya da erkek kardeşinin karısıdır.

Aileye birkaç evlilik ekle ve sonuçları listele.

## A8 — Peano aritmetiği ★★

Aksiyomlar: +(0, m) = m ve +(S(m), n) = S(+(m, n)).
1. 1 + 1 = 2 ifadesini S(0), S(S(0)) gösterimiyle yaz ve adım adım kanıtla.
2. +(m, 0) = m neden aksiyomlardan **doğrudan** çıkmaz? Ne gerekir?

## A9 — Wumpus FOL'da ★★

1. Kokulu(s) için nedensel ve teşhis kurallarını yaz.
2. Önerme mantığında 4×4 dünyada esinti kuralları için kaç cümle gerekir? FOL'da kaç?
3. "Wumpus tektir" bilgisini FOL'da yaz.

## A10 — İki bitlik toplayıcı (kod) ★★★

`ornekler/tam_toplayici.py`'deki C1 tam toplayıcısından iki tane kullanarak **iki bitlik** bir toplayıcı kur (dalgalı elde: ilk toplayıcının eldesi ikincinin üçüncü girişine gider).
1. Bağlantıları bilgi mühendisliği adımlarıyla yaz.
2. Tüm 2⁵ = 32 giriş için (a₁a₀ + b₁b₀ + elde₀) toplamını doğrula.
3. Bir bağlantıyı bilerek boz. Doğrulama hangi satırlarda başarısız oluyor?
