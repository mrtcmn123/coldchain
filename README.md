# 📦 Stok Yönetim Sistemi – Geliştirme Yol Haritası

Bu proje, ürün stoklarının yönetimini kolaylaştırmak ve stok hareketlerini daha şeffaf ve güvenilir bir şekilde takip etmek için geliştirilmektedir. Aşağıda, planlanan özellikler ve geliştirme adımları yer almaktadır.

---

## 🧭 Gösterge Paneli (Dashboard) İyileştirmeleri
- [ ] Gösterge paneli düğmelerine yönlendirme (routing) işlevi ekle  
- [ ] Google sekmesine ikon ekle  
- [ ] Mevcut Stok Dashboard üzerinde verileri create ederken create edferken girilen birim değerine bağlı filtreleme ekleme.
- [ ] Profil sekmesi uzeridneki settings ve ayarlar kismi calisacak sekilde guncellenecek

## 🧾 PDF ve Stok Raporlaması
- [ ] Sadece kritik stoklar değil, tüm stoklar için PDF raporu üret  
- [ ] Ürün stoğu kritik seviyenin altına düştüğünde uyarı ver  {{user_alerts}}
- [ ] Hangi kullanıcının stok giriş/çıkış işlemi yaptığını gösteren raporlar sun  

## ➕ Ürün Yönetimi
- [] Ürün oluşturulurken otomatik SKU değeri üret  
- [] Ürün oluşturma sayfasında dil kullanımını (Türkçe/İngilizce) tutarlı hale getir  
- [] Yeni ürün eklerken giriş alanlarını doğrula  
- urun olusturulurken min max sicaklik degeri girebilsin
- [ ] Ürün oluşturulurken sıcaklık aralığı uygun değilse kullanıcıyı uyar   {{user_alerts}}
- Name'i ayni olan urunleri kaydetme


## 📉 Stok İşlemleri ve Güncellemeleri
- [] Mevcut ürün miktarı değiştirilirken birim tutarlılığını zorunlu kıl  
- [] `/inventory/products/` sayfasını stok giriş/çıkış/güncelleme işlemlerini destekleyecek şekilde yeniden yapılandır  
- [ ] Grafiklerin doğru kaynaktan veri çekmesini sağla  
- [] `Stock` ve `Product` modellerini birleştirerek tek bir yapı haline getir  
- [] Cıkış yapma işlemleri navbar"a ekle

## 📊 Tahminleme ve Uyarılar
- [ ] Giriş/çıkış tahminine dayalı olarak stok tükenme tarihini hesapla  
- [ ] Her depo için sıcaklık takibi yap ve her ürün için gereken sıcaklık aralığını tanımla  
- [ ] Depo sıcaklığı ürünler için risk oluşturuyorsa uyarı ver  

## 🖼️ UI/UX – Modal Geliştirmeleri
- [ ] Stok sayfasındaki modal pencerelerde giriş/çıkış kayıtlarının yanına "Düzenle" düğmesi ekle  

## 🗄️ Veri ve Altyapı
- [ ] Veritabanında 6 aylık örnek veri oluştur  
- [ ] Alan adı ve hosting altyapısını kur  
