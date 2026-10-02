# Bölüm 7 — Quiz

Cevaplar dosyanın sonunda.

---

**S1.** KB ⊨ α'nın modellerle tanımı nedir?

**S2.** Sağlam ve tam çıkarım algoritmasını tanımla.

**S3.** Kitaptaki R1–R5 KB'sinde kaç model vardır? KB kaçında doğrudur? KB ⊨ ¬P12 mi, KB ⊨ ¬P22 mi?

**S4.** Tümdengelim teoremini ve çelişki ile kanıt ilkesini yaz.

**S5.** B11 ⇔ (P12 ∨ P21) cümlesinin CNF'si nedir?

**S6.** (P ∨ Q) ile (¬Q ∨ R) tümcelerinin çözümleyicisi nedir?

**S7.** Horn tümcesi ile kesin tümce arasındaki fark nedir? Horn KB'lerde gerektirmenin karmaşıklığı nedir?

**S8.** İleri ve geri zincirlemeyi "veri güdümlü / hedef güdümlü" kavramlarıyla açıkla.

**S9.** DPLL'in üç iyileştirmesini say.

**S10.** WalkSAT tam mıdır? Neden?

**S11.** Rastgele 3-SAT'ta en zor problemler hangi m/n oranında görülür? Neden?

**S12.** Çerçeve problemi nedir? Ardıl durum aksiyomu bunu nasıl çözer?

---

## Cevaplar

1. KB'nin doğru olduğu her modelde α da doğrudur: M(KB) ⊆ M(α).
2. Sağlam: Yalnızca gerektirilen cümleleri türetir. Tam: Gerektirilen her cümleyi türetebilir.
3. 7 sembol, **128** model. KB **3** modelde doğru. KB ⊨ ¬P12 **evet**; KB ⊨ ¬P22 **hayır** (ne P22 ne ¬P22 gerektirilir).
4. KB ⊨ α ⟺ (KB ⇒ α) geçerlidir. KB ⊨ α ⟺ (KB ∧ ¬α) karşılanamaz.
5. (¬B11 ∨ P12 ∨ P21) ∧ (¬P12 ∨ B11) ∧ (¬P21 ∨ B11)
6. **P ∨ R**
7. Kesin tümcede tam olarak bir, Horn tümcesinde en fazla bir pozitif literal vardır. Horn KB'lerde gerektirme **doğrusal zamanda** kararlaştırılır.
8. İleri zincirleme bilinen gerçeklerden başlayıp yeni sonuçlar türetir (veri güdümlü). Geri zincirleme sorgudan başlayıp onu kanıtlamak için gereken alt hedeflere iner (hedef güdümlü) ve çoğu zaman yalnızca ilgili gerçeklere dokunur.
9. Erken sonlandırma, saf sembol sezgiseli, birim tümce sezgiseli (birim yayılım).
10. **Hayır.** Cümle karşılanamazsa bunu kanıtlayamaz; yalnızca çevirme sınırına ulaşıp durur.
11. **m/n ≈ 4,3.** Daha az kısıtlı problemler kolayca karşılanır, daha çok kısıtlı olanlar hızla çelişkiye düşer. Geçiş bölgesinde ise ne çözüm kolayca bulunur ne de çelişki kolayca kanıtlanır.
12. Etki aksiyomları bir eylemin neyi değiştirdiğini söyler ama neyin **değişmediğini** söylemez. Bunu tek tek yazmak O(m·n) aksiyom gerektirir. Ardıl durum aksiyomu her akışkan için tek bir tanım verir: F^{t+1} ⇔ (F'yi doğru yapan eylem) ∨ (F^t ∧ F'yi yanlış yapan eylem yok).
