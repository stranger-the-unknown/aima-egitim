# A1–A8 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Bileşen karnesi

| Bileşen | Kitaptaki bölümler | Kitaba göre en önemli eksik |
|---|---|---|
| Algılayıcı ve eyleyiciler | 25, 26 | Robotların yazılımdan gömülü sistemlere geçişi; esnek robotların önce endüstride, sonra evde yaygınlaşması |
| Dünya durumunu temsil | 4, 7, 10, 14, 15, 21, 24, 25 | Olasılık, birinci derece mantık, nesne kimliği belirsizliği ve sinir ağlarını birleştiren genel, yeniden kullanılabilir temsil; soyut zaman kavramları |
| Eylem seçimi | 3, 11, 17, 22 | Hiyerarşik durum ve davranış temsillerini kendiliğinden kurmak; POMDP'ye genişletmek |
| Ne istediğimize karar vermek | 16, 17, 18, 22, 27 | Karmaşık gerçek dünya tercih modelleri ve onlar üzerinde olasılık dağılımları; ödül fonksiyonları için bilgi mühendisliği |
| Öğrenme | 19–22, 24 | Az veriyle, yapılandırılmış temsillerle ve önsel bilgiyle birlikte öğrenmek; insanla ortak bir iletişim/temsil dili |
| Kaynaklar | 21, 24, 25 | Büyük ölçekli kuantum hesaplama için donanım ve yazılım atılımları; araç ekosistemi |

