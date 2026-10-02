# Çözüm — A5: Öğrenen reklam ajanı

| Parça | Bu problemde | Örnek cümle |
|---|---|---|
| **Performans öğesi** | Bir kullanıcıya hangi reklamın gösterileceğine karar veren politika | "Bu kullanıcı spor haberlerini okuyor; koşu ayakkabısı reklamını göster." |
| **Eleştirmen** | Sabit ölçüte göre geri bildirim: tıklama, satın alma, reklamı gizleme, uzun vadeli memnuniyet | "Reklam gösterildi, kullanıcı 'bu reklamı gizle' dedi: olumsuz sinyal." |
| **Öğrenme öğesi** | Geri bildirimle modeli günceller (ör. tıklama olasılığı tahmincisini yeniden eğitir) | "Gece saatlerinde spor reklamlarının tıklanma oranı düşük; ağırlığı azalt." |
| **Problem üreteci** | Bilgi toplamak için bazen "en iyi bilinen" dışında bir reklam dener (keşif) | "Bu kullanıcıya hiç kitap reklamı gösterilmedi; küçük bir olasılıkla dene." |

**Tasarım uyarısı:** Eleştirmenin ölçütü yalnızca "tıklama" olursa, ajan tıklamayı en yükseğe çıkaran ama kullanıcıyı rahatsız eden reklamları (abartılı vaatler) öğrenir. Ölçüte gizleme ve şikâyet cezası, satın alma sonrası memnuniyet gibi terimler eklemek gerekir (Bölüm 1, A5 ile karşılaştır).

**Bağlantı:** Keşif ile mevcut bilgiyi kullanma (*exploration vs. exploitation*) ödünleşimi Bölüm 17 (bandit problemleri) ve Bölüm 22'de (pekiştirmeli öğrenme) ayrıntılı işlenir.
