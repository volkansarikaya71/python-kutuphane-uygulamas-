import json
import os

DOSYA_ADI = "kitaplar.json"


#region Kayıtlı kitapları getir
def kitaplari_yukle():
    try:
        with open(DOSYA_ADI, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Kayıt dosyası bulunamadı. Yeni bir liste oluşturuldu.\n")
        return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Dosya okunurken hata oluştu: {e}. Boş listeyle başlanıyor.\n")
        return []
#endregion

#region Kitapları Kaydet
def kitaplari_kaydet(kitaplar):
    try:
        with open(DOSYA_ADI, "w", encoding="utf-8") as f:
            json.dump(kitaplar, f, ensure_ascii=False, indent=2)
        print("Kitaplar başarıyla kaydedildi.")
    except IOError as e:
        print(f"Dosyaya kaydedilirken hata oluştu: {e}")
#endregion

#region Kayıtlı Kitapları ekrana yazdır
def kitap_listesi_yazdir(kitaplar, baslik="KİTAP LİSTESİ"):
    print(f"\n--- {baslik} ---")
    if not kitaplar:
        print("Gösterilecek kitap yok.")
    else:
        for i, kitap in enumerate(kitaplar, 1):
            durum = "okundu" if kitap["okundu"] else "okunmadı"
            puan_str = f"  ★{kitap['puan']}" if kitap.get("puan") else ""
            print(f"{i:>3}. {kitap['baslik']} — {kitap['yazar']} [{durum}]{puan_str}")
    print("-" * 30)
#endregion

#region Veri girişi kontrol
def girdi_al(mesaj, zorunlu=True):
    while True:
        deger = input(mesaj).strip()
        if deger.lower() == "iptal":
            return None
        if zorunlu and not deger:
            print("Bu alan boş olamaz! (Vazgeçmek için 'iptal' yazın)")
            continue
        return deger
#endregion

#region AnaMenuyu Ekrana Yazdirma
def menu_goster(kitaplar):
    toplam = len(kitaplar)
    okunmus = sum(1 for k in kitaplar if k["okundu"])
    okunmamis = toplam - okunmus
    print("\n" + "=" * 35)
    print("    --- KİTAP TAKİP UYGULAMASI ---")
    print(f"    Toplam: {toplam} kitap  |  ✓ {okunmus}  ✗ {okunmamis}")
    print("=" * 35)
    print("  1. Kitapları Listele")
    print("  2. Yeni Kitap Ekle")
    print("  3. Okundu/Okunmadı İşaretle")
    print("  4. Kitap Sil")
    print("  5. Çıkış")
    print("=" * 35)
#endregion

#region Kitapları Göster
def kitaplari_listele(kitaplar):
    kitap_listesi_yazdir(kitaplar)
    input("\nListeden çıkmak için ENTER veya q'ya basın: ")
#endregion

#region kitap Ekle
def kitap_ekle(kitaplar):
    print("\n--- YENİ KİTAP EKLE --- ('iptal' yazarak vazgeçebilirsiniz)")

    baslik = girdi_al("Kitap başlığı: ")
    if baslik is None:
        print("Ekleme iptal edildi.")
        return

    yazar = girdi_al("Yazar: ")
    if yazar is None:
        print("Ekleme iptal edildi.")
        return

    yeni_kitap = {
        "baslik": baslik,
        "yazar":  yazar,
        "okundu": False
    }
    kitaplar.append(yeni_kitap)
    kitaplari_kaydet(kitaplar)
    print(f"'{baslik}' eklendi.")
#endregion

#region kitap okundu mu okunmadı mı durumunu ayarlama
def durum_degistir(kitaplar):
    if not kitaplar:
        print("\nKayıtlı kitap yok.")
        return

    while True:
        kitap_listesi_yazdir(kitaplar)
        print("(Menüye dönmek için q yazın)")
        secim = input("Durumunu değiştirmek istediğiniz kitabın numarası: ").strip()

        if secim.lower() == "q":
            break

        try:
            idx = int(secim) - 1
            if 0 <= idx < len(kitaplar):
                kitaplar[idx]["okundu"] = not kitaplar[idx]["okundu"]
                durum = "okundu" if kitaplar[idx]["okundu"] else "okunmadı"
                print(f"'{kitaplar[idx]['baslik']}' artık [{durum}] olarak işaretlendi.")
                kitaplari_kaydet(kitaplar)

                onay = input("Başka bir kitabın durumunu değiştirmek ister misiniz? (e/h): ").strip().lower()
                if onay != "e":
                    break
            else:
                print("Geçersiz kitap numarası!")
        except ValueError:
            print("Lütfen bir sayı girin!")
#endregion

#region kitap sil
def kitap_sil(kitaplar):
    if not kitaplar:
        print("\nKayıtlı kitap yok.")
        return

    kitap_listesi_yazdir(kitaplar)
    secim = input("Silmek istediğiniz kitabın numarası: ").strip()

    try:
        id = int(secim) - 1
        if 0 <= id < len(kitaplar):
            silinen = kitaplar.pop(id)
            kitaplari_kaydet(kitaplar)
            print(f"'{silinen['baslik']}' silindi.")
        else:
            print("Geçersiz kitap numarası!")
    except ValueError:
        print("Lütfen bir sayı girin!")
#endregion

#region AnaEkran yüklediginde gelecek menu
def main():
    print("\nKitap Takip Uygulamasına Hoş Geldiniz!")
    kitaplar = kitaplari_yukle()

    if kitaplar:
        print(f"{len(kitaplar)} kayıtlı kitap yüklendi.")

    while True:
        menu_goster(kitaplar)

        secim = input("\nSeçiminiz (1-5): ").strip()

        if secim == "1":
            kitaplari_listele(kitaplar)
        elif secim == "2":
            kitap_ekle(kitaplar)
        elif secim == "3":
            durum_degistir(kitaplar)
        elif secim == "4":
            kitap_sil(kitaplar)
        elif secim == "5":
            print("\nProgramdan çıkılıyor... İyi okumalar!")
            break
        else:
            print("Geçersiz seçim! Lütfen 1-5 arası bir değer girin.")


if __name__ == "__main__":
    main()
#endregion