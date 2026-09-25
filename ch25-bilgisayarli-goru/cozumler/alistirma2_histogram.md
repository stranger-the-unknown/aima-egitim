# A2 çözümü — Histogram sınıf

`histogram_ozellik.py` sentetik yamaların gri (veya renk) histogramını vektör yapar; eğitim prototiplerine L1/L2 uzaklığı ile etiket atar.

- Açık / koyu / kırmızımsı prototipler ayrışır; test aynı dağılımdaysa doğru etiket gelir.
- Açık yamayı koyulaştırırsanız histogram sola kayar → “koyu” prototipe yaklaşır; tahmin değişebilir.

Bu, konum bilgisiz küresel özelliğin hem gücünü (basit ayrım) hem kırılganlığını gösterir.
