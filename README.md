
# yoskPixel - Retro Piksel Sanat Editörü

yoskPixel, Python ve Tkinter kullanılarak geliştirilmiş, retro temalara ve animasyonlu görsel efektlere sahip, basit ama güçlü bir piksel sanat editörüdür. Kendi oyun varlıklarınızı, avatarlarınızı veya sadece eğlence için piksellerle sanat yapmanızı sağlar.

<img width="866" height="744" alt="image" src="https://github.com/user-attachments/assets/014914e0-18b1-489a-859c-d12d9255d0eb" />

## ✨ Özellikler

*   **Temel Çizim Araçları:** Kalem, Silgi, Renk Kovası (Doldurma) ve Renk Seçici.
*   **Ayarlanabilir Fırça Boyutu:** 1'den 10 piksele kadar fırça kalınlığı.
*   **Simetri Modları:** Yatay ve dikey ayna modu ile simetrik çizimler yapın.
*   **Izgara Desteği:** Pikselleri daha net görmek için açılıp kapatılabilen ızgara.
*   **Geri Alma:** `Ctrl+Z` kısayolu ile son işlemi geri alın (20 adıma kadar).
*   **Retro Temalar:** Windows 98, XP Luna Blue, Matrix ve Command Prompt gibi nostaljik arayüz temaları.
*   **Özelleştirilebilir Tuval:** İstediğiniz boyutlarda (256x256 piksele kadar) yeni bir tuval oluşturun.
*   **Dosya İşlemleri:**
    *   Çalışmanızı **PNG** olarak kaydedin.
    *   Mevcut bir **PNG** dosyasını açıp düzenleyin.
*   **Animasyonlu Efektler:**
    *   **Glitch:** Dijital bozulma efekti oluşturun.
    *   **Scanline:** Eski CRT monitörlerdeki gibi tarama çizgileri ekleyin.
    *   **Noise:** Resme rastgele parazit (siyah-beyaz veya renkli) ekleyin.
*   **GIF Olarak Kaydetme:** Oluşturduğunuz animasyonlu efektleri **GIF** formatında dışa aktarın.

## ⚙️ Gereksinimler

Projeyi çalıştırmak için sisteminizde **Python 3**'ün yüklü olması gerekmektedir. Ayrıca, resim işleme işlemleri için `Pillow` kütüphanesine ihtiyaç vardır.

Aşağıdaki komut ile `Pillow` kütüphanesini kurabilirsiniz:
```bash
pip install Pillow
```

## 🚀 Nasıl Çalıştırılır?

1.  Bu projenin dosyalarını bilgisayarınıza indirin veya klonlayın.
2.  Terminali veya komut istemcisini projenin bulunduğu dizinde açın.
3.  Yukarıdaki gereksinimlerin kurulu olduğundan emin olun.
4.  Aşağıdaki komut ile uygulamayı başlatın:

```bash
python yoskPixel.py
```


## 📖 Kullanım Kılavuzu

### Araç Kutusu (Toolbar)

*   **Araçlar:** "Kalem", "Silgi", "Kova" veya "Seçici" araçlarından birini seçmek için ilgili butona tıklayın. Seçili araç vurgulanacaktır.
*   **Renk:**
    *   Mevcut seçili rengi büyük karede görebilirsiniz.
    *   `Palet...` butonuna tıklayarak sistemin renk seçicisini açabilir ve istediğiniz rengi seçebilirsiniz.
    *   Hazır renk paletindeki küçük karelere tıklayarak hızlıca renk değiştirebilirsiniz.
*   **Seçenekler:**
    *   `Fırça Boyutu` kaydırıcısı ile kalem ve silginin boyutunu ayarlayın.
    *   `Simetri` bölümünden çizim yaparken kullanılacak ayna modunu seçin.
*   **Animasyon:**
    *   `Efekt Uygula` butonuna tıklayarak animasyon ayarları penceresini açın.

### Animasyon Efektleri

`Efekt Uygula` butonuna tıkladığınızda açılan pencereden:

1.  **Efekt Türü**'nü seçin (Glitch, Scanline, Noise).
2.  Her efektin kendine özgü ayarlarını (yoğunluk, hız, kalınlık vb.) yapın.
3.  **OK**'a basarak animasyonu başlatın.
4.  Animasyon çalışırken çizim yapamazsınız. Durdurmak için **Durdur** butonuna basın.
5.  Animasyon durduktan sonra, çalışmanızı **Dosya > GIF Olarak Kaydet...** menüsünden kaydedebilirsiniz.

### Menü Çubuğu

*   **Dosya:**
    *   `Yeni Tuval...`: Farklı boyutlarda yeni bir çalışma alanı açar.
    *   `Aç (PNG)...`: Bilgisayarınızdan bir PNG dosyasını tuvale yükler.
    *   `PNG Olarak Kaydet...`: Mevcut tuval görüntüsünü PNG olarak kaydeder.
    *   `GIF Olarak Kaydet...`: Oluşturulan animasyon karelerini GIF olarak kaydeder.
*   **Düzenle:**
    *   `Geri Al`: Son çizim eylemini geri alır.
    *   `Tuvali Temizle`: Tüm tuvali beyaza boyar.
*   **Görünüm:**
    *   `Izgarayı Göster`: Çalışma alanındaki ızgarayı açar veya kapatır.
    *   `Temalar`: Uygulamanın görünümünü değiştirir.

### Kısayollar

*   **`Ctrl + Z`**: Son yapılan işlemi geri alır.
## Örnek Görseller

![example](https://github.com/user-attachments/assets/04257784-5054-4ff3-884a-e6569b27d369)


<img width="320" height="320" alt="kask" src="https://github.com/user-attachments/assets/41dc8504-6752-42f5-97c6-d196953c90eb" />
