# Çözümler — A6–A10 (kod)

Kodlar bu klasörde; çalıştırıp kendi sonuçlarınla karşılaştır.

## A6 — GA parametreleri: `alistirma6_ga_parametre.py`

10 tohum, en fazla 500 nesil, popülasyon 100:

| Seçim | Mutasyon | Elit | Başarı | Ort. nesil |
|---|---|---|---|---|
| orantılı | 0,0 | 2 | 1/10 | 10 |
| orantılı | 0,1 | 2 | 7/10 | 147 |
| orantılı | 0,6 | 2 | 8/10 | 126 |
| turnuva | 0,0 | 2 | 3/10 | 9 |
| turnuva | 0,1 | 2 | 6/10 | 57 |
| turnuva | 0,6 | 2 | 7/10 | 75 |
| orantılı | 0,6 | 0 | 7/10 | 136 |

- **Mutasyon 0:** Çaprazlama yalnızca popülasyonda **zaten var olan** rakamları karıştırır. Bir sütunda doğru satır hiçbir bireyde yoksa oraya asla ulaşılamaz. Popülasyon hızla tek tipe yakınsar ("erken yakınsama"). Başarılı olan birkaç koşu da şansla, ilk nesillerde bulunmuştur.
- **Turnuva seçimi** daha güçlü seçim baskısı yapar. Başarılı olduğunda daha hızlıdır, ama çeşitliliği de daha hızlı tüketir.
- **Elitizmi kapatmak** en iyi bireyin kaybolmasına izin verir. Bu küçük deneyde etkisi sınırlı, ama genelde ilerlemenin geri gitmesine yol açar.

## A7 — Kaygan süpürge: `alistirma7_kaygan_supurge.py`

1. SONUÇLAR(1, Sağ) = **{1, 2}** (başarı ya da kayma).
2. **Plan bulunamaz.** Durum 5'te Sağ'ın sonuçları {5, 6}. VE düğümünde 5 için de plan gerekir, ama 5 zaten yoldadır, yani döngüdür. Döngüsüz AND-OR araması bunu başarısızlık sayar. Diğer eylemler de 5'te 5'e döner. Hiçbir *döngüsüz* plan, ortamın sonsuza kadar kaydırmasına karşı garanti veremez.
3. Döngüsel plan: **[Süpür, D1: Sağ, eğer durum = 5 ise D1'e dön değilse Süpür]**. %50 kaymayla 10.000 koşunun hepsi hedefe ulaştı, ortalama 1,98 deneme (beklenen 2). **Varsayım:** Her deneme bağımsızdır ve başarı olasılığı sıfırdan büyüktür. Kalıcı bir arıza (kilitli kapı) varsa plan sonsuza kadar döner. O zaman sorun "kaygan zemin" değil, eksik bir ortam modelidir.

## A8 — Üç kareli algısız süpürge: `alistirma8_uc_kare_algisiz.py`

1. 3 konum × 2³ kir durumu = **24** fiziksel durum. Başlangıç inancı 24 durumun tamamıdır.
2. En kısa plan (BFS): **[Sağ, Sağ, Süpür, Sol, Süpür, Sol, Süpür]**, yani 7 adım.
3. İki karede 4 adım yetiyordu. Konumu bilmeyen ajan önce bir uca "yaslanıp" belirsizliği yok etmeli (2 adım), sonra her kareyi sırayla süpürmeli. n kare için plan uzunluğu yaklaşık (n − 1) + n + (n − 1) = 3n − 2 olur.

## A9 — Adım büyüklüğü: `alistirma9_10_adim_ve_lrta.py`

| α | 300 adım sonra f (bin km²) |
|---|---|
| 0,001 | 1.028 (yavaş ama minimuma yaklaşıyor) |
| 0,01 | 1.039 |
| 0,03 | 1.039 |
| 0,1 | 942 (sınırda, şans eseri başka bir çukur) |
| 0,2 | **ıraksıyor** |

- Bir havalimanına n il düşüyorsa, o koordinattaki eğrilik (ikinci türev) 2n'dir. Gradyan inişinin kararlı olması için α < 2/(2n) = 1/n gerekir. En kalabalık kümede n ≈ 11 → α ≲ 0,09. α = 0,2 bu sınırı açıkça aşar: her adım minimumu öteye aşar ve f patlar.
- α = 0,1 sınırın hemen üstündedir. İlk adımlarda aşırı sıçrayıp kümeleri değiştirdi ve şans eseri daha iyi bir çukura düştü. Bu güvenilir bir strateji değildir; aynı sıçrama daha kötü bir yere de götürebilirdi.
- **Newton** her yöndeki eğriliği bildiği için adımı ona göre ölçekler (α = 1/(2n)). Bu yüzden α seçme derdi yoktur ve 2 adımda yakınsar.

## A10 — LRTA* ve sezgisel: `alistirma9_10_adim_ve_lrta.py`

| Sezgisel | İlk deneme | Kaçıncı denemeden itibaren hep optimal (25) |
|---|---|---|
| Manhattan | 154 | 11 |
| h = 0 | 187 | 26 |
| 3 × Manhattan (kabul edilemez) | 320 | 19 |

1. h = 0 ile ajan hiçbir yön bilgisine sahip değildir. H değerlerini sıfırdan "inşa etmek" için çok daha fazla deneme gerekir.
2. 3 × Manhattan ile ilk deneme en uzun olanıdır: Aşırı tahminler, hedefe yakın ama duvarla kapalı bölgeleri bile "pahalı" gösterir ve ajan yanlış yöne sapar. Bu labirentte sonunda optimal yolu öğrendi, ama bu **garanti değildir**. Kabul edilebilirlik bozulunca H değerleri gerçek maliyetin üstünde kalabilir ve LRTA* bunları hiç aşağı çekmez. Bu yüzden optimal olmayan bir yola kilitlenebilir.
3. **İyimserlik:** Denenmemiş eylemler "doğrudan hedefe h(s) maliyetle gider" diye değerlendirilir. Ajan bilinmeyen koridorları bu yüzden dener; arada uzun "keşif" denemeleri (ör. Manhattan'da 6. deneme, 109 adım) bu iyimserliğin bedelidir.
