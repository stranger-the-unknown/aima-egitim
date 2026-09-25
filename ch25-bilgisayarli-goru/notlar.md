# Bölüm 25 — Bilgisayarlı görü: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: görüntüyü sayıya indirgemek; filtre ve görev dilini kurmak. Ağır CNN şart değil.

---

## 1. Görüntü = dizi

Gri görüntü: H×W matris; her piksel bir yoğunluk (0–255 veya 0–1).
Renkli: H×W×3 (ör. R,G,B kanalları).

```text
[[10, 10, 200],
 [10, 10, 200],
 [10, 10, 200]]   ← solda koyu, sağda açık dikey kenar
```

Bilgisayar “nesne” görmez; sayılar görür. Özellik / öğrenme bu sayılardan yapı çıkarır.

---

## 2. Konvolüsyon sezgisi

Küçük bir **çekirdek (kernel)** ızgara üzerinde kayar; yerel ağırlıklı toplam üretir.

```text
çıkış[i,j] = Σ_u Σ_v  görüntü[i+u, j+v] · çekirdek[u,v]
```

- Bulanıklaştırma: ortalama / Gauss
- Keskinleştirme: merkez yüksek, komşular negatif
- Kenar: Sobel / Prewitt tarzı fark çekirdekleri

CNN’lerde çekirdek ağırlıkları öğrenilir; burada elle kenar çekirdeği ile sezgi.

`konvolusyon_mini.py` 5×5 sentetik görüntüye dikey kenar filtresi uygular; sonucu basar / isteğe bağlı kaydeder.

---

## 3. Kenar özellikleri

Kenar ≈ yoğunlukta ani değişim. Yatay / dikey gradyan (Sobel) büyüklüğü kenar haritası verir.

Neden işe yarar? Nesne sınırları, doku geçişleri — sınıflandırma ve tespit için klasik ipucu.
Modern ağlar kenarı “kendisi öğrenir”; klasik boru hattında Canny vb. kullanılıyordu.

---

## 4. Histogram özelliği

Piksel değerlerinin (veya renk kanallarının) frekans dağılımı.

- Gri histogram: parlaklık profili
- Renk histogramı: “ne kadar kırmızı / yeşil / …” — konum bilgisi zayıf

İki görüntü histogramı L1 / L2 / kosinüs ile karşılaştırılabilir → kaba benzerlik veya toy sınıflandırıcı.

`histogram_ozellik.py` sentetik “açık / koyu / kırmızımsı” yamalardan histogram uzaklığı ile etiket tahmin eder.

---

## 5. Sınıflandırma vs tespit vs segmentasyon

| Görev | Çıktı |
|-------|--------|
| **Sınıflandırma** | Tüm görüntü için etiket (kedi / değil) |
| **Tespit (detection)** | Kutular + etiketler (nerede hangi nesne) |
| **Segmentasyon** | Piksel piksel etiket (nesne maskesi / semantik harita) |

Zorluk ve etiket maliyeti genelde sınıflandırma < tespit < (ince) segmentasyon artar.
Aynı omurga (CNN / ViT) farklı kafalarla bu görevlere uyarlanır — detay Ch21 + ileri CV.

---

## 6. Ajan bakışı

1. Önce görüntüyü matris olarak bas; kenarı elle filtreyle gör.
2. Histogramın ne kaybettiğini (konum) fark et.
3. Görevi netleştir: etiket mi, kutu mu, maske mi?
4. Sonra derin model; önce özellik sezgisi.

Özet: **görüntü = dizi; konvolüsyon = yerel filtre; kenar = gradyan; histogram = küresel dağılım; görevler = sınıf / kutu / maske.** Kitabı yasal nüshadan oku.
