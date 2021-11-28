import sqlite3,random,ssl,smtplib,hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter as tk
from tkinter import messagebox
class login():
    def __init__(self):
        self.durum=True
        self.con=sqlite3.connect("film.db")
        self.yasakliKarakterler = ["!", "'", "#", "^", "+", "$", "%", "&", "/", "{", "(", "[", ")", "]", "=", "}", "?","*", "-", "|", "_", '"', "'", "<", ">"]
        self.sifreYasakliKarakter=["ı","İ","ö","Ö","ü","Ü","ş","Ş"]
        self.telKontrol=["0","1","2","3","4","5","6","7","8","9"]
    def karakterKontrol(self, kontrolEdilecekKelime):
        for harf in kontrolEdilecekKelime:
            if harf in self.yasakliKarakterler:
                return True
    def kullanicAdiKontrol(self,kullaniciAdi):
        sistemdekiKullaniiciAdlari=list(self.con.execute("select KullaniciAdi from kullanicilar"))
        for i in sistemdekiKullaniiciAdlari:
            if kullaniciAdi==i[0]:
                return True
    def isimKontrol(self,isim):
        for i in isim:
            if i[0] in self.telKontrol:
                return True
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
    def sifreKarakterKontrol(self,sifre):
        for i in sifre:
            if i[0] in self.sifreYasakliKarakter:
                return True
    def telefonKontrol(self,tel):
        for i in tel:
            if i[0] not in self.telKontrol:
                return True
    def kullaniciKayit(self):
        def kayitKontrol():
            hataListesi = []
            if kullaniciAdi.get()=="":
                hataListesi.append('Kullanici Adi bos birakilamaz')
            if self.karakterKontrol(kullaniciAdi.get()):
                hataListesi.append(f"Kullanici Adi bu karakterleri iceremez {self.yasakliKarakterler}")
            if self.kullanicAdiKontrol(kullaniciAdi.get()):
                hataListesi.append("Bu kullanici Adi daha onceden alinmis")
            if len(sifre.get())<6:
                hataListesi.append("Sifre en az 6 karakterden olusmalidir")
            if self.sifreKarakterKontrol(sifre.get()):
                hataListesi.append(f"Sifrede bu karakterleri kullanamazsiniz {self.sifreYasakliKarakter}")
            if isim.get()=="":
                hataListesi.append("isim bos birakilamaz")
            if self.karakterKontrol(isim.get()):
                hataListesi.append(f"isim bu karakterleri iceremez {self.yasakliKarakterler}")
            if soyadi.get()=="":
                hataListesi.append("soyadi bos birakilamaz")
            if self.karakterKontrol(soyadi.get()):
                hataListesi.append(f"soyadi bu karakterleri iceremez {self.yasakliKarakterler}")
            if eposta.get()=="":
                hataListesi.append("eposta bos birakilamaz")
            if len(tel.get())!=11:
                hataListesi.append("telefon 11 haneli olmak zorundadir!")
            if self.telefonKontrol(tel.get()):
                 hataListesi.append(f"Telefon sadece bu karakterleri içerebilir {self.telKontrol}")
            dogumGunu = gun.get(), ay.get(), yil.get()
            if len(hataListesi)==0:
                kullaniciKayitForm.destroy()
                self.aktivasyonMail(isim.get(), eposta.get())
                self.aktivasyon(isim.get(), eposta.get())
                SHA256Sifre = hashlib.sha256(sifre.get().encode("ascii")).hexdigest()
                self.con.execute("insert into kullanicilar (KullaniciAdi,Sifre,Isim,Soyadi,EPosta,Telefon,DogumTarihi) values (?,?,?,?,?,?,?)",(kullaniciAdi.get(), SHA256Sifre, isim.get().lower().title(), soyadi.get().lower().title(), eposta.get(), tel.get(), str(dogumGunu)))
                self.con.commit()
            if len(hataListesi)!=0:
                hatalar = messagebox.showerror("Uyarı", str(hataListesi).split("}")[0].split("{")[0])
        kullaniciKayitForm=tk.Tk()
        kullaniciKayitForm.geometry("500x300")
        kullaniciKayitForm.title('Kullanıcı Kayıt')

        kullaniciAdi = tk.StringVar()
        sifre = tk.StringVar()
        isim = tk.StringVar()
        soyadi = tk.StringVar()
        eposta = tk.StringVar()
        tel = tk.StringVar()
        gun=tk.IntVar()
        ay = tk.IntVar()
        yil = tk.IntVar()

        kullaniciAdiLabel=tk.Label(text='Kullanıcı Adı:').place(x=10,y=10)
        kullaniciAdiEntry=tk.Entry(kullaniciKayitForm,textvariable=kullaniciAdi).place(x=100,y=10)

        sifreLabel=tk.Label(text='Sifre:').place(x=10,y=35)
        sifreEntry = tk.Entry(kullaniciKayitForm, textvariable=sifre,show='*').place(x=100, y=35)

        isimLabel = tk.Label(text='İsim:').place(x=10, y=60)
        isimEntry = tk.Entry(kullaniciKayitForm, textvariable=isim).place(x=100, y=60)

        soyadiLabel = tk.Label(text='Soyadi:').place(x=10, y=85)
        soyadiEntry = tk.Entry(kullaniciKayitForm, textvariable=soyadi).place(x=100, y=85)

        epostaLabel = tk.Label(text='e-posta:').place(x=10, y=110)
        epostaEntry = tk.Entry(kullaniciKayitForm, textvariable=eposta).place(x=100, y=110)

        telLabel = tk.Label(text='telefon:').place(x=10, y=135)
        telEntry = tk.Entry(kullaniciKayitForm, textvariable=tel).place(x=100, y=135)

        dogumGunu = tk.Label(text='Dogum Gününüzü Giriniz').place(x=10, y=160)
        dogumGun = tk.Label(text='Gun').place(x=10, y=180)
        dogumGunSpinBox = tk.Spinbox(kullaniciKayitForm,from_=1,to=31,width=2,textvariable=gun).place(x=40,y=182)
        dogumAy = tk.Label(text='Ay').place(x=70, y=180)
        dogumAySpinBox = tk.Spinbox(kullaniciKayitForm, from_=1, to=12, width=2,textvariable=ay).place(x=90, y=182)
        dogumYil = tk.Label(text='Yıl').place(x=120, y=180)
        dogumYilSpinBox = tk.Spinbox(kullaniciKayitForm, from_=1900, to=2021, width=4,textvariable=yil).place(x=140, y=182)

        gonder=tk.Button(kullaniciKayitForm,text="Kayıt ol",command=kayitKontrol).place(x=175,y=210)
        kullaniciKayitForm.mainloop()
    def kullaniciGirisKontrol(self,giris):
        veriTabaniKullanicilari = list(self.con.execute("select KullaniciAdi,Sifre from kullanicilar"))
        for i in veriTabaniKullanicilari:
            if giris[0] == i[0] and giris[1] == i[1]:
                ikiFaktorluDogrulama=list(self.con.execute(f"select IkiFaktorluDogrulama from kullanicilar where KullaniciAdi='{giris[0]}'"))
                ikiFaktorluDogrulama=ikiFaktorluDogrulama[0]
                if ikiFaktorluDogrulama[0]=="1":
                    eposta=list(self.con.execute(f"select EPosta from kullanicilar where KullaniciAdi='{giris[0]}'"))
                    eposta=eposta[0]
                    self.kullaniciGirisform.destroy()
                    self.aktivasyonMail("",eposta[0])
                    self.aktivasyon("",eposta[0])
                    with open("kullaniciAdi.txt", "w") as f:
                        f.write(giris[0])
                    import kullanicipanel
                    self.program()
                else:
                    self.kullaniciGirisform.destroy()
                    with open("kullaniciAdi.txt","w") as f:
                        f.write(giris[0])
                    import kullanicipanel
                    self.program()
        return True
    def kullaniciGiris(self):
        self.kullaniciGirisform=tk.Tk()
        self.kullaniciGirisform.geometry('500x300')
        self.kullaniciGirisform.title('Kullanici Giris')

        entry1=tk.StringVar()
        entry2=tk.StringVar()

        kullaniciAdi=tk.Label(self.kullaniciGirisform,text='Kullanıcı Adı:').place(x=10,y=10)
        kullaniciadiEntry=tk.Entry(self.kullaniciGirisform,textvariable=entry1).place(x=100,y=10)

        sifre=tk.Label(self.kullaniciGirisform,text='Sifre').place(x=10,y=40)
        sifreEntry = tk.Entry(self.kullaniciGirisform,textvariable=entry2,show='*').place(x=100, y=40)
        def goster():
            def kayitMenusuneDon():
                self.kullaniciGirisform.destroy()
                self.kullaniciKayit()
                self.program()
            def menuyeDon():
                self.kullaniciGirisform.destroy()
                self.program()
            def sifremiUnuttumBtn():
                self.kullaniciGirisform.destroy()
                self.sifremiUnuttum()
            SHA256Sifre = hashlib.sha256(entry2.get().encode("ascii")).hexdigest()
            giris = [entry1.get(), SHA256Sifre]
            if self.kullaniciGirisKontrol(giris):
                kayitolBtn = tk.Button(self.kullaniciGirisform, text='Kayıt ol',command=kayitMenusuneDon).place(x=130, y=70)
                menuyeDonBtn = tk.Button(self.kullaniciGirisform, text='Menuye Don', command=menuyeDon).place(x=145, y=105)
                sifremiUnuttumBtn=tk.Button(self.kullaniciGirisform, text='Sifremi Unuttum', command=sifremiUnuttumBtn).place(x=20, y=70)
        girisBtn=tk.Button(self.kullaniciGirisform,text='Giris',command=goster).place(x=190,y=70)
        self.kullaniciGirisform.mainloop()
    def sifremiUnuttum(self):
        def gonder():
            self.hatasayisi=0
            def gonder():
                if sifre.get()!=sifreKontrol.get():
                    hata=messagebox.showerror("Uyarı","Sifrelerin aynı olması lazım")
                    self.hatasayisi+=1
                if len(sifre.get())<6:

                    hata=messagebox.showerror("Uyarı","Sifre en az 6 karakterden olusmalidir")
                    self.hatasayisi += 1
                if self.sifreKarakterKontrol(sifre.get()):
                    hata=messagebox.showerror("Uyarı", f"Sifrede bu karakterleri kullanamazsiniz {self.sifreYasakliKarakter}")
                    self.hatasayisi += 1
                if self.hatasayisi==0:
                    SHA256Sifre = hashlib.sha256(sifre.get().encode("ascii")).hexdigest()
                    self.con.execute(f"Update kullanicilar SET Sifre='{SHA256Sifre}' where KullaniciAdi='{kullaniciAdi.get()}'")
                    self.con.commit()
                    sifreYenilemeForm.destroy()
            eposta = list(self.con.execute(f"select EPosta from kullanicilar where KullaniciAdi= '{kullaniciAdi.get()}'"))
            eposta = eposta[0]
            hatalar = messagebox.showinfo("Uyarı",f"Sistemimizde kayıtlı '{eposta[0]}' adresine bir onay kodu gelecektir onay kodunu girip sifrenizi sıfırlayabilirsiniz")
            sifremiUnuttumForm.destroy()
            self.aktivasyonMail("", eposta[0])
            self.aktivasyon("", eposta[0])
            sifreYenilemeForm=tk.Tk()
            sifreYenilemeForm.title("Sifre Yenileme Ekranı")
            sifreYenilemeForm.geometry("500x300")

            sifre=tk.StringVar()
            sifreKontrol=tk.StringVar()

            sifreLabel = tk.Label(sifreYenilemeForm, text="Yeni Sifre:").place(x=10, y=10)
            sifreEntry = tk.Entry(sifreYenilemeForm, textvariable=sifre,show="*").place(x=80, y=10)

            sifreKontrolLabel = tk.Label(sifreYenilemeForm, text="Yeni Sifre:").place(x=10, y=35)
            sifreKontrolEntry = tk.Entry(sifreYenilemeForm, textvariable=sifreKontrol,show="*").place(x=80, y=35)

            sifreBtn=tk.Button(sifreYenilemeForm,text="Gonder",command=gonder).place(x=150,y=60)

        sifremiUnuttumForm=tk.Tk()
        sifremiUnuttumForm.title("Sifremi Unuttum")
        sifremiUnuttumForm.geometry("500x300")

        kullaniciAdi=tk.StringVar()

        mesaj=tk.Label(sifremiUnuttumForm,text="Kullanici adınızı girip sistemde kayıtlı olan epostanız sayesinde hesabınızı kurtarabilirsiniz").place(x=10,y=10)
        kullaniciAdiLabel=tk.Label(sifremiUnuttumForm,text="Kullanici Adi").place(x=10,y=35)
        kullaniciAdiEntry=tk.Entry(sifremiUnuttumForm,textvariable=kullaniciAdi).place(x=90,y=35)

        gonder=tk.Button(sifremiUnuttumForm,text="Gonder",command=gonder).place(x=165,y=60)



        sifremiUnuttumForm.mainloop()
    def adminKontrol(self,giris):
        adminBilgileri=list(self.con.execute("select KullaniciAdi,Sifre from kullanicilar where KullaniciAdi='admin'"))
        adminBilgileri=list(adminBilgileri[0])
        if giris[0] == adminBilgileri[0] and giris[1] == adminBilgileri[1]:
            self.adminGirisform.destroy()
            import adminpanel
            self.program()
        return True
    def adminGiris(self):
        self.adminGirisform = tk.Tk()
        self.adminGirisform.geometry('500x300')
        self.adminGirisform.title('Kullanici Giris')

        entry1 = tk.StringVar()
        entry2 = tk.StringVar()

        adminKullaniciAdi = tk.Label(self.adminGirisform, text='Kullanıcı Adı:').place(x=10, y=10)
        admimKullaniciadiEntry = tk.Entry(self.adminGirisform, textvariable=entry1).place(x=100, y=10)

        sifre = tk.Label(self.adminGirisform, text='Sifre:').place(x=10, y=40)
        sifreEntry = tk.Entry(self.adminGirisform, textvariable=entry2, show='*').place(x=100, y=40)

        def goster():
            def kayitMenusuneDon():
                self.adminGirisform.destroy()
                self.kullaniciKayit()
                self.program()

            def menuyeDon():
                self.adminGirisform.destroy()
                self.program()

            def sifremiUnuttumBtn():
                self.adminGirisform.destroy()
                self.sifremiUnuttum()

            SHA256Sifre = hashlib.sha256(entry2.get().encode("ascii")).hexdigest()
            giris = [entry1.get(), SHA256Sifre]
            if self.adminKontrol(giris):
                kayitolBtn = tk.Button(self.adminGirisform, text='Kayıt ol', command=kayitMenusuneDon).place(x=130,
                                                                                                                 y=70)
                menuyeDonBtn = tk.Button(self.adminGirisform, text='Menuye Don', command=menuyeDon).place(x=145,
                                                                                                              y=105)
                sifremiUnuttumBtn = tk.Button(self.adminGirisform, text='Sifremi Unuttum',command=sifremiUnuttumBtn).place(x=20, y=70)

        girisBtn = tk.Button(self.adminGirisform, text='Giris', command=goster).place(x=190, y=70)
        self.adminGirisform.mainloop()
    def program(self):
        menuForm = tk.Tk()
        menuForm.geometry('500x300')
        menuForm.title('Burak Ekiz Film')
        def kontrol():
            menuForm.destroy()
            if x.get()==1:
                self.kullaniciGiris()
            if x.get()==2:
                self.adminGiris()
            if x.get()==3:
                self.kullaniciKayit()
            if x.get()==4:
                self.sifremiUnuttum()
            if x.get()==5:
                self.durum=False
        x=tk.IntVar()
        menusecim1 = tk.Radiobutton(menuForm, text='Kullanici Girisi', variable=x, value=1,command=kontrol,bg="light blue",indicator=0,width=20).place(x=10,y=10)
        menusecim2 = tk.Radiobutton(menuForm, text='Admin Girisi', variable=x, value=2,command=kontrol, bg="light blue",indicator=0,width=20).place(x=10,y=35)
        menusecim3 = tk.Radiobutton(menuForm, text='Kullanici Kayıt', variable=x, value=3,command=kontrol, bg="light blue",indicator=0,width=20).place(x=10,y=60)
        menusecim4 = tk.Radiobutton(menuForm, text='Sifremi Unuttum', variable=x, value=4,command=kontrol, bg="light blue",indicator=0,width=20).place(x=10,y=85)
        menusecim5 = tk.Radiobutton(menuForm, text='Cikis', variable=x, value=5,command=kontrol, bg="light blue",indicator=0,width=20).place(x=10,y=110)
        label=tk.Label(menuForm)
        label.pack()
        menuForm.mainloop()
login=login()
while login.durum:
    login.program()