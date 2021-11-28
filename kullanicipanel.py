import sqlite3,random,hashlib,ssl,smtplib,os
import tkinter as tk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class kullanicipanel():
    def __init__(self):
        self.con=sqlite3.connect("film.db")
        self.durum=True
        with open("kullaniciAdi.txt","r") as f:
            self.kullaniciAdi=f.read()
        self.eposta = list(self.con.execute(f"select EPosta from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
        self.isim = list(self.con.execute(f"select Isim from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
        self.eposta = self.eposta[0]
        self.isim = self.isim[0]
    def izle(self,film):
        try:
            if "Film Adı" not in film:
                hata = messagebox.showerror("Hata", "Sadece Film adı secilebilir")
            else:
                film = film.split("Film Adı: ")[1]
                izlenme=list(self.con.execute(f"select Izlenme from film where FilmAd='{film}'"))
                izlenme=izlenme[0]
                self.con.execute(f"UPDATE film set Izlenme ={int(izlenme[0])+1} where FilmAd='{film}'")
                otoizleme = list(self.con.execute(f"select OtoIzlemeListesi from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
                otoizleme = otoizleme[0]
                if otoizleme[0]=="1":
                    izlemeListesindekiFilmler = list(self.con.execute(
                        f"select IzlemeListesi from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
                    izlemeListesindekiFilmler = izlemeListesindekiFilmler[0]
                    izlemeListesindekiFilmler = str(izlemeListesindekiFilmler[0]).replace("[", "").replace("]","").split(",")
                    if film in izlemeListesindekiFilmler:
                        izlemeListesindekiFilmler.remove(film)
                    izlemeListesindekiFilmler = str(izlemeListesindekiFilmler).replace(",", "").replace("'", ",").replace("[,","[").replace( " ,", "").replace(",]", "]")
                    self.con.execute(f"UPDATE kullanicilar SET IzlemeListesi='{izlemeListesindekiFilmler}' where KullaniciAdi='{self.kullaniciAdi}'")
                self.con.commit()
                os.startfile("filmler\\" + film + ".mp4")
        except FileNotFoundError:
            hata = messagebox.showerror("Hata", "Üzgünüz\nDosya şuan kullanılamıyor..\nEn kısa sürede düzeltilecektir")
            mesaj = f"{film} mp4 dosyasi eksik"
            kullanici = ""
            sifre = ""
            context = ssl.create_default_context()
            port = 465
            host = 'smtp.gmail.com'
            posta = MIMEMultipart()
            posta['From'] = kullanici
            posta['To'] = kullanici
            posta['Subject'] = "Eksik mp4 dosyası"
            posta.attach(MIMEText(mesaj, 'plain'))
            eposta_sunucu = smtplib.SMTP_SSL(host=host, port=port, context=context)
            eposta_sunucu.login(kullanici, sifre)
            eposta_sunucu.sendmail(kullanici, kullanici, str(posta))
    def begen(self,film):
        if "Film Adı" not in film:
            hata = messagebox.showerror("Hata", "Sadece Film adı secilebilir")
        else:
            begenilenFilmler = list(self.con.execute(f"select BegenilenFilmler from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
            begenilenFilmler = begenilenFilmler[0]
            begenilenFilmler = str(begenilenFilmler[0]).replace("[", "").replace("]", "").split(",")
            begenilmeyenFilmler = list(self.con.execute(f"select BegenilmeyenFilmler from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
            begenilmeyenFilmler = begenilmeyenFilmler[0]
            begenilmeyenFilmler = str(begenilmeyenFilmler[0]).replace("[", "").replace("]", "").split(",")
            film = film.split("Film Adı: ")[1]
            begenmeSayisi = list(self.con.execute(f"select BegenmeSayisi from film where FilmAd='{film}'"))
            begenmeSayisi = begenmeSayisi[0]
            for m in begenilmeyenFilmler:
                if m == film:
                    begenmemeSayisi = list(self.con.execute(f"select BegenmemeSayisi from film where FilmAd='{film}'"))
                    begenmemeSayisi = begenmemeSayisi[0]
                    self.con.execute((f"UPDATE film SET BegenmemeSayisi='{int(begenmemeSayisi[0]) - 1}' where FilmAd='{film}'"))
                    begenilmeyenFilmler.remove(m)
                    begenilenFilmler.append(m)
                    self.con.execute((f"UPDATE film SET BegenmeSayisi='{int(begenmeSayisi[0]) + 1}' where FilmAd='{film}'"))
            if film not in begenilenFilmler:
                begenilenFilmler.append(film)
                self.con.execute((f"UPDATE film SET BegenmeSayisi='{int(begenmeSayisi[0]) + 1}' where FilmAd='{film}'"))
            begenilenFilmler = str(begenilenFilmler).replace(",", "").replace("'", ",").replace("[,", "[").replace(" ,", "").replace(",]","]").replace("[,","[")
            begenilmeyenFilmler = str(begenilmeyenFilmler).replace(",", "").replace("'", ",").replace("[,","[").replace(" ,","").replace(",]", "]").replace("[,","[")
            self.con.execute(f"UPDATE kullanicilar SET BegenilmeyenFilmler='{begenilmeyenFilmler}' where KullaniciAdi='{self.kullaniciAdi}'")
            self.con.execute(f"UPDATE kullanicilar SET BegenilenFilmler='{begenilenFilmler}' where KullaniciAdi='{self.kullaniciAdi}'")
            self.con.commit()
    def begenme(self,film):
        if "Film Adı" not in film:
            hata = messagebox.showerror("Hata", "Sadece Film adı secilebilir")
        else:
            begenilenFilmler = list(self.con.execute(f"select BegenilenFilmler from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
            begenilenFilmler = begenilenFilmler[0]
            begenilenFilmler = str(begenilenFilmler[0]).replace("[", "").replace("]", "").split(",")
            begenilmeyenFilmler = list(self.con.execute(f"select BegenilmeyenFilmler from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
            begenilmeyenFilmler = begenilmeyenFilmler[0]
            begenilmeyenFilmler = str(begenilmeyenFilmler[0]).replace("[", "").replace("]", "").split(",")
            film = film.split("Film Adı: ")[1]
            begenmemeSayisi = list(self.con.execute(f"select BegenmemeSayisi from film where FilmAd='{film}'"))
            begenmemeSayisi = begenmemeSayisi[0]
            for m in begenilenFilmler:
                if m == film:
                    begenmeSayisi = list(self.con.execute(f"select BegenmeSayisi from film where FilmAd='{film}'"))
                    begenmeSayisi = begenmeSayisi[0]
                    self.con.execute((f"UPDATE film SET BegenmemeSayisi='{int(begenmemeSayisi[0]) + 1}' where FilmAd='{film}'"))
                    begenilmeyenFilmler.append(m)
                    begenilenFilmler.remove(m)
                    self.con.execute((f"UPDATE film SET BegenmeSayisi='{int(begenmeSayisi[0]) - 1}' where FilmAd='{film}'"))
            if film not in begenilmeyenFilmler:
                begenilmeyenFilmler.append(film)
                self.con.execute((f"UPDATE film SET BegenmemeSayisi='{int(begenmemeSayisi[0]) + 1}' where FilmAd='{film}'"))
            begenilenFilmler = str(begenilenFilmler).replace(",", "").replace("'", ",").replace("[,", "[").replace(" ,", "").replace(",]","]")
            begenilmeyenFilmler = str(begenilmeyenFilmler).replace(",", "").replace("'", ",").replace("[,","[").replace(" ,","").replace(",]", "]").replace("[,","[")
            self.con.execute(f"UPDATE kullanicilar SET BegenilmeyenFilmler='{begenilmeyenFilmler}' where KullaniciAdi='{self.kullaniciAdi}'")
            self.con.execute(f"UPDATE kullanicilar SET BegenilenFilmler='{begenilenFilmler}' where KullaniciAdi='{self.kullaniciAdi}'")
            self.con.commit()
    def izlemeListemeEkle(self,film):
        if "Film Adı" not in film:
            hata = messagebox.showerror("Hata", "Sadece Film adı secilebilir")
        else:
            film = film.split("Film Adı: ")[1]
            izlemeListesi=[]
            izlemeListesiVT = list(self.con.execute(f"select IzlemeListesi from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
            izlemeListesiVT = izlemeListesiVT[0]
            for i in izlemeListesiVT:
                a = str(i).replace("[", "").replace("]", "").split(",")
                for m in a:
                    if m != "":
                        if m not in izlemeListesi:
                            izlemeListesi.append(m)
            if film not in izlemeListesi:
                izlemeListesi.append(film)
            izlemeListesi = str(izlemeListesi).replace(",", "").replace("'", ",").replace("[,", "[").replace(" ,", "").replace(",]","]")
            self.con.execute(f"UPDATE kullanicilar SET IzlemeListesi='{izlemeListesi}' where KullaniciAdi='{self.kullaniciAdi}'")
            self.con.commit()
    def butunFilmleriGoster(self):
        def izle():
            film = listbox.get(listbox.curselection())
            self.izle(film)
        def begen():
            film = listbox.get(listbox.curselection())
            self.begen(film)
        def begenme():
            film = listbox.get(listbox.curselection())
            self.begenme(film)
        def izlemeListemeEkle():
            film = listbox.get(listbox.curselection())
            self.izlemeListemeEkle(film)
        butunFilmleriGosterForm=tk.Tk()
        butunFilmleriGosterForm.title("Butun Filmleri Goster")
        butunFilmleriGosterForm.geometry("500x300")

        butunFilmler=list(self.con.execute("select * from film"))
        listbox = tk.Listbox(butunFilmleriGosterForm, selectmode=tk.SINGLE, font=18, width=500, height=8)
        listbox.pack(pady=10)
        for i in butunFilmler:
            listbox.insert(tk.END, f"Film Adı: {i[0]}")
            listbox.insert(tk.END, f"Yapım Yılı: {i[1]}")
            listbox.insert(tk.END, f"Yapımcı: {i[2]}")
            listbox.insert(tk.END, f"İzlenme: {i[3]}")
            listbox.insert(tk.END, f"Kategori: {i[4]}")
            listbox.insert(tk.END, f"Begenme Sayısı: {i[5]}")
            listbox.insert(tk.END, f"Begenmeme Sayisi: {i[6]}")
            listbox.insert(tk.END, "")
        izle = tk.Button(butunFilmleriGosterForm, text="İzle", width=8, command=izle).place(x=430, y=180)
        begenBtn = tk.Button(butunFilmleriGosterForm, text="Begendim", command=begen).place(x=360, y=180)
        begenmeBtn = tk.Button(butunFilmleriGosterForm, text="Begenmedim", command=begenme).place(x=273, y=180)
        izlemeListemeEkleBtn = tk.Button(butunFilmleriGosterForm, text="İzleme Listeme Ekle", command=izlemeListemeEkle).place(x=155, y=180)
        butunFilmleriGosterForm.mainloop()
    def kategoriSec(self):
        def ara():
            def izle():
                film = listbox.get(listbox.curselection())
                self.izle(film)
            def begen():
                film = listbox.get(listbox.curselection())
                self.begen(film)
            def begenme():
                film = listbox.get(listbox.curselection())
                self.begenme(film)
            def izlemeListemeEkle():
                film = listbox.get(listbox.curselection())
                self.izlemeListemeEkle(film)
            listbox.delete(0, tk.END)
            listbox.place(x=0, y=110, height=150)
            kategoriler = checkvar1.get(), checkvar2.get(), checkvar3.get(), checkvar4.get(), checkvar5.get(), checkvar6.get(), checkvar7.get(), checkvar8.get(), checkvar9.get(), checkvar10.get(), checkvar11.get(), checkvar12.get(), checkvar13.get(), checkvar14.get(), checkvar15.get(), checkvar16.get(), checkvar17.get(), checkvar18.get(), checkvar19.get(), checkvar20.get(), checkvar21.get(), checkvar22.get()
            kategoriler = list(kategoriler)
            kategori = []
            yeniFilmListesi = []
            for i in kategoriler:
                if i != 0:
                    kategori.append(i)
            kategori = str(kategori).split("[")[1].split("]")[0]
            if len(kategori) == 0:
                hata = messagebox.showerror("Hata", "en az 1 kategori secilmelidir")
            else:
                filmler = list(self.con.execute("select * from film"))
                for i in filmler:
                    if kategori in i[4]:
                        yeniFilmListesi.append(i)
                for i in yeniFilmListesi:
                    listbox.insert(tk.END, f"Film Adı: {i[0]}")
                    listbox.insert(tk.END, f"Yapım Yılı: {i[1]}")
                    listbox.insert(tk.END, f"Yapımcı: {i[2]}")
                    listbox.insert(tk.END, f"İzlenme: {i[3]}")
                    listbox.insert(tk.END, f"Kategori: {i[4]}")
                    listbox.insert(tk.END, f"Begenme Sayısı: {i[5]}")
                    listbox.insert(tk.END, f"Begenmeme Sayisi: {i[6]}")
                    listbox.insert(tk.END, "")
                izle = tk.Button(kategoriSecForm, text="İzle", width=8, command=izle).place(x=430, y=265)
                begenBtn = tk.Button(kategoriSecForm, text="Begendim", command=begen).place(x=360, y=265)
                begenmeBtn = tk.Button(kategoriSecForm, text="Begenmedim", command=begenme).place(x=273, y=265)
                izlemeListemeEkleBtn = tk.Button(kategoriSecForm, text="İzleme Listeme Ekle",command=izlemeListemeEkle).place(x=155, y=265)
            checkvar1.set(0)
            checkvar2.set(0)
            checkvar3.set(0)
            checkvar4.set(0)
            checkvar5.set(0)
            checkvar6.set(0)
            checkvar7.set(0)
            checkvar8.set(0)
            checkvar9.set(0)
            checkvar10.set(0)
            checkvar11.set(0)
            checkvar12.set(0)
            checkvar13.set(0)
            checkvar14.set(0)
            checkvar15.set(0)
            checkvar16.set(0)
            checkvar17.set(0)
            checkvar18.set(0)
            checkvar19.set(0)
            checkvar20.set(0)
            checkvar21.set(0)
            checkvar22.set(0)
        kategoriSecForm=tk.Tk()
        kategoriSecForm.title("Burak Film")
        kategoriSecForm.geometry("500x300")

        checkvar1 = tk.IntVar()
        checkvar2 = tk.IntVar()
        checkvar3 = tk.IntVar()
        checkvar4 = tk.IntVar()
        checkvar5 = tk.IntVar()
        checkvar6 = tk.IntVar()
        checkvar7 = tk.IntVar()
        checkvar8 = tk.IntVar()
        checkvar9 = tk.IntVar()
        checkvar10 = tk.IntVar()
        checkvar11 = tk.IntVar()
        checkvar12 = tk.IntVar()
        checkvar13 = tk.IntVar()
        checkvar14 = tk.IntVar()
        checkvar15 = tk.IntVar()
        checkvar16 = tk.IntVar()
        checkvar17 = tk.IntVar()
        checkvar18 = tk.IntVar()
        checkvar19 = tk.IntVar()
        checkvar20 = tk.IntVar()
        checkvar21 = tk.IntVar()
        checkvar22 = tk.IntVar()

        c1 = tk.Checkbutton(kategoriSecForm, text="Aile", variable=checkvar1, onvalue=10).place(x=10, y=10)
        c2 = tk.Checkbutton(kategoriSecForm, text="Aksiyon", variable=checkvar2, onvalue=11).place(x=85, y=10)
        c3 = tk.Checkbutton(kategoriSecForm, text="Animasyon", variable=checkvar3, onvalue=12).place(x=175, y=10)
        c4 = tk.Checkbutton(kategoriSecForm, text="Anime", variable=checkvar4, onvalue=13).place(x=260, y=10)
        c5 = tk.Checkbutton(kategoriSecForm, text="Aşk", variable=checkvar5, onvalue=14).place(x=340, y=10)
        c6 = tk.Checkbutton(kategoriSecForm, text="Bağımsız", variable=checkvar6, onvalue=15).place(x=410, y=10)
        c7 = tk.Checkbutton(kategoriSecForm, text="Belgesel", variable=checkvar7, onvalue=16).place(x=10, y=35)
        c8 = tk.Checkbutton(kategoriSecForm, text="Bilim Kurgu", variable=checkvar8, onvalue=17).place(x=85, y=35)
        c9 = tk.Checkbutton(kategoriSecForm, text="Doğaüstü", variable=checkvar9, onvalue=18).place(x=175, y=35)
        c10 = tk.Checkbutton(kategoriSecForm, text="Drama", variable=checkvar10, onvalue=19).place(x=260, y=35)
        c11 = tk.Checkbutton(kategoriSecForm, text="Epik", variable=checkvar11, onvalue=20).place(x=340, y=35)
        c12 = tk.Checkbutton(kategoriSecForm, text="Fantazi", variable=checkvar12, onvalue=21).place(x=410, y=35)
        c13 = tk.Checkbutton(kategoriSecForm, text="Gerilim", variable=checkvar13, onvalue=22).place(x=10, y=60)
        c14 = tk.Checkbutton(kategoriSecForm, text="Gizem", variable=checkvar14, onvalue=23).place(x=85, y=60)
        c15 = tk.Checkbutton(kategoriSecForm, text="Komedi", variable=checkvar15, onvalue=24).place(x=175, y=60)
        c16 = tk.Checkbutton(kategoriSecForm, text="Korku", variable=checkvar16, onvalue=25).place(x=260, y=60)
        c17 = tk.Checkbutton(kategoriSecForm, text="Mecara", variable=checkvar17, onvalue=26).place(x=340, y=60)
        c18 = tk.Checkbutton(kategoriSecForm, text="Muzikal", variable=checkvar18, onvalue=27).place(x=410, y=60)
        c19 = tk.Checkbutton(kategoriSecForm, text="Spor", variable=checkvar19, onvalue=28).place(x=10, y=85)
        c20 = tk.Checkbutton(kategoriSecForm, text="Suç", variable=checkvar20, onvalue=29).place(x=85, y=85)
        c21 = tk.Checkbutton(kategoriSecForm, text="Western", variable=checkvar21, onvalue=30).place(x=175, y=85)
        c22 = tk.Checkbutton(kategoriSecForm, text="Çizgi Film", variable=checkvar22, onvalue=31).place(x=260,y=85)
        listbox=tk.Listbox(kategoriSecForm,width=500, height=8,font=18)
        arabtn=tk.Button(kategoriSecForm,text="Ara",width=5,command=ara).place(x=345, y=82)
        kategoriSecForm.mainloop()
    def randomFilm(self):
        def randomFilmGetir():
            def izle():
                film = listbox.get(listbox.curselection())
                self.izle(film)
            def begen():
                film = listbox.get(listbox.curselection())
                self.begen(film)
            def begenme():
                film = listbox.get(listbox.curselection())
                self.begenme(film)
            def izlemeListemeEkle():
                film = listbox.get(listbox.curselection())
                self.izlemeListemeEkle(film)
            listbox.delete(0, tk.END)
            listbox.pack(pady=35)
            if randomfilm.get() > len(FilmAdListesi):
                hata = messagebox.showerror("Hata","Veri Tabanında şuanda bu kadar film yok lütfen daha düşük bir sayi giriniz")
            randomFilmListe = []
            while len(randomFilmListe) < randomfilm.get():
                randomFilm = random.choice(FilmAdListesi)
                if randomFilm not in randomFilmListe:
                    randomFilmListe.append(randomFilm)
            for i in randomFilmListe:
                film = list(self.con.execute(f"select * from film where FilmAd='{i[0]}'"))
                film=film[0]
                listbox.insert(tk.END, f"Film Adı: {film[0]}")
                listbox.insert(tk.END, f"Yapım Yılı: {film[1]}")
                listbox.insert(tk.END, f"Yapımcı: {film[2]}")
                listbox.insert(tk.END, f"İzlenme: {film[3]}")
                listbox.insert(tk.END, f"Kategori: {film[4]}")
                listbox.insert(tk.END, f"Begenme Sayısı: {film[5]}")
                listbox.insert(tk.END, f"Begenmeme Sayisi: {film[6]}")
                listbox.insert(tk.END, "")
            izle = tk.Button(randomFilmForm, text="İzle", width=8, command=izle).place(x=430, y=200)
            begenBtn = tk.Button(randomFilmForm, text="Begendim", command=begen).place(x=360, y=200)
            begenmeBtn = tk.Button(randomFilmForm, text="Begenmedim", command=begenme).place(x=273, y=200)
            izlemeListemeEkleBtn = tk.Button(randomFilmForm, text="İzleme Listeme Ekle",command=izlemeListemeEkle).place(x=155, y=200)
        randomFilmForm = tk.Tk()
        randomFilmForm.title("Burak Film")
        randomFilmForm.geometry("500x300")

        randomfilm = tk.IntVar()
        FilmAdListesi = list(self.con.execute("select FilmAd from film"))
        filmLabel = tk.Label(randomFilmForm, text="Random Film Miktari: ").place(x=10, y=10)
        filmSpinbox = tk.Spinbox(randomFilmForm, textvariable=randomfilm,from_=1, to=len(FilmAdListesi), width=2).place(x=140, y=10)
        filmButton = tk.Button(randomFilmForm, text="Arat", command=randomFilmGetir).place(x=170, y=7)
        listbox = tk.Listbox(randomFilmForm, selectmode=tk.SINGLE, font=18, width=500, height=8)

        randomFilmForm.mainloop()
    def yapimYili(self):
        def ara():
            def izle():
                film = listbox.get(listbox.curselection())
                self.izle(film)
            def begen():
                film = listbox.get(listbox.curselection())
                self.begen(film)
            def begenme():
                film = listbox.get(listbox.curselection())
                self.begenme(film)
            def izlemeListemeEkle():
                film = listbox.get(listbox.curselection())
                self.izlemeListemeEkle(film)
            filmler=[]
            listbox.delete(0, tk.END)
            listbox.pack(pady=60)
            if yapimYili.get()!="":
                filmler.append(list(self.con.execute(f"select * from film where YapimYili={yapimYili.get()}")))
            for i in yapimYiliListbox.curselection():
                filmler.append(list(self.con.execute(f"select * from film where YapimYili={yapimYiliListbox.get(i)[0]}")))
            for x in filmler:
                for i in x:
                    listbox.insert(tk.END, f"Film Adı: {i[0]}")
                    listbox.insert(tk.END, f"Yapım Yılı: {i[1]}")
                    listbox.insert(tk.END, f"Yapımcı: {i[2]}")
                    listbox.insert(tk.END, f"İzlenme: {i[3]}")
                    listbox.insert(tk.END, f"Kategori: {i[4]}")
                    listbox.insert(tk.END, f"Begenme Sayısı: {i[5]}")
                    listbox.insert(tk.END, f"Begenmeme Sayisi: {i[6]}")
                    listbox.insert(tk.END, "")
            izle = tk.Button(yapimYiliForm, text="İzle", width=8, command=izle).place(x=430, y=225)
            begenBtn = tk.Button(yapimYiliForm, text="Begendim", command=begen).place(x=360, y=225)
            begenmeBtn = tk.Button(yapimYiliForm, text="Begenmedim", command=begenme).place(x=273, y=225)
            izlemeListemeEkleBtn = tk.Button(yapimYiliForm, text="İzleme Listeme Ekle",command=izlemeListemeEkle).place(x=155, y=225)
            yapimYili.set("")
        yapimYiliForm = tk.Tk()
        yapimYiliForm.title("Burak Film")
        yapimYiliForm.geometry("500x300")

        yapimYili = tk.StringVar()

        yapimYiliLabel = tk.Label(yapimYiliForm, text="Yapim Yili Gir").place(x=10, y=10)
        yapimYiliEntry=tk.Entry(yapimYiliForm,textvariable=yapimYili,width=7).place(x=100,y=10)

        yapimyiliLabel2=tk.Label(yapimYiliForm,text="Yapim Yili Sec").place(x=10,y=35)
        yapimYiliListbox = tk.Listbox(yapimYiliForm, selectmode=tk.MULTIPLE, font=18, width=5, height=1)
        yapimYiliListbox.place(x=100, y=35)

        yapimYiliList=[]
        yapimYiliVeri=list(self.con.execute("select YapimYili from film"))
        for i in yapimYiliVeri:
            if i not in yapimYiliList:
                yapimYiliList.append(i)
        for i in yapimYiliList:
            yapimYiliListbox.insert(tk.END,i)

        listbox = tk.Listbox(yapimYiliForm, selectmode=tk.SINGLE, font=18, width=500, height=8,)
        yapimYiliButton = tk.Button(yapimYiliForm, text="Arat",width=6,height=3,command=ara).place(x=160, y=5)

        yapimYiliForm.mainloop()
    def yapimci(self):
        def ara():
            def izle():
                film = listbox.get(listbox.curselection())
                self.izle(film)
            def begen():
                film = listbox.get(listbox.curselection())
                self.begen(film)
            def begenme():
                film = listbox.get(listbox.curselection())
                self.begenme(film)
            def izlemeListemeEkle():
                film = listbox.get(listbox.curselection())
                self.izlemeListemeEkle(film)
            filmler=[]
            listbox.delete(0, tk.END)
            listbox.pack(pady=60)
            if yapimci.get()!="":
                filmler.append(list(self.con.execute(f"select * from film where Yapimci='{yapimci.get().lower().title()}'")))
            for i in yapimciListbox.curselection():
                filmler.append(list(self.con.execute(f"select * from film where Yapimci='{yapimciListbox.get(i)[0]}'")))
            for x in filmler:
                for i in x:
                    listbox.insert(tk.END, f"Film Adı: {i[0]}")
                    listbox.insert(tk.END, f"Yapım Yılı: {i[1]}")
                    listbox.insert(tk.END, f"Yapımcı: {i[2]}")
                    listbox.insert(tk.END, f"İzlenme: {i[3]}")
                    listbox.insert(tk.END, f"Kategori: {i[4]}")
                    listbox.insert(tk.END, f"Begenme Sayısı: {i[5]}")
                    listbox.insert(tk.END, f"Begenmeme Sayisi: {i[6]}")
                    listbox.insert(tk.END, "")
            izle = tk.Button(yapimciForm, text="İzle", width=8, command=izle).place(x=430, y=225)
            begenBtn = tk.Button(yapimciForm, text="Begendim", command=begen).place(x=360, y=225)
            begenmeBtn = tk.Button(yapimciForm, text="Begenmedim", command=begenme).place(x=273, y=225)
            izlemeListemeEkleBtn = tk.Button(yapimciForm, text="İzleme Listeme Ekle",command=izlemeListemeEkle).place(x=155, y=225)
            yapimci.set("")
        yapimciForm = tk.Tk()
        yapimciForm.title("Burak Film")
        yapimciForm.geometry("500x300")

        yapimci = tk.StringVar()

        yapimciLabel = tk.Label(yapimciForm, text="Yapimci Gir").place(x=10, y=10)
        yapimciEntry=tk.Entry(yapimciForm,textvariable=yapimci).place(x=90,y=10)

        yapimciLabel2=tk.Label(yapimciForm,text="Yapimci Sec").place(x=10,y=35)
        yapimciListbox = tk.Listbox(yapimciForm, selectmode=tk.MULTIPLE, font=18, width=13, height=1)
        yapimciListbox.place(x=90, y=35)

        yapimciList=[]
        yapimciVeri=list(self.con.execute("select Yapimci from film"))
        for i in yapimciVeri:
            if i not in yapimciList:
                yapimciList.append(i)
        for i in yapimciList:
            yapimciListbox.insert(tk.END,i)
        listbox = tk.Listbox(yapimciForm, selectmode=tk.SINGLE, font=18, width=500, height=8,)
        yapimYiliButton = tk.Button(yapimciForm, text="Arat",width=6,height=3,command=ara).place(x=220, y=5)

        yapimciForm.mainloop()
    def filmArat(self):
        def arat():
            def izle():
                film = listbox.get(listbox.curselection())
                self.izle(film)
            def begen():
                film = listbox.get(listbox.curselection())
                self.begen(film)
            def begenme():
                film = listbox.get(listbox.curselection())
                self.begenme(film)
            def izlemeListemeEkle():
                film = listbox.get(listbox.curselection())
                self.izlemeListemeEkle(film)
            listbox.delete(0, tk.END)
            listbox.pack(pady=35)
            filmListesi = list(self.con.execute("select FilmAd from film"))
            yeniFilmListesi = []
            for i in filmListesi:
                if filmara.get() in i[0] and i[0] not in yeniFilmListesi:
                    yeniFilmListesi.append(i[0])
                if filmara.get().lower().title() in i[0] and i[0] not in yeniFilmListesi:
                    yeniFilmListesi.append(i[0])
            for n in yeniFilmListesi:
                bulunanFilmler = list(self.con.execute(f"select * from film where FilmAd='{n}'"))
                for x in bulunanFilmler:
                    listbox.insert(tk.END, f"Film Adı: {x[0]}")
                    listbox.insert(tk.END, f"Yapım Yılı: {x[1]}")
                    listbox.insert(tk.END, f"Yapımcı: {x[2]}")
                    listbox.insert(tk.END, f"İzlenme: {x[3]}")
                    listbox.insert(tk.END, f"Kategori: {x[4]}")
                    listbox.insert(tk.END, f"Begenme Sayısı: {x[5]}")
                    listbox.insert(tk.END, f"Begenmeme Sayisi: {x[6]}")
                    listbox.insert(tk.END, "")
            izle=tk.Button(filmAratForm,text="İzle",width=8,command=izle).place(x=430,y=200)
            begenBtn = tk.Button(filmAratForm,text="Begendim",command=begen).place(x=360,y=200)
            begenmeBtn = tk.Button(filmAratForm, text="Begenmedim", command=begenme).place(x=273, y=200)
            izlemeListemeEkleBtn = tk.Button(filmAratForm, text="İzleme Listeme Ekle", command=izlemeListemeEkle).place(x=155, y=200)
        filmAratForm = tk.Tk()
        filmAratForm.title("Burak Film")
        filmAratForm.geometry("500x300")

        filmara=tk.StringVar()

        filmLabel=tk.Label(filmAratForm,text="Film Adı: ").place(x=10,y=10)
        filmEntry=tk.Entry(filmAratForm,textvariable=filmara).place(x=70,y=10)
        filmButton=tk.Button(filmAratForm,text="Arat",command=arat).place(x=210,y=7)
        listbox = tk.Listbox(filmAratForm, selectmode=tk.SINGLE, font=18, width=500,height=8)

        filmAratForm.mainloop()
    def izlemeListesiniGoster(self):
        def izle():
            film = listbox.get(listbox.curselection())
            self.izle(film)
        def begen():
            film = listbox.get(listbox.curselection())
            self.begen(film)
        def begenme():
            film = listbox.get(listbox.curselection())
            self.begenme(film)
        def izlemeListesindenKaldir():
            film = listbox.get(listbox.curselection())
            izlemeListesindekiFilmler.remove(film.split("Film Adı: ")[1])
            izlemeListesi = str(izlemeListesindekiFilmler).replace(",", "").replace("'", ",").replace("[,", "[").replace(" ,","").replace(",]", "]")
            self.con.execute(f"UPDATE kullanicilar SET IzlemeListesi='{izlemeListesi}' where KullaniciAdi='{self.kullaniciAdi}'")
            self.con.commit()
            izlemeListesiniGoster.destroy()
            self.izlemeListesiniGoster()
        izlemeListesiniGoster=tk.Tk()
        izlemeListesiniGoster.title("İzleme Listem")
        izlemeListesiniGoster.geometry("500x300")

        izlemeListesindekiFilmler=list(self.con.execute(f"select IzlemeListesi from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
        izlemeListesindekiFilmler=izlemeListesindekiFilmler[0]
        izlemeListesindekiFilmler = str(izlemeListesindekiFilmler[0]).replace("[","").replace("]","").split(",")
        listbox = tk.Listbox(izlemeListesiniGoster, selectmode=tk.SINGLE, font=18, width=500, height=8)
        listbox.pack(pady=10)
        if len(izlemeListesindekiFilmler)==1:
            hata=messagebox.showerror("Hata","İzleme Listenizde Film bulunmamaktadir")
            izlemeListesiniGoster.destroy()
        else:
            for i in izlemeListesindekiFilmler:
                filmler=list(self.con.execute(f"select * from film where FilmAd='{i}'"))
                for i in filmler:
                    listbox.insert(tk.END, f"Film Adı: {i[0]}")
                    listbox.insert(tk.END, f"Yapım Yılı: {i[1]}")
                    listbox.insert(tk.END, f"Yapımcı: {i[2]}")
                    listbox.insert(tk.END, f"İzlenme: {i[3]}")
                    listbox.insert(tk.END, f"Kategori: {i[4]}")
                    listbox.insert(tk.END, f"Begenme Sayısı: {i[5]}")
                    listbox.insert(tk.END, f"Begenmeme Sayisi: {i[6]}")
                    listbox.insert(tk.END, "")
            izle = tk.Button(izlemeListesiniGoster, text="İzle", width=8, command=izle).place(x=430, y=180)
            begenBtn = tk.Button(izlemeListesiniGoster, text="Begendim", command=begen).place(x=360, y=180)
            begenmeBtn = tk.Button(izlemeListesiniGoster, text="Begenmedim", command=begenme).place(x=273, y=180)
            izlemeListesindenKaldirBtn=tk.Button(izlemeListesiniGoster,text="İzleme Listemden Kaldir",command=izlemeListesindenKaldir).place(x=135,y=180)
        izlemeListesiniGoster.mainloop()
    def enCokBegenilenFilmler(self):
        def izle():
            film = listbox.get(listbox.curselection())
            self.izle(film)

        def begen():
            film = listbox.get(listbox.curselection())
            self.begen(film)

        def begenme():
            film = listbox.get(listbox.curselection())
            self.begenme(film)

        def izlemeListemeEkle():
            film = listbox.get(listbox.curselection())
            self.izlemeListemeEkle(film)

        enCokBegenilenFilmlerForm = tk.Tk()
        enCokBegenilenFilmlerForm.title("En Cok Begenilen Filmler")
        enCokBegenilenFilmlerForm.geometry("500x300")

        butunFilmler = list(self.con.execute("select * from film order by BegenmeSayisi desc"))
        listbox = tk.Listbox(enCokBegenilenFilmlerForm, selectmode=tk.SINGLE, font=18, width=500, height=8)
        listbox.pack(pady=10)
        for i in butunFilmler:
            listbox.insert(tk.END, f"Film Adı: {i[0]}")
            listbox.insert(tk.END, f"Yapım Yılı: {i[1]}")
            listbox.insert(tk.END, f"Yapımcı: {i[2]}")
            listbox.insert(tk.END, f"İzlenme: {i[3]}")
            listbox.insert(tk.END, f"Kategori: {i[4]}")
            listbox.insert(tk.END, f"Begenme Sayısı: {i[5]}")
            listbox.insert(tk.END, f"Begenmeme Sayisi: {i[6]}")
            listbox.insert(tk.END, "")
        izle = tk.Button(enCokBegenilenFilmlerForm, text="İzle", width=8, command=izle).place(x=430, y=180)
        begenBtn = tk.Button(enCokBegenilenFilmlerForm, text="Begendim", command=begen).place(x=360, y=180)
        begenmeBtn = tk.Button(enCokBegenilenFilmlerForm, text="Begenmedim", command=begenme).place(x=273, y=180)
        izlemeListemeEkleBtn = tk.Button(enCokBegenilenFilmlerForm, text="İzleme Listeme Ekle",command=izlemeListemeEkle).place(x=155, y=180)
        enCokBegenilenFilmlerForm.mainloop()
    def aktivasyonMail(self,isim,alici):
        self.aktivasyonKodu = random.randint(10000, 99999)
        kullanici = ""
        sifre = ""
        context = ssl.create_default_context()
        port = 465
        host = 'smtp.gmail.com'
        posta = MIMEMultipart()
        posta['From'] = kullanici
        posta['To'] = alici
        posta['Subject'] = "BurakFilm Aktivasyon Kodu"
        mesaj =f"Merhabalar {isim},\n\naktivasyon kodun:{self.aktivasyonKodu}\n\nİyi Günler"

        posta.attach(MIMEText(mesaj, 'plain'))

        eposta_sunucu = smtplib.SMTP_SSL(host=host, port=port, context=context)
        eposta_sunucu.login(kullanici, sifre)
        eposta_sunucu.sendmail(kullanici, alici, str(posta))
    def aktivasyon(self,isim,alici):
        self.hataliGiris = 0
        def gonder():
            if aktivasyon.get() == self.aktivasyonKodu:
                aktivasyonForm.destroy()
                return True
            else:
                self.hataliGiris += 1
                hata = messagebox.showerror("Uyarı", "Aktivasyon kodu hatali girildi Lütfen tekrar deneyiniz")
                if self.hataliGiris == 6:
                    hata = messagebox.showerror("Uyarı", "Aktivasyon kodunu 6 kere hatalı girdiğiniz için sizi menüye aktarıyorum")
                    aktivasyonForm.destroy()
                    self.program()
        def yeniAktivasyon():
            self.aktivasyonMail(isim,alici)
        aktivasyonForm=tk.Tk()
        aktivasyonForm.geometry("500x300")
        aktivasyonForm.title("Mail Aktivasyon")

        aktivasyon=tk.IntVar()

        mesaj=tk.Label(aktivasyonForm,text="Mailinize gelen aktivasyon kodunu giriniz").place(x=10,y=10)
        aktivasyonLabel=tk.Label(aktivasyonForm,text="Aktivasyon Kodu:").place(x=10,y=35)
        aktivasyonEntry=tk.Entry(aktivasyonForm,textvariable=aktivasyon).place(x=120,y=35)
        aktivasyonBtn=tk.Button(aktivasyonForm,text="Gonder",command=gonder).place(x=195,y=60)
        yeniAktivasyonKoduBtn=tk.Button(aktivasyonForm,text="Kodu Tekrar Gonder",command=yeniAktivasyon).place(x=70,y=60)
        aktivasyonForm.mainloop()
    def kontrol(self,kullanciAdi,sifre):
        hesap=list(self.con.execute(f"select Sifre from kullanicilar where KullaniciAdi= '{kullanciAdi}'"))
        SHA256Sifre = hashlib.sha256(sifre.encode("ascii")).hexdigest()
        if str(hesap[0]).split("'")[1] == SHA256Sifre:
            return True
        return False
    def epostaGuncelle(self):
        def gonder():
            def guncelle():
                uyari = messagebox.showinfo("Bilgi", "Girdiğiniz E-Posta adresine gelen onay kodunu giriniz")
                epostaGuncelleForm.destroy()
                self.aktivasyonMail("", eposta.get())
                if self.aktivasyon("", eposta.get()):
                    pass
                else:
                    self.con.execute(f"UPDATE kullanicilar SET EPosta='{eposta.get().lower()}' where KullaniciAdi='{self.kullaniciAdi}'")
                    self.con.commit()
            if self.kontrol(self.kullaniciAdi,sifre.get()):
                eposta=tk.StringVar()

                epostaLabel=tk.Label(epostaGuncelleForm,text="E-Posta: ")
                epostaLabel.place(x=10,y=110)
                epostaEntry=tk.Entry(epostaGuncelleForm,textvariable=eposta)
                epostaEntry.place(x=70,y=110)

                guncelleBtn=tk.Button(epostaGuncelleForm,text="Guncelle",command=guncelle)
                guncelleBtn.place(x=200,y=105)
            else:
                hata=messagebox.showerror("Hata","Girdiginiz sifre yanlis lutfen tekrar deneyiniz")
        epostaGuncelleForm=tk.Tk()
        epostaGuncelleForm.title("E-Posta Guncelle")
        epostaGuncelleForm.geometry("500x300")

        sifre=tk.StringVar()

        sifreLabel = tk.Label(epostaGuncelleForm, text="Sifre:").place(x=10, y=10)
        sifreEntry = tk.Entry(epostaGuncelleForm, textvariable=sifre,show="*").place(x=100, y=10)

        gonder=tk.Button(epostaGuncelleForm,text="Kontrol",command=gonder).place(x=175,y=35)
        epostaGuncelleForm.mainloop()
    def telGuncelle(self):
        def gonder():
            def guncelle():
                if len(telefon.get())!=11:
                    hata=messagebox.showerror("hata","Telefon 11 haneli olmak zorundadir")
                else:
                    self.con.execute(f"UPDATE kullanicilar SET Telefon='{telefon.get()}' where KullaniciAdi='{self.kullaniciAdi}'")
                    self.con.commit()
                    info=messagebox.showinfo("Bilgi","Telefon basariyla guncellendi")
                    telGuncelleForm.destroy()
            if self.kontrol(self.kullaniciAdi,sifre.get()):
                telefon=tk.StringVar()
                telefonLabel=tk.Label(telGuncelleForm,text="Telefon: ")
                telefonLabel.place(x=10,y=110)
                telefonEntry=tk.Entry(telGuncelleForm,textvariable=telefon)
                telefonEntry.place(x=70,y=110)
                guncelleBtn=tk.Button(telGuncelleForm,text="Guncelle",command=guncelle)
                guncelleBtn.place(x=200,y=105)
            else:
                hata=messagebox.showerror("Hata","Girdiginiz sifre yanlis lutfen tekrar deneyiniz")
        telGuncelleForm=tk.Tk()
        telGuncelleForm.title("Telefon Guncelle")
        telGuncelleForm.geometry("500x300")

        sifre=tk.StringVar()

        sifreLabel = tk.Label(telGuncelleForm, text="Sifre:").place(x=10, y=10)
        sifreEntry = tk.Entry(telGuncelleForm, textvariable=sifre,show="*").place(x=100, y=10)

        gonder=tk.Button(telGuncelleForm,text="Kontrol",command=gonder).place(x=175,y=35)
        telGuncelleForm.mainloop()
    def sifreGuncelle(self):
        self.aktivasyonMail(self.isim[0], self.eposta[0])
        if self.aktivasyon(self.isim[0],self.eposta[0]):
            pass
        else:
            def gonder():
                if len(sifre.get()) < 6:
                    hata = messagebox.showerror("Hata", "Sifre en az 6 karakter icermelidir")
                if sifre.get() != sifre2.get():
                    hata = messagebox.showerror("Hata", "Sifreler birbiriyle eslesmiyor")
                if sifre.get() == sifre2.get():
                    SHA256Sifre = hashlib.sha256(sifre.get().encode("ascii")).hexdigest()
                    self.con.execute(
                        f"UPDATE kullanicilar SET Sifre='{SHA256Sifre}' where KullaniciAdi='{self.kullaniciAdi}'")
                    self.con.commit()
                    info = messagebox.showinfo("Bilgi", "Sifre basariyla guncellendi")
                    sifreGuncelleForm.destroy()
            sifreGuncelleForm=tk.Tk()
            sifreGuncelleForm.title("Sifre Guncelle")
            sifreGuncelleForm.geometry("500x300")

            sifre=tk.StringVar()
            sifre2=tk.StringVar()

            sifreLabel=tk.Label(sifreGuncelleForm,text="Sifre").place(x=10,y=10)
            sifreEntry=tk.Entry(sifreGuncelleForm,textvariable=sifre,show="*").place(x=100,y=10)
            sifreKontrol=tk.Label(sifreGuncelleForm,text="Sifre Kontrol").place(x=10,y=35)
            sifreKontrolEntry=tk.Entry(sifreGuncelleForm,textvariable=sifre2,show="*").place(x=100,y=35)
            gonder=tk.Button(sifreGuncelleForm,text="Degistir",command=gonder).place(x=100,y=60)

            sifreGuncelleForm.mainloop()
    def ikiFaktorluDogrulamaAcma(self):
        def soruGir():
            SoruGirLabel.place(x=210, y=65)
            soruGirEntry.place(x=290, y=65)
        def gonder():
            if x.get()==1:
                text = "Ilk Evcil Hayvaniniz Adi"
            elif x.get()==2:
                text = "Ilkokul ogretmeninizin adi"
            elif x.get() == 3:
                text = "En Sevdiginiz Hayvan"
            elif x.get() == 4:
                text = "En yakin arkadasinizin adi"
            elif x.get() == 5:
                text = "En Sevdiginiz Film"
            elif x.get() == 6:
                text = "En Sevdiginiz Renk"
            else:
                text=soru.get()
            soru1=list(self.con.execute(f"select IFDKaldirmaSoru1 from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
            soru1=soru1[0]
            if soru1[0]==" ":
                uyari=messagebox.askyesno("Uyari",f"Girdiginiz Soru: {text}\nVerdiginiz Cevap: {cevap.get()}\nOnayliyor Musunuz?")
                if uyari==True:
                    self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru1 ='{text}' where KullaniciAdi='{self.kullaniciAdi}'")
                    self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru1Cevap ='{cevap.get()}' where KullaniciAdi='{self.kullaniciAdi}'")
                    self.con.commit()
                    if x.get() == 1:
                        menusecim1.destroy()
                    elif x.get() == 2:
                        menusecim2.destroy()
                    elif x.get() == 3:
                        menusecim3.destroy()
                    elif x.get() == 4:
                        menusecim4.destroy()
                    elif x.get() == 5:
                        menusecim5.destroy()
                    elif x.get() == 6:
                        menusecim6.destroy()
            else:
                if soru1[0]==text:
                    uyari=messagebox.showerror("Hata","Girdiğiniz soru ilk soruyla aynı olamaz")
                else:
                    uyari=messagebox.askyesno("Uyari",f"Girdiginiz Soru: {text}\nVerdiginiz Cevap: {cevap.get()}\nOnayliyor Musunuz?")
                    if uyari==True:
                        self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru2 ='{text}' where KullaniciAdi='{self.kullaniciAdi}'")
                        self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru2Cevap ='{cevap.get()}' where KullaniciAdi='{self.kullaniciAdi}'")
                        self.con.execute(f"UPDATE kullanicilar set IkiFaktorluDogrulama =True where KullaniciAdi='{self.kullaniciAdi}'")
                        self.con.commit()
                        bilgi=messagebox.showinfo("İki Faktorlu Dogrulama","İki Faktörlü Doğrulama açılmıştır")
                        ikiFaktorluDogrulamaAcmaForm.destroy()
        def soruGirSil():
            SoruGirLabel.place(x=-210, y=-65)
            soruGirEntry.place(x=-290, y=-65)
        ikiFaktorluDogrulamaAcmaForm = tk.Tk()
        ikiFaktorluDogrulamaAcmaForm.title("Hesap Bilgileri")
        ikiFaktorluDogrulamaAcmaForm.geometry("500x300")

        bilgiNotu=tk.Label(ikiFaktorluDogrulamaAcmaForm,text="İki Faktorlu Dogrulamayı açmak için 2 tane soru cevaplayınız,\n İki Faktörlü Doğrulamayı kapatmak isterseniz cevapladığınız   \n sorularının cevabını kullanarak kapatacaksınız                            ",width=45).place(x=10,y=10)

        x = tk.IntVar()
        soru=tk.StringVar()
        cevap=tk.StringVar()


        SoruGirLabel=tk.Label(ikiFaktorluDogrulamaAcmaForm,text="Soru Giriniz:")
        soruGirEntry=tk.Entry(ikiFaktorluDogrulamaAcmaForm,textvariable=soru,width=30)

        cevapLabel=tk.Label(ikiFaktorluDogrulamaAcmaForm,text="Cevap: ").place(x=210,y=90)
        cevapEntry=tk.Entry(ikiFaktorluDogrulamaAcmaForm,textvariable=cevap,width=30).place(x=290,y=90)

        menusecim1 = tk.Radiobutton(ikiFaktorluDogrulamaAcmaForm, text='İlk Evcil Hayvanınız Adı', variable=x, value=1, command=soruGirSil)
        menusecim1.place(x=10, y=60)
        menusecim2 = tk.Radiobutton(ikiFaktorluDogrulamaAcmaForm, text='İlkokul öğretmeninizin adı', variable=x, value=2, command=soruGirSil)
        menusecim2.place(x=10, y=85)
        menusecim3 = tk.Radiobutton(ikiFaktorluDogrulamaAcmaForm, text='En Sevdiğiniz Hayvan', variable=x, value=3, command=soruGirSil)
        menusecim3.place(x=10, y=110)
        menusecim4 = tk.Radiobutton(ikiFaktorluDogrulamaAcmaForm, text='En yakın arkadaşınızın adı', variable=x, value=4, command=soruGirSil)
        menusecim4.place(x=10, y=135)
        menusecim5 = tk.Radiobutton(ikiFaktorluDogrulamaAcmaForm, text='En Sevdiğiniz Film', variable=x, value=5, command=soruGirSil)
        menusecim5.place(x=10, y=160)
        menusecim6 = tk.Radiobutton(ikiFaktorluDogrulamaAcmaForm, text='En Sevdiğiniz Renk', variable=x, value=6, command=soruGirSil)
        menusecim6.place(x=10, y=185)
        menusecim7 = tk.Radiobutton(ikiFaktorluDogrulamaAcmaForm, text='Soruyu Ben Girmek İstiyorum', variable=x, value=7,command=soruGir)
        menusecim7.place(x=10, y=210)
        gonder=tk.Button(ikiFaktorluDogrulamaAcmaForm,text="Gonder",command=gonder).place(x=425,y=115)
        ikiFaktorluDogrulamaAcmaForm.mainloop()
    def ikiFaktorluDogrulamaKapama(self):
        def gonder():
            if cevap1.get()==cevaplar[0] and cevap2.get()==cevaplar[1]:
                self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru1 =' ' where KullaniciAdi='{self.kullaniciAdi}'")
                self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru1Cevap =' ' where KullaniciAdi='{self.kullaniciAdi}'")
                self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru2 =' ' where KullaniciAdi='{self.kullaniciAdi}'")
                self.con.execute(f"UPDATE kullanicilar set IFDKaldirmaSoru2Cevap =' ' where KullaniciAdi='{self.kullaniciAdi}'")
                self.con.execute(f"UPDATE kullanicilar set IkiFaktorluDogrulama =False where KullaniciAdi='{self.kullaniciAdi}'")
                self.con.commit()
                ikiFaktorluDogrulamaKapamaForm.destroy()
            else:
                hata=messagebox.showerror("Hata","Cevap / cevaplar yanlis lutfen tekrar deneyiniz")
        ikiFaktorluDogrulamaKapamaForm=tk.Tk()
        ikiFaktorluDogrulamaKapamaForm.title("İki Faktörlü Doğrulama Kapama")
        ikiFaktorluDogrulamaKapamaForm.geometry("500x300")

        cevap1=tk.StringVar()
        cevap2=tk.StringVar()

        sorular=list(self.con.execute(f"select IFDKaldirmaSoru1,IFDKaldirmaSoru2 from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
        sorular=sorular[0]
        cevaplar=list(self.con.execute(f"select IFDKaldirmaSoru1Cevap,IFDKaldirmaSoru2Cevap from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
        cevaplar = cevaplar[0]

        soru1Label=tk.Label(ikiFaktorluDogrulamaKapamaForm,text=sorular[0],width=68,height=5).place(x=10,y=10)
        cevap1Label=tk.Label(ikiFaktorluDogrulamaKapamaForm,text="1.Sorunun cevabı: ").place(x=10,y=105)
        cevap1Entry=tk.Entry(ikiFaktorluDogrulamaKapamaForm,textvariable=cevap1,width=60).place(x=120,y=105)

        soru2Label = tk.Label(ikiFaktorluDogrulamaKapamaForm, text=sorular[1], width=68,height=5).place(x=10, y=140)
        cevap2Label = tk.Label(ikiFaktorluDogrulamaKapamaForm, text="2.Sorunun cevabı: ").place(x=10, y=230)
        cevap2Entry = tk.Entry(ikiFaktorluDogrulamaKapamaForm, textvariable=cevap2, width=60).place(x=120, y=230)

        gonder=tk.Button(ikiFaktorluDogrulamaKapamaForm,text="Gonder",command=gonder).place(x=435,y=260)

        ikiFaktorluDogrulamaKapamaForm.mainloop()
    def program(self):
        def kontrol():
            menuForm.destroy()
            if x.get() == 1:
                def kontrol():
                    filmIzleForm.destroy()
                    if filmIzleMenuSecim.get()==1:
                        self.filmArat()
                    if filmIzleMenuSecim.get()==2:
                        self.randomFilm()
                    if filmIzleMenuSecim.get()==3:
                        self.butunFilmleriGoster()
                    if filmIzleMenuSecim.get()==4:
                        self.yapimYili()
                    if filmIzleMenuSecim.get()==5:
                        self.yapimci()
                    if filmIzleMenuSecim.get()==6:
                        self.kategoriSec()
                    if filmIzleMenuSecim.get()==7:
                        self.izlemeListesiniGoster()
                    if filmIzleMenuSecim.get()==8:
                        self.enCokBegenilenFilmler()
                filmIzleForm = tk.Tk()
                filmIzleForm.title("Burak Film")
                filmIzleForm.geometry("500x300")

                filmIzleMenuSecim = tk.IntVar()

                menusecim1 = tk.Radiobutton(filmIzleForm, text='Film Ara', variable=filmIzleMenuSecim, value=1, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=10)
                menusecim2 = tk.Radiobutton(filmIzleForm, text='Random Film', variable=filmIzleMenuSecim, value=2, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=35)
                menusecim3 = tk.Radiobutton(filmIzleForm, text='Butun Filmleri Getir', variable=filmIzleMenuSecim, value=3, command=kontrol, bg="light blue",indicator=0, width=20).place(x=10, y=60)
                menusecim4 = tk.Radiobutton(filmIzleForm, text='Yapim Yili Gir/Sec', variable=filmIzleMenuSecim, value=4, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=85)
                menusecim5 = tk.Radiobutton(filmIzleForm, text='Yapimci Gir/Sec', variable=filmIzleMenuSecim, value=5, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=110)
                menusecim6 = tk.Radiobutton(filmIzleForm, text='Kategori Sec', variable=filmIzleMenuSecim, value=6, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=135)
                menusecim7 = tk.Radiobutton(filmIzleForm, text='İzleme Listem', variable=filmIzleMenuSecim,value=7, command=kontrol, bg="light blue", indicator=0, width=20).place(x=10, y=160)
                menusecim7 = tk.Radiobutton(filmIzleForm, text='En Cok Begenilen Filmler', variable=filmIzleMenuSecim, value=8, command=kontrol, bg="light blue", indicator=0, width=20).place(x=10, y=185)

                filmIzleForm.mainloop()
            if x.get() == 2:
                def kontrol():
                    hesapBilgileriForm.destroy()
                    if hesapBilgileriSecim.get() == 1:
                        self.epostaGuncelle()
                    if hesapBilgileriSecim.get() == 2:
                        self.telGuncelle()
                    if hesapBilgileriSecim.get() == 3:
                        self.sifreGuncelle()
                def otoIzleme():
                    otoizleme = list(self.con.execute(f"select OtoIzlemeListesi from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
                    otoizleme = otoizleme[0]
                    if otoizleme[0] == "0":
                        self.con.execute(f"UPDATE kullanicilar set OtoIzlemeListesi =True where KullaniciAdi='{self.kullaniciAdi}'")
                        otoIzlemeSecim.config(bg="green", text="Aktif")
                    else:
                        self.con.execute(f"UPDATE kullanicilar set OtoIzlemeListesi =False where KullaniciAdi='{self.kullaniciAdi}'")
                        otoIzlemeSecim.config(bg="red", text="Pasif")
                    self.con.commit()
                def ikiFaktorluDogrulama():
                    ikiFaktDogrulama = list(self.con.execute(f"select IkiFaktorluDogrulama from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
                    ikiFaktDogrulama = ikiFaktDogrulama[0]
                    if ikiFaktDogrulama[0] == "0":
                        hesapBilgileriForm.destroy()
                        self.ikiFaktorluDogrulamaAcma()

                        self.con.execute(f"UPDATE kullanicilar set IkiFaktorluDogrulama =True where KullaniciAdi='{self.kullaniciAdi}'")
                    else:
                        hesapBilgileriForm.destroy()
                        self.ikiFaktorluDogrulamaKapama()
                        self.con.execute(f"UPDATE kullanicilar set IkiFaktorluDogrulama =False where KullaniciAdi='{self.kullaniciAdi}'")
                    self.con.commit()
                hesapBilgileriForm = tk.Tk()
                hesapBilgileriForm.title("Hesap Bilgileri")
                hesapBilgileriForm.geometry("500x300")

                renk=list(self.con.execute(f"select OtoIzlemeListesi from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
                renk=renk[0]
                ikiFaktorluDogrulamaRenk= list(self.con.execute(f"select IkiFaktorluDogrulama from kullanicilar where KullaniciAdi='{self.kullaniciAdi}'"))
                ikiFaktorluDogrulamaRenk = ikiFaktorluDogrulamaRenk[0]
                hesapBilgileriSecim = tk.IntVar()

                menusecim1 = tk.Radiobutton(hesapBilgileriForm, text='E-Posta Adresi Güncelle', variable=hesapBilgileriSecim, value=1,command=kontrol, bg="light blue", indicator=0, width=20).place(x=10, y=10)
                menusecim2 = tk.Radiobutton(hesapBilgileriForm, text='Telefon Numarasi Güncelle', variable=hesapBilgileriSecim, value=2,command=kontrol, bg="light blue", indicator=0, width=20).place(x=10, y=35)
                menusecim3 = tk.Radiobutton(hesapBilgileriForm, text='Sifre Degistir', variable=hesapBilgileriSecim,value=3, command=kontrol, bg="light blue", indicator=0, width=20).place(x=10, y=60)

                otoIzlemeListesi=tk.Label(hesapBilgileriForm,text="İzleme listenizde olan filmleri izlediğinizde\notomatik olarak listeden silme").place(x=170,y=10)
                otoIzlemeSecim = tk.Button(hesapBilgileriForm, command=otoIzleme, width=8,heigh=2)
                if renk[0]=="0":
                    otoIzlemeSecim.config(bg="red",text="Pasif")
                else:
                    otoIzlemeSecim.config(bg="green", text="Aktif")
                otoIzlemeSecim.place(x=400, y=10)
                ikiFaktorluDogrulamaLabel = tk.Label(hesapBilgileriForm,text="İki faktörlü kimlik doğrulaması\nGiriş yaparken mail onayını açar").place(x=170, y=60)
                ikiFaktorluDogrulamaBtn=tk.Button(hesapBilgileriForm,command=ikiFaktorluDogrulama, width=8,heigh=2)
                if ikiFaktorluDogrulamaRenk[0]=="0":
                    ikiFaktorluDogrulamaBtn.config(bg="red",text="Pasif")
                else:
                    ikiFaktorluDogrulamaBtn.config(bg="green", text="Aktif")
                ikiFaktorluDogrulamaBtn.place(x=400, y=60)

                hesapBilgileriForm.mainloop()
            if x.get() == 3:
                def gonder():
                    mesaj="Kullanici Adi: "+kullanciAdi.get()+"\n\n"+mesajEntry.get(1.0, tk.END+"-1c")
                    kullanici = ""
                    sifre = ""
                    context = ssl.create_default_context()
                    port = 465
                    host = 'smtp.gmail.com'
                    posta = MIMEMultipart()
                    posta['From'] = kullanici
                    posta['To'] = kullanici
                    posta['Subject'] = konu.get()
                    posta.attach(MIMEText(mesaj, 'plain'))
                    eposta_sunucu = smtplib.SMTP_SSL(host=host, port=port, context=context)
                    eposta_sunucu.login(kullanici, sifre)
                    eposta_sunucu.sendmail(kullanici, kullanici, str(posta))
                    info=messagebox.showinfo("Posta","E-posta basariyla gonderildi")
                destekForm = tk.Tk()
                destekForm.title("Mail Gonderme")
                destekForm.geometry("500x300")

                konu=tk.StringVar()
                kullanciAdi=tk.StringVar()

                kullanciAdiLabel = tk.Label(destekForm, text="Kullanici Adiniz:").place(x=10, y=10)
                kullanciAdiEntry = tk.Entry(destekForm, textvariable=kullanciAdi, width=30).place(x=110, y=10)

                konuLabel=tk.Label(destekForm,text="konu:").place(x=10,y=35)
                konuEntry=tk.Entry(destekForm,textvariable=konu,width=30).place(x=110,y=35)

                mesajLabel = tk.Label(destekForm, text="Mesaj").place(x=10, y=60)
                mesajEntry = tk.Text(destekForm, width=60,height=10)
                mesajEntry.place(x=8, y=85)

                gonderBtn=tk.Button(destekForm,text="Gonder",command=gonder).place(x=440,y=265)
                destekForm.mainloop()
            if x.get() == 5:
                self.durum=False
        menuForm = tk.Tk()
        menuForm.title("Admin Panel")
        menuForm.geometry("500x300")
        x = tk.IntVar()
        menusecim1 = tk.Radiobutton(menuForm, text='Film İzle', variable=x, value=1, command=kontrol, bg="light blue", indicator=0, width=20).place(x=10, y=10)
        menusecim2 = tk.Radiobutton(menuForm, text='Hesap Bilgileri', variable=x, value=2, command=kontrol, bg="light blue",indicator=0, width=20).place(x=10, y=35)
        menusecim3 = tk.Radiobutton(menuForm, text='Destek', variable=x, value=3, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=60)
        menusecim4 = tk.Radiobutton(menuForm, text='İletisim-Oneri', variable=x, value=3, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=85)
        menusecim5 = tk.Radiobutton(menuForm, text='Cikis', variable=x, value=5, command=kontrol, bg="light blue",indicator=0, width=20).place(x=10, y=110)
        menuForm.mainloop()
kullanicipanel=kullanicipanel()
while kullanicipanel.durum:
    kullanicipanel.program()
