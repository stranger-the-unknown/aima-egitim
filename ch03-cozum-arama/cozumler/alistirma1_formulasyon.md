# Çözüm — A1: Problem formülasyonu

| Parça | Tanım |
|-------|--------|
| **Durum** | Robotun (satır, sütun) konumu; satır,sütun ∈ {0,1,2} |
| **Başlangıç** | (0, 0) |
| **Eylemler** | Yukarı, aşağı, sol, sağ (ızgara dışına çıkanlar elenir) |
| **Geçiş** | Konumu seçilen yöne bir birim kaydır |
| **Hedef testi** | konum == (2, 2) |
| **Yol maliyeti** | Adım sayısı (her kenar maliyeti 1) |

**Gerekçe:** Engeller ve nesneler yok; karar için yalnızca konum yeterli — sade durum uzayı aramayı kolaylaştırır.
