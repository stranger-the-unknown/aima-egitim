# Bölüm 11 — Alıştırmalar

Sorular özgündür. Çözümler `cozumler/` klasöründe; önce kendin dene.

Zorluk: ★ kolay · ★★ orta · ★★★ zor

---

## A1 — Koy şeması ★

`ornekler/strips_bloklar.py`'deki elli bloklar dünyasında `Koy(X, Y)` eylemi, tutulan X bloğunu serbest Y bloğunun üstüne koyar. Önkoşulunu, ekleme ve silme listelerini yaz. Her silme için "neden?" sorusunu yanıtla.

## A2 — Bir adım ileri ★

Başlangıç durumu: `{On(A,Masa), On(B,Masa), Clear(A), Clear(B), ElBos}`.
`Kaldir(A, Masa)` eylemini uygula (`strips_bloklar.py`'deki tanımıyla). Yeni durumu tam olarak yaz. Hangi atomlar silindi, hangileri eklendi, hangileri olduğu gibi kaldı?

## A3 — İleri ve geri, elle ★

Kitaptaki hava kargo problemini kullan (`ornekler/kitap_problemleri.py`).
1. Başlangıçta `Load(C1, P1, SFO)` uygulanırsa yeni durum ne olur?
2. Hedef `At(C1,JFK) ∧ At(C2,SFO)`'yu `Unload(C1, P1, JFK)` ile gerilet. Gerilemiş hedef ne?
3. `Fly(P1, SFO, JFK)` bu (ilk) hedef için geri aramada ilgili bir eylem mi? Neden?

## A4 — Unutulan önkoşul ★★

Yedek lastik probleminde `PutOn` eyleminin `¬At(Flat, Axle)` önkoşulunu silersek planlayıcı ne bulur? Bu plan gerçek dünyada neden saçmadır? Bu deneyden modelleme hakkında ne öğreniyoruz? (İpucu: `cozumler/alistirma4_10_kod.py`'deki `a4_negatifsiz_lastik` fonksiyonuna bakmadan önce tahmin et.)

Ek soru: `LeaveOvernight` eylemi bir plana hiç yarar sağlayabilir mi?

## A5 — Sussman anomalisi, elle ★★

Başlangıç: C, A'nın üstünde; A ve B masada. Hedef: On(A, B) ∧ On(B, C).
1. Önce yalnızca On(A, B)'yi en kısa yoldan sağla, sonra On(B, C)'yi. Ne oluyor?
2. Tersini dene: Önce On(B, C), sonra On(A, B).
3. 3 adımlık doğru planı yaz ve neden alt hedefleri tek tek çözmekle bulunamadığını açıkla.

`python ornekler/kitap_problemleri.py` çıktısındaki "Sussman" bölümüyle karşılaştır.

## A6 — Sezgisellerin kabul edilebilirliği ★★

İki kargo (C1, C2) ve tek uçak (P1) SFO'da. Hedef: iki kargo da JFK'de.
1. En kısa planı yaz. h* kaç?
2. Silme listelerini yok sayarak h_max ve h_add'i elle hesapla. Hangisi h*'dan büyük? Neden?
3. h_max'ın her zaman kabul edilebilir olduğunu kısaca gerekçelendir.

## A7 — Kendi PDDL alanın: kahve robotu (kod) ★★

Bir robot Ofis'te. Odalar: Ofis – Koridor – Mutfak (yalnızca yan yana olanlar arasında geçilir). Kahve makinesi Mutfak'ta. Robot aynı anda tek fincan taşıyabilir.
1. `Git(a, b)`, `KahveYap(y)` ve `Birak(y)` eylem şemalarını `planlama.Sema` ile yaz.
2. Hedef KahveVar(Ofis) için planı bul. Kaç adım?
3. Koridor'a bitişik bir Toplantı odası ekle. Hedef KahveVar(Ofis) ∧ KahveVar(Toplantı) için plan kaç adım? BFS, h_max ve h_add ile genişletilen düğüm sayılarını karşılaştır.

## A8 — Çizelgeyi değiştir (kod) ★★

`ornekler/kritik_yol.py`'de MotorTak2'nin süresi 60 yerine 40 dakika olsun.
1. Kaynak kısıtı olmadan toplam süre ve kritik yol ne olur?
2. Kaynak kısıtlarıyla (1 vinç, 1 teker istasyonu) en kısa çizelge kaç dakika? Hangi motor önce takılmalı?
3. Tek denetçi olsaydı süre değişir miydi?

## A9 — Yeni bir inceltme (kod) ★★★

`ornekler/hiyerarsik_plan.py`'deki `Git(Ev, Havalimanı)` üst düzey eylemine üçüncü bir inceltme ekle: `[Yürü(Ev, İstasyon), Metro(İstasyon, Havalimanı)]`. Metro yalnızca ajanın ulaşım kartı varsa kullanılabilsin.
1. Arabası olmayan, 10 lirası ve kartı olan bir ajan için plan nedir?
2. Kartı da yoksa ne olur?
3. Arabası da kartı da olan bir ajan hangi planı alır? Neden? (Arama sırasını düşün.)

## A10 — Geri arama (kod) ★★★

`planlama.py`'ye bir geri (regression) arama yaz: Alt hedefleri (pozitif atomlar, negatif atomlar) çifti olarak tut, genişlik öncelikli ara.
1. İlgili ve tutarlı eylem koşullarını ve gerileme formülünü yaz.
2. Yedek lastik, bloklar ve hava kargo problemlerinde çalıştır. Planlar doğru mu?
3. Genişletilen düğüm sayısını ileri BFS ile karşılaştır. Sonuç seni şaşırttı mı? Nedenini açıkla: Geri aramanın ürettiği alt hedeflerin hepsi gerçekten ulaşılabilir durumları mı temsil ediyor?
