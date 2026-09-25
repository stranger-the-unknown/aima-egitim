# Katkı ve bölüm ekleme rehberi

Bu depo, öğrencinin asistanla birlikte AIMA’yı bölüm bölüm tamamlaması için tasarlandı. Yeni içerik eklerken şu kurallara uyun.

## Telif kuralları (zorunlu)

1. Kitaptan **uzun alıntı** veya **yakın parafraz** yok.
2. Notlar **özgün Türkçe** öğretim diliyle yazılır.
3. Kod, kamuya açık algoritmaların **eğitici** Python uygulamasıdır; kitap metni aktarılmaz.
4. Alıştırmalar ve quizler **özgün** olmalıdır (kitap sorularının kopyası değil).
5. Resmi kaynaklara bağlantı verin: [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/), [aimacode](https://github.com/aimacode).

## Yeni bölüm nasıl eklenir? (asistanla)

Önerilen konuşma/akış:

1. `MUFREDAT.md` içinde hedef bölümü işaretle.
2. Asistana şunu söyle: *“chNN için notlar + örnek + 5 alıştırma + quiz yaz”*.
3. Asistan şu iskeleti oluşturur:

```
chNN-kisa-baslik/
├── README.md        # öğrenme hedefleri
├── notlar.md        # özgün Türkçe notlar (+ mermaid diyagram)
├── ornekler/        # çalıştırılabilir Python
├── alistirmalar.md  # 5 özgün alıştırma
├── cozumler/        # en az ilk 2 alıştırmanın çözümü
└── quiz.md          # 5 kısa soru + cevaplar
```

4. Örnek kodu birlikte çalıştırın; hataları düzeltin.
5. `MUFREDAT.md` içinde durumu `hazır` yapın.

## Kod stili

- Python 3.10+, tip ipuçları teşvik edilir.
- Yorumlar ve çıktı mesajları **Türkçe** olabilir (eğitsel amaç).
- Bağımlılık eklerken `requirements.txt` güncelleyin; mümkün olduğunca minimal tutun.
- Her `ornekler/*.py` dosyası doğrudan çalıştırılabilir olsun (`if __name__ == "__main__"`).

## Test ve kontrol

```bash
python scripts/check_setup.py
pytest   # ileride eklenecek testler için
```

## Commit mesajı önerisi

```
ch03: çözüm arama notları ve BFS/DFS örnekleri
```

## Soru / hata

Bir not belirsizse veya kod çalışmıyorsa: ilgili dosya yolunu, beklenen/gerçek çıktıyı yazın; asistanla birlikte düzeltin.
