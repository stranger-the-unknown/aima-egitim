# Çözüm — A2: Niceleyici sırası

1. **∀x ∃y Bağlı(x, y)**: "Herkes en az bir kişiye bağlıdır." Her x için (belki farklı) bir y yeter.
2. **∃y ∀x Bağlı(x, y)**: "Öyle biri var ki herkes ona bağlıdır." Tek bir ortak y gerekir.

**Ayırt eden model:** Alan {A, B}, bağlar A → B ve B → A.
- (1) doğrudur: A, B'ye; B, A'ya bağlı.
- (2) yanlıştır: Herkesin bağlı olduğu tek bir kişi yok. B'nin kendisine bağı olmadığı için y = B işe yaramaz; aynı şekilde y = A da işe yaramaz.

**İkisinin de doğru olduğu model:** Bağlar A → B ve B → B. Herkes B'ye bağlıdır.

(2) her zaman (1)'i gerektirir: Herkesin bağlı olduğu bir y varsa, her x için o y iş görür. Tersi doğru değildir. Bu yüzden niceleyicilerin sırası değiştirilemez.
