import sqlite3,csv,os,ssl,smtplib,shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
import tkinter as tk
from tkinter import messagebox
from functools import partial

class film:
    def __init__(self):
        self.con = sqlite3.connect("film.db")
        self.durum=True
        self.yasakliKarakterler=["!","'","#","^","+","$","%","&","/","{","(","[",")","]","=","}","?","*","-","|","_",'"',"'","<",">","."]
        self.sayilar=["0","1","2","3","4","5","6","7","8","9"]
        self.filmler = list(self.con.execute("select * from film"))
        self.filmsayisi = len(self.filmler)
        time = date.today()
        if time.strftime("%a") == "Sun":
            #veritabanını local olarak kaydetme
            dosyaismi = f"Film veritabanı {time} yedegi"
            original = r'C:\Users\2000005332\PycharmProjects\Film\film.db'
            target = fr'C:\Users\2000005332\PycharmProjects\Film\yedekler\{dosyaismi}.db'
            shutil.copyfile(original, target)
    
            #veritabanının yedeğini mail olarak atma
            kullanici = ""
            sifre = ""
            alici = ""
            context = ssl.create_default_context()
            port = 465
            host = 'smtp.gmail.com'
            posta = MIMEMultipart()
            posta['From'] = kullanici
            posta['To'] = alici
            posta['Subject'] = "Haftalık veritabanı yedeği"
            mesaj = "Merhabalar,\n\nbu mesaj yedek alınmak amacıyla atılmıştır yedeğe ihtiyacınız yoksa bu maili görmezden gelebilirsiniz.\n\nİyi Günler"
            posta.attach(MIMEText(mesaj, 'plain'))
            eklenti_dosya_ismi = "film.db"
            with (open(eklenti_dosya_ismi, 'rb')) as eklenti_dosyasi:
                payload = MIMEBase('application', 'octate-stream')
                payload.set_payload((eklenti_dosyasi).read())
                encoders.encode_base64(payload)
                payload.add_header("Content-Disposition", "attachment", filename=eklenti_dosya_ismi)
                posta.attach(payload)
                posta_str = posta.as_string()
            eposta_sunucu = smtplib.SMTP_SSL(host=host, port=port, context=context)
            eposta_sunucu.login(kullanici, sifre)
            eposta_sunucu.sendmail(kullanici, alici, posta_str)
    def yapimciKontrol(self,yapimci):
        for harf in yapimci:
            if harf in self.yasakliKarakterler:
                return True
    def yapimciSayiKontrol(self,yapimci):
        for harf in yapimci:
            if harf in self.sayilar:
                return True
    def kayitKontrol(self,filmAdi):
        filmadi=self.con.execute("select FilmAd from film")
        filmadi=list(filmadi)
        for i in filmadi:
            if i[0]==filmAdi.lower().title():
                return True
    def veriKontrol(self,filmAdi):
        filmadi = self.con.execute("select FilmAd from film")
        filmadi = list(filmadi)
        for i in filmadi:
            if i[0] == filmAdi.lower().title():
                return False
        return True
    def veriGir(self):
        def verileriKaydet():
            hatalistesi=[]
            if self.filmAd.get()=="":
                hatalistesi.append(" Film adi bos girilemez")
            if self.kayitKontrol(self.filmAd.get()):
                hatalistesi.append("Bu film daha önceden kaydedilmiş!!!")
            if self.yapimci.get()=="":
                hatalistesi.append("Yapimci bos girilemez")
            if self.yapimciKontrol(self.yapimci.get()):
                hatalistesi.append(f"Yapimci bu karakterleri içeremez {self.yasakliKarakterler}")
            if self.yapimciSayiKontrol(self.yapimci.get()):
                hatalistesi.append("Yapimci adina sadece harf girebilirsiniz")
            kategoriler= checkvar1.get(), checkvar2.get(), checkvar3.get(), checkvar4.get(), checkvar5.get(), checkvar6.get(), checkvar7.get(), checkvar8.get(), checkvar9.get(), checkvar10.get(), checkvar11.get(), checkvar12.get(), checkvar13.get(), checkvar14.get(), checkvar15.get(), checkvar16.get(), checkvar17.get(), checkvar18.get(), checkvar19.get(), checkvar20.get(), checkvar21.get(), checkvar22.get()
            kategoriler=list(kategoriler)
            kategori=[]
            for i in kategoriler:
                if i!=0:
                    kategori.append(i)
            kategori=str(kategori).split("[")[1].split("]")[0]
            if len(kategori)==0:
                hatalistesi.append("en az 1 kategori secilmelidir")
            if len(hatalistesi)==0:
                self.con.execute("insert into film (FilmAd,YapimYili,Yapimci,Izlenme,Kategori,BegenmeSayisi,BegenmemeSayisi) values (?,?,?,0,?,0,0)",(self.filmAd.get().lower().title(), self.yapimYili.get(), self.yapimci.get().lower().title(), kategori))
                self.con.commit()
                self.filmAd.set("")
                self.yapimYili.set(1800)
                self.yapimci.set("")
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
            else:
                hata=messagebox.showerror("hata",str(hatalistesi).split("[")[1].split("{")[0].split("]")[0].replace(",","\n").replace("'",""))
            yenifilmler = list(self.con.execute("select FilmAd from film"))
            if self.filmsayisi + 15 == len(yenifilmler):
                self.filmsayisi += 15
                epostalar = list(self.con.execute("select EPosta from kullanicilar"))
                for i in epostalar:
                    kullanici = ""
                    sifre = ""
                    alici = i
                    mesaj = f"Merhabalar,\n\nYeni eklenen filmleri izlemek isteyebilecegini dusunduk. Bir goz atmaya ne dersin?\n{str(yenifilmler[-15:]).replace('(', '').replace(')', '').replace(',', '').replace('[', '').replace(']', '')}"
                    context = ssl.create_default_context()
                    port = 465
                    host = 'smtp.gmail.com'
                    eposta_sunucu = smtplib.SMTP_SSL(host=host, port=port, context=context)
                    eposta_sunucu.login(kullanici, sifre)
                    eposta_sunucu.sendmail(kullanici, alici, mesaj)
        veriGirForm=tk.Tk()
        veriGirForm.title("Veri Girme Ekrani")
        veriGirForm.geometry("500x300")

        self.filmAd = tk.StringVar()
        self.yapimYili = tk.StringVar()
        self.yapimci = tk.StringVar()

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

        filmAdLabel = tk.Label(text='Film Adı:').place(x=10, y=10)
        filmAdEntry = tk.Entry(veriGirForm, textvariable=self.filmAd).place(x=100, y=10)

        yapimYiliLabel = tk.Label(text='Yapım Yılı:').place(x=10, y=35)
        yapimYiliSpinBox = tk.Spinbox(veriGirForm,from_=1800,to=2021,width=4,textvariable=self.yapimYili).place(x=100,y=35)

        yapimciLabel = tk.Label(text='Yapımcı:').place(x=10, y=60)
        yapimciEntry = tk.Entry(veriGirForm, textvariable=self.yapimci).place(x=100, y=60)

        c1 = tk.Checkbutton(veriGirForm,text="Aile",variable=checkvar1, onvalue = 10).place(x=10,y=90)
        c2 = tk.Checkbutton(veriGirForm, text="Aksiyon", variable=checkvar2, onvalue = 11).place(x=85,y=90)
        c3 = tk.Checkbutton(veriGirForm, text="Animasyon", variable=checkvar3, onvalue = 12).place(x=165,y=90)
        c4 = tk.Checkbutton(veriGirForm, text="Anime", variable=checkvar4, onvalue = 13).place(x=250,y=90)
        c5 = tk.Checkbutton(veriGirForm, text="Aşk", variable=checkvar5, onvalue = 14).place(x=10,y=115)
        c6 = tk.Checkbutton(veriGirForm, text="Bağımsız", variable=checkvar6, onvalue = 15).place(x=85,y=115)
        c7 = tk.Checkbutton(veriGirForm, text="Belgesel", variable=checkvar7, onvalue = 16).place(x=165,y=115)
        c8 = tk.Checkbutton(veriGirForm, text="Bilim Kurgu", variable=checkvar8, onvalue = 17).place(x=250,y=115)
        c9 = tk.Checkbutton(veriGirForm, text="Doğaüstü", variable=checkvar9, onvalue = 18).place(x=10, y=140)
        c10 = tk.Checkbutton(veriGirForm, text="Drama", variable=checkvar10, onvalue = 19).place(x=85, y=140)
        c11 = tk.Checkbutton(veriGirForm, text="Epik", variable=checkvar11, onvalue = 20).place(x=165, y=140)
        c12 = tk.Checkbutton(veriGirForm, text="Fantazi", variable=checkvar12, onvalue = 21).place(x=250, y=140)
        c13 = tk.Checkbutton(veriGirForm, text="Gerilim", variable=checkvar13, onvalue = 22).place(x=10, y=165)
        c14 = tk.Checkbutton(veriGirForm, text="Gizem", variable=checkvar14, onvalue = 23).place(x=85, y=165)
        c15 = tk.Checkbutton(veriGirForm, text="Komedi", variable=checkvar15, onvalue = 24).place(x=165, y=165)
        c16 = tk.Checkbutton(veriGirForm, text="Korku", variable=checkvar16, onvalue = 25).place(x=250, y=165)
        c17 = tk.Checkbutton(veriGirForm, text="Mecara", variable=checkvar17, onvalue = 26).place(x=10, y=190)
        c18 = tk.Checkbutton(veriGirForm, text="Muzikal", variable=checkvar18, onvalue = 27).place(x=85, y=190)
        c19 = tk.Checkbutton(veriGirForm, text="Spor", variable=checkvar19, onvalue = 28).place(x=165, y=190)
        c20 = tk.Checkbutton(veriGirForm, text="Suç", variable=checkvar20, onvalue = 29).place(x=250, y=190)
        c21 = tk.Checkbutton(veriGirForm, text="Western", variable=checkvar21, onvalue = 30).place(x=10, y=215)
        c22 = tk.Checkbutton(veriGirForm, text="Çizgi Film", variable=checkvar22, onvalue = 31).place(x=85, y=215)

        gonder = tk.Button(veriGirForm, text="Veriyi Kaydet",command=verileriKaydet).place(x=250, y=250)

        veriGirForm.mainloop()
    def arat(self,listbox,film,arananveri):
        listbox.delete(0,tk.END)
        listbox.pack(pady=75)
        if film.get() == "":
            hata = messagebox.showerror("Hata", "Bu alan bos girilemez")
        yeniFilmListesi = []

        filmler = list(self.con.execute(f"select {arananveri} from film"))
        for i in filmler:
            if i[0] not in yeniFilmListesi and film.get().lower().title() in i[0]:
                yeniFilmListesi.append(i[0])
        for i in yeniFilmListesi:
            gosterilecekFilm = list(self.con.execute(f"select * from film where {arananveri}='{i}'"))
            gosterilecekFilm = gosterilecekFilm[0]
            listbox.insert(tk.END, f"Film Adı: {gosterilecekFilm[0]}")
            listbox.insert(tk.END, f"Yapım Yılı: {gosterilecekFilm[1]}")
            listbox.insert(tk.END, f"Yapımcı: {gosterilecekFilm[2]}")
            listbox.insert(tk.END, f"İzlenme: {gosterilecekFilm[3]}")
            listbox.insert(tk.END, f"Kategori: {gosterilecekFilm[4]}")
            listbox.insert(tk.END, f"Begenme Sayısı: {gosterilecekFilm[5]}")
            listbox.insert(tk.END, f"Begenmeme Sayisi: {gosterilecekFilm[6]}")
            listbox.insert(tk.END, "")
    def intArat(self,listbox,baslangicyapimyili,bitisyapimyili,arananveri):
        listbox.delete(0, tk.END)
        listbox.pack(pady=75)
        yeniFilmListesi = []
        for i in range(baslangicyapimyili.get(), bitisyapimyili.get()):
            filmler = list(self.con.execute(f"select * from film where {arananveri}={i}"))
            if len(filmler) != 0:
                yeniFilmListesi.append(filmler)
        for i in yeniFilmListesi:
            gosterilecekFilm = i[0]
            listbox.insert(tk.END, f"Film Adı: {gosterilecekFilm[0]}")
            listbox.insert(tk.END, f"Yapım Yılı: {gosterilecekFilm[1]}")
            listbox.insert(tk.END, f"Yapımcı: {gosterilecekFilm[2]}")
            listbox.insert(tk.END, f"İzlenme: {gosterilecekFilm[3]}")
            listbox.insert(tk.END, f"Kategori: {gosterilecekFilm[4]}")
            listbox.insert(tk.END, f"Begenme Sayısı: {gosterilecekFilm[5]}")
            listbox.insert(tk.END, f"Begenmeme Sayisi: {gosterilecekFilm[6]}")
            listbox.insert(tk.END, "")
    def veriAratma(self):
        def kontrol():
            veriAratmaForm.destroy()
            if x.get() == 1:
                veriAratmaFormSecim1=tk.Tk()
                veriAratmaFormSecim1.title("Film Adina Gore Arat")
                veriAratmaFormSecim1.geometry("500x300")

                film = tk.StringVar()

                filmAdiLabel=tk.Label(veriAratmaFormSecim1,text="Film Adi:").place(x=10,y=10)
                filmAdiEntry=tk.Entry(veriAratmaFormSecim1,textvariable=film).place(x=70,y=10)
                listbox = tk.Listbox(veriAratmaFormSecim1, selectmode=tk.SINGLE, font=18,width=500)


                arat = tk.Button(veriAratmaFormSecim1, text="Film Ara", command=partial(self.arat,listbox,film,"FilmAd")).place(x=140,y=35)

                #filmIzle=tk.Button(veriAratmaFormSecim1,text="Film izle",font=28,command=izle).place(x=420,y=240)
                veriAratmaFormSecim1.mainloop()
            if x.get()==2:
                veriAratmaFormSecim2=tk.Tk()
                veriAratmaFormSecim2.title("Yapım yılına gore arat")
                veriAratmaFormSecim2.geometry("500x300")

                baslangicyapimyili=tk.IntVar()
                bitisyapimyili=tk.IntVar()

                yapimyiliLabel=tk.Label(veriAratmaFormSecim2,text="Baslangıc Yapım Yılı").place(x=10,y=10)
                yapimyiliSpinBox=tk.Spinbox(veriAratmaFormSecim2, from_=1900, to=2021, width=4,textvariable=baslangicyapimyili).place(x=125,y=11)

                yapimyiliLabel = tk.Label(veriAratmaFormSecim2, text="Bitis Yapım Yılı").place(x=10, y=35)
                yapimyiliSpinBox = tk.Spinbox(veriAratmaFormSecim2, from_=1900, to=2021, width=4,textvariable=bitisyapimyili).place(x=125, y=36)

                listbox = tk.Listbox(veriAratmaFormSecim2, selectmode=tk.SINGLE, font=18, width=500)

                arat = tk.Button(veriAratmaFormSecim2, text="Film Ara",width=10,height=2,command=partial(self.intArat,listbox,baslangicyapimyili,bitisyapimyili,"YapimYili")).place(x=175, y=10)

                veriAratmaFormSecim2.mainloop()
            if x.get()==3:
                veriAratmaFormSecim3 = tk.Tk()
                veriAratmaFormSecim3.title("Yapımcıya Gore Arat")
                veriAratmaFormSecim3.geometry("500x300")

                yapimci = tk.StringVar()

                yapimciLabel = tk.Label(veriAratmaFormSecim3, text="Yapimci:").place(x=10, y=10)
                yapimciEntry = tk.Entry(veriAratmaFormSecim3, textvariable=yapimci).place(x=70, y=10)
                listbox = tk.Listbox(veriAratmaFormSecim3, selectmode=tk.SINGLE, font=18, width=500)
                arat = tk.Button(veriAratmaFormSecim3, text="Film Ara",command=partial(self.arat, listbox, yapimci, "Yapimci")).place(x=140, y=35)
                veriAratmaFormSecim3.mainloop()
            if x.get()==4:
                veriAratmaFormSecim4 = tk.Tk()
                veriAratmaFormSecim4.title("Izlenmeye gore arat")
                veriAratmaFormSecim4.geometry("500x300")

                baslangicIzlenme = tk.IntVar()
                bitisIzlenme = tk.IntVar()

                yapimyiliLabel = tk.Label(veriAratmaFormSecim4, text="Baslangıc Izlenme").place(x=10, y=10)
                yapimyiliSpinBox = tk.Spinbox(veriAratmaFormSecim4, from_=1900, to=2021, width=4,textvariable=baslangicIzlenme).place(x=125, y=11)

                yapimyiliLabel = tk.Label(veriAratmaFormSecim4, text="Bitis Izlenme").place(x=10, y=35)
                yapimyiliSpinBox = tk.Spinbox(veriAratmaFormSecim4, from_=1900, to=2021, width=4,textvariable=bitisIzlenme).place(x=125, y=36)

                listbox = tk.Listbox(veriAratmaFormSecim4, selectmode=tk.SINGLE, font=18, width=500)

                arat = tk.Button(veriAratmaFormSecim4, text="Film Ara", width=10, height=2,command=partial(self.intArat, listbox, baslangicIzlenme, bitisIzlenme,"Izlenme")).place(x=175, y=10)

                veriAratmaFormSecim4.mainloop()
            if x.get()==5:
                def arat():
                    listbox.delete(0, tk.END)
                    listbox.place(x=0,y=110,height=150)
                    kategoriler = checkvar1.get(), checkvar2.get(), checkvar3.get(), checkvar4.get(), checkvar5.get(), checkvar6.get(), checkvar7.get(), checkvar8.get(), checkvar9.get(), checkvar10.get(), checkvar11.get(), checkvar12.get(), checkvar13.get(), checkvar14.get(), checkvar15.get(), checkvar16.get(), checkvar17.get(), checkvar18.get(), checkvar19.get(), checkvar20.get(), checkvar21.get(), checkvar22.get()
                    kategoriler = list(kategoriler)
                    kategori = []
                    yeniFilmListesi=[]
                    for i in kategoriler:
                        if i != 0:
                            kategori.append(i)
                    kategori = str(kategori).split("[")[1].split("]")[0]
                    if len(kategori) == 0:
                       hata=messagebox.showerror("Hata","en az 1 kategori secilmelidir")
                    else:
                        filmler=list(self.con.execute("select * from film"))
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

                veriAratmaFormSecim5 = tk.Tk()
                veriAratmaFormSecim5.title("Kategoriye gore arat")
                veriAratmaFormSecim5.geometry("500x300")

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

                c1 = tk.Checkbutton(veriAratmaFormSecim5, text="Aile", variable=checkvar1, onvalue=10).place(x=10, y=10)
                c2 = tk.Checkbutton(veriAratmaFormSecim5, text="Aksiyon", variable=checkvar2, onvalue=11).place(x=85, y=10)
                c3 = tk.Checkbutton(veriAratmaFormSecim5, text="Animasyon", variable=checkvar3, onvalue=12).place(x=175, y=10)
                c4 = tk.Checkbutton(veriAratmaFormSecim5, text="Anime", variable=checkvar4, onvalue=13).place(x=260, y=10)
                c5 = tk.Checkbutton(veriAratmaFormSecim5, text="Aşk", variable=checkvar5, onvalue=14).place(x=340, y=10)
                c6 = tk.Checkbutton(veriAratmaFormSecim5, text="Bağımsız", variable=checkvar6, onvalue=15).place(x=410, y=10)
                c7 = tk.Checkbutton(veriAratmaFormSecim5, text="Belgesel", variable=checkvar7, onvalue=16).place(x=10, y=35)
                c8 = tk.Checkbutton(veriAratmaFormSecim5, text="Bilim Kurgu", variable=checkvar8, onvalue=17).place(x=85, y=35)
                c9 = tk.Checkbutton(veriAratmaFormSecim5, text="Doğaüstü", variable=checkvar9, onvalue=18).place(x=175, y=35)
                c10 = tk.Checkbutton(veriAratmaFormSecim5, text="Drama", variable=checkvar10, onvalue=19).place(x=260, y=35)
                c11 = tk.Checkbutton(veriAratmaFormSecim5, text="Epik", variable=checkvar11, onvalue=20).place(x=340, y=35)
                c12 = tk.Checkbutton(veriAratmaFormSecim5, text="Fantazi", variable=checkvar12, onvalue=21).place(x=410, y=35)
                c13 = tk.Checkbutton(veriAratmaFormSecim5, text="Gerilim", variable=checkvar13, onvalue=22).place(x=10, y=60)
                c14 = tk.Checkbutton(veriAratmaFormSecim5, text="Gizem", variable=checkvar14, onvalue=23).place(x=85, y=60)
                c15 = tk.Checkbutton(veriAratmaFormSecim5, text="Komedi", variable=checkvar15, onvalue=24).place(x=175, y=60)
                c16 = tk.Checkbutton(veriAratmaFormSecim5, text="Korku", variable=checkvar16, onvalue=25).place(x=260, y=60)
                c17 = tk.Checkbutton(veriAratmaFormSecim5, text="Mecara", variable=checkvar17, onvalue=26).place(x=340, y=60)
                c18 = tk.Checkbutton(veriAratmaFormSecim5, text="Muzikal", variable=checkvar18, onvalue=27).place(x=410, y=60)
                c19 = tk.Checkbutton(veriAratmaFormSecim5, text="Spor", variable=checkvar19, onvalue=28).place(x=10, y=85)
                c20 = tk.Checkbutton(veriAratmaFormSecim5, text="Suç", variable=checkvar20, onvalue=29).place(x=85, y=85)
                c21 = tk.Checkbutton(veriAratmaFormSecim5, text="Western", variable=checkvar21, onvalue=30).place(x=175, y=85)
                c22 = tk.Checkbutton(veriAratmaFormSecim5, text="Çizgi Film", variable=checkvar22, onvalue=31).place(x=260, y=85)
                listbox = tk.Listbox(veriAratmaFormSecim5, selectmode=tk.SINGLE, font=18, width=500)
                gonder = tk.Button(veriAratmaFormSecim5, text="Film Ara", command=arat).place(x=345, y=82)
        veriAratmaForm=tk.Tk()
        x = tk.IntVar()
        veriAratmaForm.title("Veri Aratma Menusu")
        veriAratmaForm.geometry("500x300")
        menusecim1 = tk.Radiobutton(veriAratmaForm, text='Film Adı', variable=x, value=1, command=kontrol, bg="light blue", indicator=0, width=20).place(x=10, y=10)
        menusecim2 = tk.Radiobutton(veriAratmaForm, text='Yapim yılı', variable=x, value=2, command=kontrol, bg="light blue",indicator=0, width=20).place(x=10, y=35)
        menusecim3 = tk.Radiobutton(veriAratmaForm, text='Yapimci', variable=x, value=3, command=kontrol, bg="light blue",indicator=0, width=20).place(x=10, y=60)
        menusecim4 = tk.Radiobutton(veriAratmaForm, text='Izlenme', variable=x, value=4, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=85)
        menusecim5 = tk.Radiobutton(veriAratmaForm, text='Kategori', variable=x, value=5, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=110)
        veriAratmaForm.mainloop()
    def veriGoruntule(self):
        def islem(event):
            def sil():
                self.con.execute(f"DELETE from film where FilmAd='{filmDegiskenVerisi.lower().title()}'")
            def degistir():
                if x.get()==1:
                    if self.kayitKontrol(yeniveri.get().lower().title()):
                        hata=messagebox.showerror("Hata","Bu Film Zaten Kayıtlı")
                    elif yeniveri.get().lower().title()=="":
                        hata = messagebox.showerror("Hata", "Film Adı Bos Girilemez")
                    else:
                        self.con.execute(f"UPDATE film SET FilmAd='{yeniveri.get().lower().title()}' where FilmAd='{filmDegiskenVerisi}'")
                    yeniveri.set("")
                if x.get()==2:
                    self.con.execute(f"UPDATE film SET YapimYili='{yapimYili.get()}' where FilmAd='{filmDegiskenVerisi}'")
                    yapimYili.set(1900)
                if x.get()==3:
                    if self.yapimciKontrol(yeniveri.get().lower().title()):
                        hata=messagebox.showerror("hata","Yapimci adina sadece harf girebilirsiniz")
                    elif yeniveri.get().lower().title()=="":
                        hata = messagebox.showerror("hata", "Yapimci Adı Bos Bıraklımaz")
                    elif self.yapimciSayiKontrol(yeniveri.get().lower().title()):
                        hata=messagebox.showerror("hata",f"Yapimci bu karakterleri içeremez {self.yasakliKarakterler}")
                    else:
                        self.con.execute(f"UPDATE film SET Yapimci='{yeniveri.get().lower().title()}' where FilmAd='{filmDegiskenVerisi}'")
                    yeniveri.set("")
                if x.get()==4:
                    kategoriler = checkvar1.get(), checkvar2.get(), checkvar3.get(), checkvar4.get(), checkvar5.get(), checkvar6.get(), checkvar7.get(), checkvar8.get(), checkvar9.get(), checkvar10.get(), checkvar11.get(), checkvar12.get(), checkvar13.get(), checkvar14.get(), checkvar15.get(), checkvar16.get(), checkvar17.get(), checkvar18.get(), checkvar19.get(), checkvar20.get(), checkvar21.get(), checkvar22.get()
                    kategoriler = list(kategoriler)
                    kategori = []
                    for i in kategoriler:
                        if i != 0:
                            kategori.append(i)
                    kategori = str(kategori).split("[")[1].split("]")[0]
                    self.con.execute(f"UPDATE film SET Kategori='{kategori}' where FilmAd='{filmDegiskenVerisi}'")
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
                self.con.commit()
            def menusecim1():
                c1.place(x=-130, y=-180)
                c2.place(x=-200, y=-180)
                c3.place(x=-270, y=-180)
                c4.place(x=-350, y=-180)
                c5.place(x=-420, y=-180)
                c6.place(x=-130, y=-205)
                c7.place(x=-200, y=-205)
                c8.place(x=-270, y=-205)
                c9.place(x=-350, y=-205)
                c10.place(x=-420, y=-205)
                c11.place(x=-130, y=-230)
                c12.place(x=-200, y=-230)
                c13.place(x=-270, y=-230)
                c14.place(x=-350, y=-230)
                c15.place(x=-420, y=-230)
                c16.place(x=-130, y=-255)
                c17.place(x=-200, y=-255)
                c18.place(x=-270, y=-255)
                c19.place(x=-350, y=-255)
                c20.place(x=-420, y=-255)
                c21.place(x=-130, y=-280)
                c22.place(x=-200, y=-280)
                yeniVeriEntry.place(x=140,y=190)
                yapimYiliSpinBox.place(x=-990, y=-990)
                degistir.place(x=270, y=186)
            def menusecim2():
                sil.place(x=-340, y=-186)
                c1.place(x=-130, y=-180)
                c2.place(x=-200, y=-180)
                c3.place(x=-270, y=-180)
                c4.place(x=-350, y=-180)
                c5.place(x=-420, y=-180)
                c6.place(x=-130, y=-205)
                c7.place(x=-200, y=-205)
                c8.place(x=-270, y=-205)
                c9.place(x=-350, y=-205)
                c10.place(x=-420, y=-205)
                c11.place(x=-130, y=-230)
                c12.place(x=-200, y=-230)
                c13.place(x=-270, y=-230)
                c14.place(x=-350, y=-230)
                c15.place(x=-420, y=-230)
                c16.place(x=-130, y=-255)
                c17.place(x=-200, y=-255)
                c18.place(x=-270, y=-255)
                c19.place(x=-350, y=-255)
                c20.place(x=-420, y=-255)
                c21.place(x=-130, y=-280)
                c22.place(x=-200, y=-280)
                yeniVeriEntry.place(x=-990, y=-990)
                yapimYiliSpinBox.place(x=140, y=192)
                degistir.place(x=200, y=186)
            def menusecim3():
                sil.place(x=-340, y=-186)
                c1.place(x=-130, y=-180)
                c2.place(x=-200, y=-180)
                c3.place(x=-270, y=-180)
                c4.place(x=-350, y=-180)
                c5.place(x=-420, y=-180)
                c6.place(x=-130, y=-205)
                c7.place(x=-200, y=-205)
                c8.place(x=-270, y=-205)
                c9.place(x=-350, y=-205)
                c10.place(x=-420, y=-205)
                c11.place(x=-130, y=-230)
                c12.place(x=-200, y=-230)
                c13.place(x=-270, y=-230)
                c14.place(x=-350, y=-230)
                c15.place(x=-420, y=-230)
                c16.place(x=-130, y=-255)
                c17.place(x=-200, y=-255)
                c18.place(x=-270, y=-255)
                c19.place(x=-350, y=-255)
                c20.place(x=-420, y=-255)
                c21.place(x=-130, y=-280)
                c22.place(x=-200, y=-280)
                yeniVeriEntry.place(x=140, y=190)
                yapimYiliSpinBox.place(x=-990, y=-990)
                degistir.place(x=270, y=186)
            def menusecim4():
                sil.place(x=-340, y=-186)
                yeniVeriEntry.place(x=-990, y=-990)
                yapimYiliSpinBox.place(x=-990, y=-990)
                degistir.place(x=420, y=276)
                c1.place(x=130,y=180)
                c2.place(x=200,y=180)
                c3.place(x=270,y=180)
                c4.place(x=350,y=180)
                c5.place(x=420,y=180)
                c6.place(x=130,y=205)
                c7.place(x=200,y=205)
                c8.place(x=270,y=205)
                c9.place(x=350,y=205)
                c10.place(x=420,y=205)
                c11.place(x=130,y=230)
                c12.place(x=200,y=230)
                c13.place(x=270,y=230)
                c14.place(x=350,y=230)
                c15.place(x=420,y=230)
                c16.place(x=130,y=255)
                c17.place(x=200,y=255)
                c18.place(x=270,y=255)
                c19.place(x=350,y=255)
                c20.place(x=420,y=255)
                c21.place(x=130,y=280)
                c22.place(x=200,y=280)
            x=tk.IntVar()
            yapimYili = tk.IntVar()
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
            yeniveri = tk.StringVar()

            menusecim1 = tk.Radiobutton(veriGoruntuleForm, text='Film Adı', variable=x, value=1,command= menusecim1,bg="light blue", indicator=0, width=15).place(x=10, y=190)
            menusecim2 = tk.Radiobutton(veriGoruntuleForm, text='Yapım Yılı', variable=x, value=2,command= menusecim2,bg="light blue", indicator=0, width=15).place(x=10, y=215)
            menusecim3 = tk.Radiobutton(veriGoruntuleForm, text='Yapımcı', variable=x, value=3,command= menusecim3, bg="light blue", indicator=0, width=15).place(x=10, y=240)
            menusecim4 = tk.Radiobutton(veriGoruntuleForm, text='Kategori', variable=x, value=4,command= menusecim4, bg="light blue", indicator=0, width=15).place(x=10, y=265)

            yeniVeriEntry = tk.Entry(veriGoruntuleForm, textvariable=yeniveri)
            yeniVeriEntry.place(x=140, y=190)
            degistir = tk.Button(veriGoruntuleForm, text="Degistir", command=degistir)
            degistir.place(x=270, y=186)

            yapimYiliSpinBox = tk.Spinbox(veriGoruntuleForm, from_=1800, to=2021, width=4, textvariable=yapimYili)

            sil=tk.Button(veriGoruntuleForm,text="Sil",command=sil,width=5)
            sil.place(x=340,y=186)

            filmDegiskenIsmi=str(mylistbox.get(mylistbox.curselection()).split(": ")[0])
            filmDegiskenVerisi=str(mylistbox.get(mylistbox.curselection()).split(": ")[1])

            if filmDegiskenIsmi!="Film Adı":
                messagebox.showerror("Hata","Sadece Film adı secilebilir")

            c1 = tk.Checkbutton(veriGoruntuleForm, text="Aile", variable=checkvar1, onvalue=10)
            c2 = tk.Checkbutton(veriGoruntuleForm, text="Aksiyon", variable=checkvar2, onvalue=11)
            c3 = tk.Checkbutton(veriGoruntuleForm, text="Animasyon", variable=checkvar3, onvalue=12)
            c4 = tk.Checkbutton(veriGoruntuleForm, text="Anime", variable=checkvar4, onvalue=13)
            c5 = tk.Checkbutton(veriGoruntuleForm, text="Aşk", variable=checkvar5, onvalue=14)
            c6 = tk.Checkbutton(veriGoruntuleForm, text="Bağımsız", variable=checkvar6, onvalue=15)
            c7 = tk.Checkbutton(veriGoruntuleForm, text="Belgesel", variable=checkvar7, onvalue=16)
            c8 = tk.Checkbutton(veriGoruntuleForm, text="Bilim Kurgu", variable=checkvar8, onvalue=17)
            c9 = tk.Checkbutton(veriGoruntuleForm, text="Doğaüstü", variable=checkvar9, onvalue=18)
            c10 = tk.Checkbutton(veriGoruntuleForm, text="Drama", variable=checkvar10, onvalue=19)
            c11 = tk.Checkbutton(veriGoruntuleForm, text="Epik", variable=checkvar11, onvalue=20)
            c12 = tk.Checkbutton(veriGoruntuleForm, text="Fantazi", variable=checkvar12, onvalue=21)
            c13 = tk.Checkbutton(veriGoruntuleForm, text="Gerilim", variable=checkvar13, onvalue=22)
            c14 = tk.Checkbutton(veriGoruntuleForm, text="Gizem", variable=checkvar14, onvalue=23)
            c15 = tk.Checkbutton(veriGoruntuleForm, text="Komedi", variable=checkvar15, onvalue=24)
            c16 = tk.Checkbutton(veriGoruntuleForm, text="Korku", variable=checkvar16, onvalue=25)
            c17 = tk.Checkbutton(veriGoruntuleForm, text="Mecara", variable=checkvar17, onvalue=26)
            c18 = tk.Checkbutton(veriGoruntuleForm, text="Muzikal", variable=checkvar18, onvalue=27)
            c19 = tk.Checkbutton(veriGoruntuleForm, text="Spor", variable=checkvar19, onvalue=28)
            c20 = tk.Checkbutton(veriGoruntuleForm, text="Suç", variable=checkvar20, onvalue=29)
            c21 = tk.Checkbutton(veriGoruntuleForm, text="Western", variable=checkvar21, onvalue=30)
            c22 = tk.Checkbutton(veriGoruntuleForm, text="Çizgi Film", variable=checkvar22, onvalue=31)

        def goruntule():
            mylistbox.delete(0, tk.END)
            mylistbox.place(x=0, y=28, height=150)
            filmler=[]
            if film.get()=="*":
                filmler = list(self.con.execute("select * from film "))
            elif film.get()=="":
                hata=messagebox.showerror("Hata","Film adı bos bırakılamaz butun vefileri goruntulemek istiyorsanız * girmeniz gerekmektedir.")
            else:
                filmler = list(self.con.execute(f"select * from film where FilmAd='{film.get().lower().title()}'"))
            for i in filmler:
                mylistbox.insert(tk.END, f"Film Adı: {i[0]}",f"Yapım Yılı: {i[1]}",f"Yapımcı: {i[2]}",f"İzlenme: {i[3]}",f"Kategori: {i[4]}",f"Begenme Sayısı: {i[5]}",f"Begenmeme Sayisi: {i[6]}","")
            mylistbox.bind('<Double-1>',islem)
        veriGoruntuleForm=tk.Tk()
        veriGoruntuleForm.title("Veri Goruntule")
        veriGoruntuleForm.geometry("500x300")

        film=tk.StringVar()

        filmLabel=tk.Label(veriGoruntuleForm,text="Film Adı:").place(x=10,y=4)
        filmEntry=tk.Entry(veriGoruntuleForm,textvariable=film).place(x=70,y=4)
        mylistbox = tk.Listbox(veriGoruntuleForm, selectmode=tk.SINGLE, font=18, width=500)

        gonder=tk.Button(veriGoruntuleForm,text="Gonder",command=goruntule).place(x=200,y=0)

        veriGoruntuleForm.mainloop()
    def dosyaAdiKontrol(self,dosyaAdi):
        with open("dosyaAdiTxt.txt", "r") as f:
            if dosyaAdi in f.read():
                return False
            else:
                with open("dosyaAdiTxt.txt","a+") as f:
                    f.write(dosyaAdi)
                    f.write("\n")
                return True
    def verileriDisaAktar(self):
        def disariAktar():
            uzanti=""
            if x.get()==1:
                uzanti=".txt"
            if x.get()==2:
                uzanti=".csv"
            if uzanti=="":
                hata=messagebox.showerror("Hata","Uzanti Secimi Zorunludur")
            if dosyaAdi.get()=="":
                hata = messagebox.showerror("Hata", "Dosya adi bos birakilamaz!!")
            data = list(self.con.execute("Select * from film"))
            dosyaKontrolIsmi = "dosyaAdiTxt"
            dosya=os.path.join("C:/Users/2000005332/PycharmProjects/Film/TxtveCsvDosyaları",dosyaAdi.get())
            if self.dosyaAdiKontrol(dosyaAdi.get())==False and uzanti!="" and dosyaAdi.get()!="":
                
                hata=messagebox.askyesno("Hata","Girdiginiz dosya adi zaten kayıtlı ustune yazmak ister misiniz?")
                if hata==True:
                    with open(f'{dosya}{uzanti}', 'w') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Film Adi', 'Yapim Yili', "Yapimci", "Izlenme", "Kategori"])
                        writer.writerows(data)
            else:
                with open(f'{dosya}{uzanti}', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Film Adi', 'Yapim Yili', "Yapimci", "Izlenme", "Kategori"])
                    writer.writerows(data)

        verileriDisariAktarForm=tk.Tk()
        verileriDisariAktarForm.title("Verileri Dısari Aktar")
        verileriDisariAktarForm.geometry("500x300")

        x = tk.IntVar()
        dosyaAdi=tk.StringVar()

        dosyaAdiLabel=tk.Label(verileriDisariAktarForm,text="Dosya Adi:").place(x=10,y=10)
        dosyaAdiEntry=tk.Entry(verileriDisariAktarForm,textvariable=dosyaAdi).place(x=80,y=10)

        menusecim1 = tk.Radiobutton(verileriDisariAktarForm, text='Txt', variable=x, value=1, bg="light blue",indicator=0, width=7).place(x=10, y=35)
        menusecim2 = tk.Radiobutton(verileriDisariAktarForm, text='Csv', variable=x, value=2, bg="light blue",indicator=0, width=7).place(x=10, y=60)

        disariAktar=tk.Button(verileriDisariAktarForm,text="Disari Aktar",height=3,width=16,command=disariAktar).place(x=80,y=35)

        verileriDisariAktarForm.mainloop()
    def klasorYonetimi(self):
        def islem(event):
            dosyaad=tk.Label(klasorYonetimForm,text="",width=20,fg="black",bg="red")
            dosyaad.config(text=listbox.selection_get())
            dosyaad.place(x=10,y=190)
            def sil():
                with open("dosyaAdiTxt.txt", "r") as dosya:
                    kontrol = dosya.readlines()
                with open("dosyaAdiTxt.txt","w") as dosya:
                    for i in kontrol:
                        if i.strip("\n") != dosyaAdi.split(".")[0]:
                            dosya.write(i)
                os.remove(os.path.join("C:/Users/2000005332/PycharmProjects/Film/TxtveCsvDosyaları",dosyaAdi))
                listbox.delete(tk.ANCHOR)
                data.remove(dosyaAdi)
                dosyaad.config(fg="green")

            def duzenle():
                if yeniDosyaAdi.get()=="":
                    hata=messagebox.showerror("Hata","Yeni dosya adi bos birakilamaz")
                uzanti=str(listbox.selection_get()).split(".")
                if self.dosyaAdiKontrol(yeniDosyaAdi.get()):
                    sil()
                    dosya = os.path.join("C:/Users/2000005332/PycharmProjects/Film/TxtveCsvDosyaları", yeniDosyaAdi.get())
                    with open(f'{dosya}.{uzanti[1]}', 'w') as f:
                        data = list(self.con.execute("Select * from film"))
                        writer = csv.writer(f)
                        writer.writerow(['Film Adi', 'Yapim Yili', "Yapimci", "Izlenme", "Kategori"])
                        writer.writerows(data)
                else:
                    hata=messagebox.showerror("hata","Bu dosya adı zaten sistemde mevcut")
            def goster():
                dosya = os.path.join("C:/Users/2000005332/PycharmProjects/Film/TxtveCsvDosyaları", listbox.selection_get())
                listbox.delete(0,tk.END)
                with open(dosya, "r") as f:
                    veriler = f.read()
                for i in veriler.split("\n"):
                    listbox.insert(tk.END, i)
            yeniDosyaAdi=tk.StringVar()
            dosyaAdi = str(listbox.get(listbox.curselection()))
            dosyaSil=tk.Button(klasorYonetimForm,text="Sil",width=5,command=sil).place(x=350,y=188)
            yeniDosyaAdiEntry=tk.Entry(klasorYonetimForm,textvariable=yeniDosyaAdi).place(x=160,y=191)
            duzenle=tk.Button(klasorYonetimForm,text="Duzenle",command=duzenle).place(x=290,y=188)
            goster=tk.Button(klasorYonetimForm,text="Goster",command=goster).place(x=400,y=188)
        def listele():
            listbox.delete(0, tk.END)
            listbox.place(x=0, y=35, height=150)

            for i in data:
                if c1.get()==1 and c2.get()==2:
                    listbox.insert(tk.END,i)
                elif c1.get()==1:
                    if i.split(".")[1]=="txt":
                        listbox.insert(tk.END, i)
                elif c2.get()==2:
                    if i.split(".")[1] == "csv":
                        listbox.insert(tk.END, i)
            listbox.bind('<Double-1>', islem)
        klasorYonetimForm=tk.Tk()
        klasorYonetimForm.title("Klasor Yonetimi")
        klasorYonetimForm.geometry("500x300")

        data = os.listdir("C:/Users/2000005332/PycharmProjects/Film/TxtveCsvDosyaları")

        x = tk.IntVar()
        c1=tk.IntVar()
        c2=tk.IntVar()

        checkButton1 = tk.Checkbutton(klasorYonetimForm,text="Txt",variable=c1, onvalue = 1).place(x=10,y=10)
        checkButton2 = tk.Checkbutton(klasorYonetimForm, text="Csv", variable=c2, onvalue =2).place(x=60, y=10)

        listbox = tk.Listbox(klasorYonetimForm, selectmode=tk.SINGLE, font=18, width=500)

        listele=tk.Button(klasorYonetimForm,text="Listele",command=listele).place(x=120,y=8)
        klasorYonetimForm.mainloop()
    def program(self):
        menuForm=tk.Tk()
        menuForm.title("Admin Panel")
        menuForm.geometry("500x300")
        def kontrol():
            menuForm.destroy()
            if x.get()==1:
                self.veriGir()
            if x.get()==2:
                self.veriAratma()
            if x.get()==3:
                self.veriGoruntule()
            if x.get()==4:
                self.verileriDisaAktar()
            if x.get()==5:
                self.klasorYonetimi()
            if x.get()==6:
                self.durum = False
        x = tk.IntVar()
        menusecim1 = tk.Radiobutton(menuForm, text='Veri Gir', variable=x, value=1, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=10)
        menusecim2 = tk.Radiobutton(menuForm, text='Veri Arat', variable=x, value=2, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=35)
        menusecim3 = tk.Radiobutton(menuForm, text='Verileri Görüntüle', variable=x, value=3, command=kontrol, bg="light blue",indicator=0, width=20).place(x=10, y=60)
        menusecim4 = tk.Radiobutton(menuForm, text='Verileri dışarı aktar', variable=x, value=4, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=85)
        menusecim5 = tk.Radiobutton(menuForm, text='Txt ve Csv dosyalarını yönet', variable=x, value=5, command=kontrol,bg="light blue", indicator=0, width=20).place(x=10, y=110)
        menusecim6 = tk.Radiobutton(menuForm, text='Cikis', variable=x, value=6, command=kontrol, bg="light blue",indicator=0, width=20).place(x=10, y=135)
        label = tk.Label(menuForm)
        label.pack()
        menuForm.mainloop()
film=film()
while film.durum:
    film.program()