Gerekçe örneği: "Ne istediğimize karar vermek" en kritik olandır, çünkü diğer bileşenler ne kadar güçlenirse yanlış belirtilmiş bir amacın zararı o kadar büyür (Bölüm 27'deki Kral Midas sorunu). Başka bir gerekçeyle başka bir bileşen de savunulabilir.

## A2 — Kaba kuvvet

1. Bir yılda 10⁵¹ × 3.16 × 10⁷ ≈ 3.2 × 10⁵⁸ dizi. 100 000¹¹ = 10⁵⁵ ≤ 3.2 × 10⁵⁸ < 10⁶⁰ = 100 000¹²: **11 sözcük**. 12 sözcük için 10⁶⁰ / 3.2 × 10⁵⁸ ≈ **32 yıl**. (10 000 sözcüklük sözlükle 14 sözcük.)
2. 2^(2 × 10¹³) = 10^(2 × 10¹³ × 0.301) ≈ **10^(6 × 10¹²)**: altı trilyon basamaklı bir sayı. Karşılaştırma: Gözlemlenebilir evrende ~10⁸⁰ atom var. Kaba kuvvetle değil, hiyerarşi ve üst-akıl yürütmeyle karar verilmelidir.

## A3 — Üstel eğilimler

1. 72 ay / 3.5 = 20.6 katlanma → 2^20.6 ≈ **1.6 milyon kat**. Aynı hızla 10 yıl daha: 2^(120/3.5) ≈ **2 × 10¹⁰ kat**.
2. 5 × 10⁷ kat ucuzlama 50 yılda: yarılanma süresi 50 · ln 2 / ln(5 × 10⁷) ≈ **1.96 yıl**. 10 yıl sonra $0.02 / 2^(10/1.96) ≈ **$0.0006**.
3. Kitaba göre şimdiye dek her teknoloji S eğrisi izledi: Üstel büyüme fiziksel (enerji, ısı, atom boyutu), ekonomik (tek bir eğitim çalıştırmasının maliyeti) ya da toplumsal nedenlerle yavaşlar. Bölüm 27'deki örnekte S eğrisinin ilk 10 yılına uydurulan üstel 30. yıl için gerçeğin ~1500 katını tahmin etmişti. Bu tahminler en fazla "eğilim sürerse" anlamına gelir.

## A4 — Her an kesilebilir algoritma

Eğim yaklaşık **−0.46** (kuram −0.5): Monte Carlo kestiriminin standart hatası σ/√n'dir. Algoritma her an elindeki örneklerin ortalamasını döndürebilir; daha uzun çalıştıkça yanıt iyileşir ama hiçbir anda "yanıtsız" değildir. Bu, yinelemeli derinleştirmede her derinlik bitince en iyi hamlenin hazır olmasına benzer.

## A5 — Hesaplamanın değeri

1. | Maliyet | Ort. benzetim | Doğru eylem | Net fayda |
   |---|---|---|---|
   | 0.1 | 1.6 | %42 | 0.965 |
   | 0.01 | 4.0 | %61 | 1.143 |
   | 0.001 | 7.7 | %66 | 1.189 |

   Hesaplama ucuzladıkça etmen daha uzun düşünür, daha sık doğru eylemi seçer ve net faydası artar. Pahalıysa az düşünüp "yeterince iyi" bir kararla harekete geçmek akılcıdır.
2. Miyop hesap yalnızca **tek** bir benzetimin kararı değiştirme olasılığına bakar. İki eylem birbirinden epey farklı görünüyorsa tek bir gözlem sıralamayı değiştiremez; değer maliyetin altında kalır ve etmen durur. Oysa birkaç gözlem birlikte sıralamayı değiştirebilir. 1–20 benzetimlik paketlerin (benzetim başına) net değerine bakan etmen maliyet 0.01'de ortalama 4.2 benzetimle doğru eylemi **%71** (miyop %61) seçer, net fayda **1.171** (miyop 1.143). Kitabın dediği gibi üst düzey pekiştirmeli öğrenme de bu miyopiden kaçınmanın bir yoludur.

## A6 — Sınırlı en iyilik

| b | En iyi derinlik | Net değer |
|---|---|---|
| 2 | 7 | 0.959 |
| 3 | 5 | 0.898 |
| 10 | 3 | 0.684 |

Aynı "mimari" (birim zaman maliyeti) için farklı programlar (derinlikler) arasından en iyi net değeri veren seçilir; dallanma büyüdükçe en iyi program daha sığ aramadır ve ulaşılabilen değer düşer. Bu, "mükemmel akılcı" etmenin değil, mimarinin izin verdiği en iyi programın hedeflenmesidir. Basitleştirmeler: Gerçekte program uzayı yalnızca bir derinlik parametresi değildir; nitelik ve süre fonksiyonları bilinmez; en iyi derinlik duruma göre değişir (her an kesilebilir arama ve üst-akıl yürütme bu yüzden gereklidir).

## A7 — Genel YZ tartışması

Turing'in listesi kişisel ve zihinsel nitelikler (nezaket, mizah, âşık olmak, yeni bir şey yapmak), Heinlein'ınki fiziksel ve toplumsal beceriler (bez değiştirmek, kemik sarmak, gemi yönetmek, sone yazmak, ölmekte olanı teselli etmek). İkisi de genelliği vurgular ve hiçbir YZ ikisini karşılamaz. Wright benzetmesinin gücü: Çalışan dar bir sistemden öğrenilenler genel çözüme giden yolu açar; doğrudan "genel uçuş" hedeflemek de, tek görevi sonsuza dek cilalamak da yanlıştır. Zayıflığı: Uçuşun fizik yasaları baştan biliniyordu; zekânın "genel" ilkeleri belki dar görevlerin birikimiyle değil, temelden yeni fikirlerle bulunacaktır (bazı HLAI savunucularının görüşü). Yanıt bir görüş meselesidir; argümanın tutarlılığı önemlidir.

## A8 — Kişisel etmen tasarla

Örnek taslak:
- **Bilgi:** Takvim, iletişim, alışkanlıklar, kullanıcının açıkça belirttiği hedefler (sağlık, öğrenme, aile). Veri cihazda kalır; gerekiyorsa federe öğrenme ve diferansiyel mahremiyet (Bölüm 27).
- **Fayda öğrenme:** Kullanıcının seçimlerinden ters PÖ / tercih öğrenme (Bölüm 22, 26); ama tıklamalar uzun vadeli çıkarı değil anlık dürtüyü yansıtabilir. Bu yüzden ara ara açık geri bildirim ("Bu hafta istediğin kadar okuyabildin mi?") ve karşılaştırmalı sorular.
- **Tercih belirsizliği:** Yardım oyunu bakışı (Bölüm 18, 27): Emin olmadığında sor, geri alınamaz eylemlerden kaçın, düşük etkili davran.
- **Güvenlik ve mahremiyet:** Satıcıların tekliflerine aracılık ederken kendi teşvikleri (reklam geliri) olmamalı; açıklanabilir öneriler; kullanıcının etmeni kapatabilmesi ve kararlarını denetleyebilmesi.
- **Mimari:** Her an kesilebilir öneri (bildirim anında hazır bir yanıt), üst-akıl yürütme (hangi konuyu düşünmeye değer: önemli bir sağlık randevusu mu, gereksiz bir bildirim mi), refleks katman (acil uyarılar).
