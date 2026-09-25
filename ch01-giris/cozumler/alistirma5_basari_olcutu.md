# Çözüm — A5: Başarı ölçütü tuzağı

| # | P tanımı | Olası istenmeyen davranış |
|---|---|---|
| 1 | Oturum başına **tıklama sayısını** en yükseğe çıkar | Sistem abartılı başlıklar (*clickbait*), öfke uyandıran ve kutuplaştırıcı içerik önerir; kullanıcı çok tıklar ama daha az bilgilenir. |
| 2 | Kullanıcının **uzun vadeli bilgi kazanımını** en yükseğe çıkar (ör. sonradan yapılan kısa anketlerle ölçülür) | Ölçülebilir olanı "bilgi" sanar: kolay anket sorularına hazırlayan yüzeysel içerik öne çıkar. Ayrıca kullanıcıyı sıkıp platformdan uzaklaştırabilir. |
| 3 | **Zararlı/yanıltıcı** içeriğe ceza ver | "Zararlı" etiketini veren sınıflandırıcı hatalıysa meşru ama tartışmalı haberler bastırılır (aşırı sansür). Sistem riskten kaçmak için yalnızca zararsız ama önemsiz içerik gösterebilir. |

## Dersler

1. **Her ölçüt bir vekildir (*proxy*).** Gerçekte istediğimiz "iyi bilgilendirilmiş, memnun kullanıcı"dır. Bunu doğrudan ölçemediğimiz için tıklama, anket, etiket gibi vekiller kullanırız.
2. **Güçlü bir en iyileyici, vekil ile gerçek hedef arasındaki boşluğu bulup kullanır.** Buna *Goodhart yasası* da denir: "Bir ölçü hedef hâline geldiğinde iyi bir ölçü olmaktan çıkar."
3. Tek bir ölçüt yerine birden çok ölçütü **dengelemek**, insan geri bildirimi almak ve amacın *belirsiz* olduğunu kabul etmek daha sağlam bir yoldur (bkz. notlar §2).
