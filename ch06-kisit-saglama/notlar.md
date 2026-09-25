# Bölüm 6 — Kısıt sağlama: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Kavramları Türkçe, kendi cümlelerimizle öğretir.

---

## 1. CSP nedir?

Bazı problemlerde “yol maliyeti”nden çok **kısıtların hepsinin aynı anda sağlanması** önemlidir. Zaman çizelgesi, sudoku, harita boyama, N-vezir… Hepsi aynı kalıba oturur:

| Parça | Anlamı | Harita boyama örneği |
|-------|--------|----------------------|
| **Değişkenler** \(X\) | Atama yapılacak nesneler | Bölgeler: Marmara, Ege, … |
| **Domainler** \(D\) | Her değişkenin alabileceği değerler | `{Kırmızı, Yeşil, Mavi}` |
| **Kısıtlar** \(C\) | Hangi kombinasyonlar yasak/izinli | Komşu bölgeler farklı renk |

Bir **atama** her değişkene bir değer vermektir. **Tam atama** hepsine değer verir; **tutarlı atama** hiçbir kısıtı çiğnemez. CSP çözümü = tutarlı ve tam atama.

Klasik aramadan fark: durum uzayı “hangi sırayla hangi değeri denedim” değil; çoğu zaman **değişken seçimi + değer seçimi** ile ağaç büyütülür ve kısıtlar budama sağlar.

---

## 2. Kısıt türleri (kısa)

- **Tekli:** “Bu değişken şu değerde olamaz.”
- **İkili:** İki değişken arasında ilişki (haritada “komşular ≠”).
- **Yüksek mertebe:** Üç veya daha fazla değişken (ör. “bu üç dersten en az biri sabah”).

Pratikte çoğu eğitim örneği **ikili CSP**’ye indirgenir veya öyle formüle edilir.

---

## 3. Geri dönüşlü arama (backtracking)

En temel sistematik yöntem:

1. Henüz atanmamış bir değişken seç.
2. Domaininden bir değer dene.
3. Kısıtlar bozulmuyorsa devam et; bozuluyorsa o değeri bırak, başkasını dene.
4. Hiç değer kalmazsa bir önceki değişkene **geri dön** (backtrack).

Bu, derinlik öncelikli aramanın CSP’ye özel hâli gibidir: kısmi atama tutarsızlaşınca o alt ağaç ölür.

```text
BT(atama):
  hepsi atandıysa → çözüm
  var ← seç_değişken(atanmamışlar)
  her değer in sıralı_domain(var):
      atama[var] = değer
      kısıtlar OK ve (isteğe bağlı) çıkarım OK ise:
          sonuç = BT(atama)
          başarılıysa döndür
      atama[var]'ı geri al
  başarısız
```

Çıktı: ya bir çözüm, ya “çözüm yok”.

---

## 4. İleriye kontrol (forward checking)

Bir değişkene değer verince, **henüz atanmamış komşuların domainlerinden** o değeri (veya kısıtı bozan değerleri) sil. Birinin domaini boşalırsa hemen geri dön — ileride boşa derinleşmeyiz.

Sezgi: “Ben Marmara’yı kırmızı yaptım → Ege’nin domaininden kırmızıyı çıkar; Ege’de renk kalmadıysa bu dal ölü.”

İleriye kontrol **yerel** bir bakıştır; uzak zincirleri her zaman görmez. Daha güçlü tutarlılık algoritmaları gerekir.

---

## 5. Yayılma ve AC-3 sezgisi

**Yayılma (arc consistency):** Kenar \((X_i, X_j)\) için: \(X_i\)’nin her değeri için \(X_j\)’de en az bir uyumlu değer varsa yay tutarlıdır. Yoksa \(X_i\)’den o değeri sil.

**AC-3:** Tutarsız yayları kuyruğa koy; bir değişkenden değer silinince o değişkene gelen yayları yeniden kontrol et. Domainler küçülür; biri boşalırsa problem (o kısmi atama altında) çözümsüzdür.

Backtracking’in her adımında AC-3 çalıştırmak (MAC — Maintaining Arc Consistency) ileriye kontrolden genelde daha pahalı ama daha güçlü budama verir. Bu notlarda sezgi yeter: **domainleri kısıtlara göre erken daralt**.

---

## 6. Sezgiseller: sırayı akıllı seç

Hangi değişken / hangi değer önce? Yanlış sıra → kocaman başarısız alt ağaçlar.

| Sezgisel | Ne yapar? | Neden işe yarar? |
|----------|-----------|------------------|
| **MRV** (Minimum Remaining Values) | Domaini en küçük kalan değişkeni seç | En kısıtlı olanı önce “sıkıştır”; erken başarısızlık |
| **Derece (degree)** | MRV berabere kalırsa en çok kısıta bağlı değişkeni seç | Diğerlerini daha çok etkiler |
| **LCV** (Least Constraining Value) | Değeri seçerken komşuların domainini **en az** daraltanı dene | Esnekliği koru; çözüm şansını artır |

MRV “hangi soruyu önce sorayım?”, LCV “cevabı nasıl vereyim ki kapıları kapatmayayım?” gibidir.

---

## 7. Yerel arama ile bağ

Bölüm 4’teki tepe tırmanma / SA, CSP’de de kullanılır: rastgele tam atama → çiğnenen kısıt sayısını azalt. Büyük, seyrek kısıtlı problemlerde bazen backtracking’den hızlıdır; **garanti** aramaz (yerel tepe).

Bu bölümün omurgası yine sistematik BT + tutarlılık + sezgisellerdir.

---

## 8. Özet

| Kavram | Tek cümle |
|--------|-----------|
| CSP | Değişken + domain + kısıt; tutarlı tam atama ara |
| Backtracking | Değişken/değer dene; tutarsızsa geri dön |
| Forward checking | Atama sonrası komşu domainlerini küçült |
| AC-3 | Yay tutarlılığını kuyrukla yay |
| MRV / derece / LCV | Önce zor değişken; sonra yumuşak değer |

Örnekler: `harita_boyama_csp.py` (Türkiye bölgeleri), `n_vezir_csp.py` (CSP olarak N-vezir).

Sonraki bölüm (7): bilgi tabanlı ajanlar ve önermeler mantığı.
