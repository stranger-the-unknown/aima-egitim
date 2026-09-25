# Bölüm 6 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — CSP modeli

Bir üniversitede üç ders (`MAT`, `FIZ`, `YAZ`) üç zaman dilimine (`09:00`, `11:00`, `14:00`) yerleştirilecek. Aynı anda en fazla bir ders olabilir. `MAT` ile `FIZ` aynı hocayı paylaştığı için **farklı** saatlerde olmalı (zaten genel kısıttan da gelir).

1. Değişkenleri, domainleri ve kısıtları yazın.
2. Bu problem neden “klasik yol arama”dan çok CSP’ye uyuyor?

## A2 — MRV sezgisi

Harita boyamada İç Anadolu’nun altı komşusu var; Ege’nin üç. Üç renk var; İç Anadolu’nun domaini bir nedenle 1 renge düşmüş, Ege’nin hâlâ 3 rengi var.

1. MRV hangi değişkeni önce seçer? Neden?
2. Derece sezgiseli berabere kalınca ne işe yarar?

## A3 — Harita boyama çalıştır

```bash
python ornekler/harita_boyama_csp.py
python ornekler/harita_boyama_csp.py --mrv --forward
python ornekler/harita_boyama_csp.py --karsilastir
```

1. Üç renkle çözüm bulundu mu? İç Anadolu hangi renge boyandı?
2. `--karsilastir` çıktısında hangi mod daha az değer denemesi yaptı? Kısaca yorumlayın.

## A4 — N-vezir CSP

```bash
python ornekler/n_vezir_csp.py --n 4
python ornekler/n_vezir_csp.py --n 8
```

1. Değişken / domain / kısıt tanımını kendi cümlelerinizle yazın.
2. Bölüm 4’teki tepe tırmanmadan farkı nedir (garanti açısından)?

## A5 — İleriye kontrol vs AC-3

Bir değişkene değer verdiniz; komşunun domaininden o değeri sildiniz (ileriye kontrol). Neden bu, tam yay tutarlılığı (AC-3) kadar güçlü olmayabilir? Bir cümlelik senaryo düşünün (A→B→C zinciri).
