import wx
import wx.adv
import csv
import pyodbc
import time
import functools
kullaniciAdi = 'a'
sifresi = 'b'
blrtcBLM = 'c'
secimAD = 'd'
akts_ogrenci = 1.00

class kulGiris(wx.Frame):
    def __init__(self,parent,title):
        super(kulGiris,self).__init__(parent,title=title,size=(280,155))
        self.Asikar()
        self.Centre()
        self.Show()

    def Asikar(self):
        yuzey = wx.Panel(self)
        diz = wx.GridBagSizer(0,0)

        yaziBicimi = wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.BOLD)

        kulAdYazi = wx.StaticText(yuzey,label='Kullanıcı Adınız : ')
        diz.Add(kulAdYazi,pos=(0,0),flag=wx.ALL,border=7)
        kulAdYazi.SetFont(yaziBicimi)
        self.kulAd = wx.TextCtrl(yuzey)
        diz.Add(self.kulAd,pos=(0,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)

        sifreYazi = wx.StaticText(yuzey,label='Şifreniz : ')
        diz.Add(sifreYazi,pos=(1,0),flag=wx.ALL,border=7)
        sifreYazi.SetFont(yaziBicimi)
        self.sifre = wx.TextCtrl(yuzey,style=wx.TE_PASSWORD)
        diz.Add(self.sifre,pos=(1,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)
        
        cikisDugme = wx.Button(yuzey,label='Çık')
        diz.Add(cikisDugme,pos=(2,0),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)
        cikisDugme.Bind(wx.EVT_BUTTON,self.cikis)

        girisDugme = wx.Button(yuzey,label='Gir')
        diz.Add(girisDugme,pos=(2,2),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)
        girisDugme.Bind(wx.EVT_BUTTON,self.girisDenetle)
        
        yuzey.SetSizerAndFit(diz)
    def cikis(self,event):
        self.Destroy()
    def girisDenetle(self,event):
        kAD = self.kulAd.GetValue()
        sfr = self.sifre.GetValue()
        if len(sfr)>11 or len(sfr)<4:
            wx.MessageBox('Şifre veya Kullanıcı adı yanlış','HATA',wx.OK|wx.ICON_INFORMATION)
        else:
            bilgiSQL = sqlIslem()
            cursor=bilgiSQL.baglan.cursor()
            cursor.execute(" exec udSP_ogrenciKullaniciArama ?,? ",(kAD,sfr))
            kayit = cursor.fetchall()
        
            global kullaniciAdi
            global sifresi
            if kayit[0][0] is True:
                kullaniciAdi = kAD
                sifresi = sfr
                self.ogrenciGiris()
            elif kayit[0][0] is False:
                cursor.execute(" exec udSP_yoneticiKullaniciArama ?,? ",(kAD,sfr))
                kayit2 = cursor.fetchall()
                if kayit2[0][0] is True:
                    self.yoneticiGiris()
                else:
                    cursor.execute(" execute udSP_ogretmenKullaniciArama ?,? ",(kAD,sfr))
                    kayit3 = cursor.fetchall()
                    if kayit3[0][0] is True:
                        kullaniciAdi = kAD
                        sifresi = sfr
                        #print (kullaniciAdi)
                        self.ogretmenGiris()
                    else:
                        self.girisBasarisiz()

        





        #if kAD in ['yonetici'] and sfr in ['1234']:
        #    self.yoneticiGiris()
        #elif kAD in ['ogrenci'] and sfr in ['1234']:
        #    self.ogrenciGiris()
        #elif kAD in ['ogretmen'] and sfr in ['1234']:
            #self.ogretmenGiris()
        
    def girisBasarisiz(self):
        wx.MessageBox('Hatalı giriş yaptınız.','HATA',wx.OK|wx.ICON_INFORMATION)
    def yoneticiGiris(self):
        yoneticiGirisi=girisYonetici(None,title='Yönetici')
        self.Destroy()
    def ogrenciGiris(self):
        ogrenciGirisi=girisOgrenci(None,title='Öğrenci')
        self.Destroy()
    def ogretmenGiris(self):
        ogretmenGirisi=girisOgretmen(None,title='Öğretmen')
        self.Destroy()

class girisOgretmen(wx.Frame):
    def __init__(self,parent,title):
        super(girisOgretmen,self).__init__(parent,title=title,size=(300,220))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        yuzey = wx.Panel(self)
        diz = wx.GridBagSizer(0,0)

        dersNotEkle = wx.Button(yuzey,label='Sınav Sonuçlarını Gir')
        diz.Add(dersNotEkle,pos=(0,0),flag=wx.EXPAND|wx.ALL,border=5)
        dersNotEkle.Bind(wx.EVT_BUTTON,self.notEKle)

        girilenDers = wx.Button(yuzey,label='Girdiğim dersleri göster')
        diz.Add(girilenDers,pos=(1,0),flag=wx.EXPAND|wx.ALL,border=5)

        ogretmenBilgi = wx.Button(yuzey,label='Bilgilerim')
        diz.Add(ogretmenBilgi,pos=(2,0),flag=wx.EXPAND|wx.ALL,border=5)
        ogretmenBilgi.Bind(wx.EVT_BUTTON,self.ogretmenBilgileriGetir)


        Cikis = wx.Button(yuzey,label='Çık')
        diz.Add(Cikis,pos=(4,0),flag=wx.EXPAND|wx.ALL,border=7)
        Cikis.Bind(wx.EVT_BUTTON,self.Cik)

        oturumCikis = wx.Button(yuzey,label='Oturumu Kapat')
        diz.Add(oturumCikis,pos=(4,2),flag=wx.EXPAND|wx.ALL,border=7)
        oturumCikis.Bind(wx.EVT_BUTTON,self.oturumCik)
        
        yuzey.SetSizerAndFit(diz)
    def Cik(self,event):
        self.Destroy()
    def oturumCik(self,event):
        kul_gir=kulGiris(None,title='Kullanıcı Girişi')
        self.Destroy()
    def ogretmenBilgileriGetir(self,event):
        ogrtmn_bilgi=ogretmenBilgileriGoster(None,title='Öğretmen Bilgileri')
    def notEKle(self,event):
        dersNot = dersNotuEkle(None,title='Sınav Sonuçlarını Ekleme')
class dersNotuEkle(wx.Frame):
    def __init__(self,parent,title):
        super(dersNotuEkle,self).__init__(parent,title=title,size=(600,150))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        self.yuzey = wx.Panel(self)
        self.dizilim = wx.GridBagSizer(0,0)

        
        drs = self.dersADI()
        drsBlrtcYazi = wx.StaticText(self.yuzey,label='Not girşi yapılacak olan ders : ')
        self.dizilim.Add(drsBlrtcYazi,pos=(0,0),flag=wx.ALL,border=5)
        self.drsBlrtc = wx.Choice(self.yuzey,choices=drs)
        self.dizilim.Add(self.drsBlrtc,pos=(0,1),span=(1,2),flag=wx.ALL,border=5)

        derseNotEkle = wx.Button(self.yuzey,label='Sonuçları Gir')
        self.dizilim.Add(derseNotEkle,pos=(0,4),flag=wx.EXPAND|wx.ALL,border=7)
        derseNotEkle.Bind(wx.EVT_BUTTON,self.dersiAlanOgrenciler)   
        
        self.yuzey.SetSizerAndFit(self.dizilim)
    def dersADI(self):
        a = 0
        b = 0
        sqlBaglanti= sqlIslem()
        cursor = sqlBaglanti.baglan.cursor()
        cursor.execute("select dersADI from derslerTB where dersBelirtec in (select dersBelirtec from verilenDerslerTB where verilenDerslerTB.ogretmenBelirtec = ?)",(kullaniciAdi))
        satir = cursor.fetchone()
        while satir:
            #print(b)
            b=b+1
            satir = cursor.fetchone()
        drs = ['']*b
        cursor.execute("select dersADI from derslerTB where dersBelirtec in (select dersBelirtec from verilenDerslerTB where verilenDerslerTB.ogretmenBelirtec = ?)",(kullaniciAdi))
        satir = cursor.fetchone()
        while satir:
            #print(drs[a])
            drs[a]=satir[0]
            a=a+1
            satir = cursor.fetchone()
        return drs
    def dersiAlanOgrenciler(self,event):
        global secimAD 
        secimAD = self.drsBlrtc.GetString(self.drsBlrtc.GetSelection())
        print(secimAD)
        notgrs=notGiris(None,title='Not Giriş Ekranı')
        self.Destroy()
class notGiris(wx.Frame):
    def __init__(self,parent,title):
        super(notGiris,self).__init__(parent,title=title,size=(800,350))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        self.yuzey = wx.Panel(self)
        self.ogrenciSiralama = wx.Panel(self.yuzey)
        self.dizilim = wx.GridBagSizer(0,0)
        self.sayac = 0

        Numara = wx.StaticText(self.yuzey,-1,label='Numarası')
        ad1 = wx.StaticText(self.yuzey,-1,label='Ad')
        #ad2 = wx.StaticText(self.yuzey,-1,label='2. Adı')
        #ad3 = wx.StaticText(self.yuzey,-1,label='3. Adı')
        soyad = wx.StaticText(self.yuzey,-1,label='Soyad')
        finalNotu = wx.StaticText(self.yuzey,-1,label='Final Notu')
        vizeNotu = wx.StaticText(self.yuzey,-1,label='Vize Notu')
        Odev = wx.StaticText(self.yuzey,-1,label='Ödev')

        #Numara.SetPosition((10,10))
        #ad1.SetPosition((90,10))
        #ad2.SetPosition((170,10))
        #ad3.SetPosition((250,10))
        #soyad.SetPosition((330,10))
        #finalNotu.SetPosition((410,10))
        #vizeNotu.SetPosition((520,10))
        #Odev.SetPosition((630,10))


        self.dizilim.Add(Numara,pos=(0,0),flag=wx.ALL,border=5)
        self.dizilim.Add(ad1,pos=(0,1),flag=wx.ALL,border=5)
        #self.dizilim.Add(ad2,pos=(0,2),flag=wx.ALL,border=5)
        #self.dizilim.Add(ad3,pos=(0,3),flag=wx.ALL,border=5)
        self.dizilim.Add(soyad,pos=(0,2),flag=wx.ALL,border=5)
        self.dizilim.Add(finalNotu,pos=(0,3),flag=wx.ALL,border=5)
        self.dizilim.Add(vizeNotu,pos=(0,4),flag=wx.ALL,border=5)
        self.dizilim.Add(Odev,pos=(0,5),flag=wx.ALL,border=5)


        sqlBaglan = sqlIslem()
        cursor=sqlBaglan.baglan.cursor()
        cursor.execute("exec udSP_notGirmeEkrani ?",(secimAD))
        satir = cursor.fetchone()
        while satir:
            print(satir)
            self.sayac = self.sayac + 1
            satir = cursor.fetchone()
        print(self.sayac)
        
        sqlBaglan = sqlIslem()
        cursor=sqlBaglan.baglan.cursor()
        cursor.execute("exec udSP_notGirmeEkrani ?",(secimAD))
        satir = cursor.fetchone()

        y=1
        aydi = 0
        while satir:
            z=0
            snc = wx.StaticText(self.yuzey,id=aydi,label=satir[0])
            #snc.SetPosition((10+y,z))
            self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
            aydi = aydi+1
            if satir[2] is not None:
                if satir[3] is not None:
                    z=z+1
                    snc = wx.StaticText(self.yuzey,-1,label=satir[1]+' '+satir[2]+' '+satir[3])
                    #snc.SetPosition((10+y,z))
                    self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
                else:
                    z=z+1
                    snc = wx.StaticText(self.yuzey,-1,label=satir[1]+' '+satir[2])
                    #snc.SetPosition((10+y,z))
                    self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
            else:
                z=z+1
                snc = wx.StaticText(self.yuzey,-1,label=satir[1])
                #snc.SetPosition((10+y,z))
                self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
            z=z+1
            snc = wx.StaticText(self.yuzey,-1,label=satir[4])
            #snc.SetPosition((10+y,z))
            self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
            if satir[5] is not None:
                z=z+1
                #snc = wx.StaticText(self.yuzey,-1,label=satir[5])
                #snc.SetPosition((30+y,z))
                self.final = wx.TextCtrl(self.yuzey,id=aydi)
                self.dizilim.Add(self.final,pos=(y,z),flag=wx.ALL,border=5)
                aydi=aydi+1
            else:
                z=z+1
                #snc = wx.StaticText(self.yuzey,-1,label='Girilmedi')
                #snc.SetPosition((30+y,z))
                self.final = wx.TextCtrl(self.yuzey,id=aydi)
                self.dizilim.Add(self.final,pos=(y,z),flag=wx.ALL,border=5)
                aydi=aydi+1
            if satir[6] is not None:
                z=z+1
                #snc = wx.StaticText(self.yuzey,-1,label=satir[6])
                #snc.SetPosition((50+y,z))
                self.vize = wx.TextCtrl(self.yuzey,id=aydi)
                self.dizilim.Add(self.vize,pos=(y,z),flag=wx.ALL,border=5)
                aydi=aydi+1
            else:
                z=z+1
                #snc = wx.StaticText(self.yuzey,-1,label='Girilmedi')
                #snc.SetPosition((50+y,z))
                self.vize = wx.TextCtrl(self.yuzey,id=aydi)
                self.dizilim.Add(self.vize,pos=(y,z),flag=wx.ALL,border=5)
                aydi=aydi+1
            if satir[7] is not None:
                z=z+1
                #snc = wx.StaticText(self.yuzey,-1,label=satir[7])
                #snc.SetPosition((70+y,z))
                self.odev = wx.TextCtrl(self.yuzey,id=aydi)
                self.dizilim.Add(self.odev,pos=(y,z),flag=wx.ALL,border=5)
                aydi=aydi+1
            else:
                z=z+1
                #snc = wx.StaticText(self.yuzey,-1,label='Girilmedi')
                #snc.SetPosition((70+y,z))
                self.odev = wx.TextCtrl(self.yuzey,id=aydi)
                self.dizilim.Add(self.odev,pos=(y,z),flag=wx.ALL,border=5)
                aydi=aydi+1
            satir = cursor.fetchone()
            y=y+1

        yayinla = wx.Button(self.yuzey,label='Sonuçları Yayınla')
        self.dizilim.Add(yayinla,pos=(y,6),flag=wx.ALL,border=5)
        yayinla.Bind(wx.EVT_BUTTON,self.sonucYayinla)

        self.syc = self.sayac
        self.sayac=0
        self.yuzey.SetSizerAndFit(self.dizilim)
    def cik(self,event):
        self.Destroy()
    def sonucYayinla(self,event):
        #print(self.syc)
        #asd = self.yuzey.FindWindowById(self.syc).GetValue()
        #print(asd)
        sncGosterSQL = sqlIslem()
        cursor = sncGosterSQL.baglan.cursor()
        for x in range(0,(self.syc*4)):
            if x%4==0:
                ogrNO = self.yuzey.FindWindowById(x).GetLabel()
                #print(ogrNO)
            elif x%4==1:
                final = self.yuzey.FindWindowById(x).GetValue()
                #print(final)
                if int(final)>100 or int(final)<0:
                    wx.MessageBox('Öğrenci numarası %s olan öğrencinin final notunu yanlış girdiniz' %(ogrNO),'HATA',wx.OK|wx.ICON_INFORMATION)
                    break
            elif x%4==2:
                vize = self.yuzey.FindWindowById(x).GetValue()
                #print (vize)
                if int(vize)>100 or int(vize)<0:
                    wx.MessageBox('Öğrenci numarası %s olan öğrencinin vize notunu yanlış girdiniz' %(ogrNO),'HATA',wx.OK|wx.ICON_INFORMATION)
                    break
            else:
                odev = self.yuzey.FindWindowById(x).GetValue()
                #print(odev)
                #print(secimAD)
                if int(odev)>100 or int(odev)<0:
                    wx.MessageBox('Öğrenci numarası %s olan öğrencinin ödev notunu yanlış girdiniz' %(ogrNO),'HATA',wx.OK|wx.ICON_INFORMATION)
                    break
                else:
                    try:
                        cursor.execute("exec udSP_notGirmeIslemi ?, ?, ?, ?, ?",(ogrNO,final,vize,odev,secimAD))
                        sncGosterSQL.baglan.commit()
                    except Exception as e:
                        sncGosterSQL.hata(e)
class ogretmenBilgileriGoster(wx.Frame):
    def __init__(self,parent,title):
        super(ogretmenBilgileriGoster,self).__init__(parent,title=title,size=(800,350))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        self.yuzey = wx.Panel(self)
        dizilim = wx.GridBagSizer(0,0)

        yaziBicimi = wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        yaziBicimi2 = wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        bilgiSQL = sqlIslem()
        cursor=bilgiSQL.baglan.cursor()
        try:
            cursor.execute(" execute udSP_ogretmenBilgiGoruntuleme ?,? ",(kullaniciAdi,sifresi))
            kayit = cursor.fetchall()
        except Exception as e:
            bilgiSQL.hata(e)
        for satir in kayit:
            #print("Öğrenci Belirtec = ",satir[4])
            ogrnciBlrtciYazi = wx.StaticText(self.yuzey,label='Öğretmen Belirteci : ')
            dizilim.Add(ogrnciBlrtciYazi,pos=(0,0),flag=wx.ALL,border=5)
            ogrnciBlrtciYazi.SetFont(yaziBicimi)
            ogrnciBlrtciYazi.SetForegroundColour((0, 153, 255))
            ogrnciBlrtci = wx.StaticText(self.yuzey,label=satir[0])
            dizilim.Add(ogrnciBlrtci,pos=(0,1),flag=wx.ALL,border=5)
            ogrnciBlrtci.SetFont(yaziBicimi2)

            ogrnciTcYazi = wx.StaticText(self.yuzey,label='TC Kimlik Numarası : ')
            dizilim.Add(ogrnciTcYazi,pos=(0,3),flag=wx.ALL,border=5)
            ogrnciTcYazi.SetFont(yaziBicimi)
            ogrnciTcYazi.SetForegroundColour((0, 153, 255))
            ogrnciTc = wx.StaticText(self.yuzey,label=satir[1])
            dizilim.Add(ogrnciTc,pos=(0,4),flag=wx.ALL,border=5)
            ogrnciTc.SetFont(yaziBicimi2)

            if satir[4] is None:
                if satir[3] is None:
                    ogrnciAdYazi = wx.StaticText(self.yuzey,label='Adı : ')
                    dizilim.Add(ogrnciAdYazi,pos=(1,0),flag=wx.ALL,border=5)
                    ogrnciAdYazi.SetFont(yaziBicimi)
                    ogrnciAdYazi.SetForegroundColour((0, 153, 255))
                    ogrnciAd = wx.StaticText(self.yuzey,label=satir[2])
                    dizilim.Add(ogrnciAd,pos=(1,1),flag=wx.ALL,border=5)
                    ogrnciAd.SetFont(yaziBicimi2)
                else:
                    ogrnciAdYazi = wx.StaticText(self.yuzey,label='Adı : ')
                    dizilim.Add(ogrnciAdYazi,pos=(1,0),flag=wx.ALL,border=5)
                    ogrnciAdYazi.SetFont(yaziBicimi)
                    ogrnciAdYazi.SetForegroundColour((0, 153, 255))
                    ogrnciAd = wx.StaticText(self.yuzey,label=satir[2]+' '+satir[3])
                    dizilim.Add(ogrnciAd,pos=(1,1),flag=wx.ALL,border=5)
                    ogrnciAd.SetFont(yaziBicimi2)
            else:
                ogrnciAdYazi = wx.StaticText(self.yuzey,label='Adı : ')
                dizilim.Add(ogrnciAdYazi,pos=(1,0),flag=wx.ALL,border=5)
                ogrnciAdYazi.SetFont(yaziBicimi)
                ogrnciAdYazi.SetForegroundColour((0, 153, 255))
                ogrnciAd = wx.StaticText(self.yuzey,label=satir[2]+' '+satir[3]+' '+satir[4])
                dizilim.Add(ogrnciAd,pos=(1,1),flag=wx.ALL,border=5)
                ogrnciAd.SetFont(yaziBicimi2)

            ogrnciSoyadYazi = wx.StaticText(self.yuzey,label='Soyadı : ')
            dizilim.Add(ogrnciSoyadYazi,pos=(1,3),flag=wx.ALL,border=5)
            ogrnciSoyadYazi.SetFont(yaziBicimi)
            ogrnciSoyadYazi.SetForegroundColour((0, 153, 255))
            ogrnciSoyad = wx.StaticText(self.yuzey,label=satir[5])
            dizilim.Add(ogrnciSoyad,pos=(1,4),flag=wx.ALL,border=5)
            ogrnciSoyad.SetFont(yaziBicimi2)

            ogrnciDogumYazi = wx.StaticText(self.yuzey,label='Doğum Tarihi : ')
            dizilim.Add(ogrnciDogumYazi,pos=(2,0),flag=wx.ALL,border=5)
            ogrnciDogumYazi.SetFont(yaziBicimi)
            ogrnciDogumYazi.SetForegroundColour((0, 153, 255))
            dTarih = satir[6].strftime('%d / %m / %Y')
            ogrnciDogum = wx.StaticText(self.yuzey,label=dTarih)
            dizilim.Add(ogrnciDogum,pos=(2,1),flag=wx.ALL,border=5)
            ogrnciDogum.SetFont(yaziBicimi2)

            ogrnciKayitYazi = wx.StaticText(self.yuzey,label='Kayıt Tarihi : ')
            dizilim.Add(ogrnciKayitYazi,pos=(2,3),flag=wx.ALL,border=5)
            ogrnciKayitYazi.SetFont(yaziBicimi)
            ogrnciKayitYazi.SetForegroundColour((0, 153, 255))
            dTarih = satir[7].strftime('%d / %m / %Y')
            ogrnciKayit = wx.StaticText(self.yuzey,label=dTarih)
            dizilim.Add(ogrnciKayit,pos=(2,4),flag=wx.ALL,border=5)
            ogrnciKayit.SetFont(yaziBicimi2)

            blmYazi = wx.StaticText(self.yuzey,label='Bölümü : ')
            dizilim.Add(blmYazi,pos=(3,0),flag=wx.ALL,border=5)
            blmYazi.SetFont(yaziBicimi)
            blmYazi.SetForegroundColour((0, 153, 255))
            blm = wx.StaticText(self.yuzey,label=self.bolumBelirtec(satir[8]))
            dizilim.Add(blm,pos=(3,1),flag=wx.ALL,border=5)
            blm.SetFont(yaziBicimi2)

            anablmYazi = wx.StaticText(self.yuzey,label='Ana Bilim Dalı : ')
            dizilim.Add(anablmYazi,pos=(3,3),flag=wx.ALL,border=5)
            anablmYazi.SetFont(yaziBicimi)
            anablmYazi.SetForegroundColour((0, 153, 255))
            anablm = wx.StaticText(self.yuzey,label=self.anaBilim(satir[8]))
            dizilim.Add(anablm,pos=(3,4),flag=wx.ALL,border=5)
            anablm.SetFont(yaziBicimi2)

            cnsytYazi = wx.StaticText(self.yuzey,label='Cinsiyeti : ')
            dizilim.Add(cnsytYazi,pos=(4,0),flag=wx.ALL,border=5)
            cnsytYazi.SetFont(yaziBicimi)
            cnsytYazi.SetForegroundColour((0, 153, 255))
            cinsiyet = wx.StaticText(self.yuzey,label=satir[9])
            dizilim.Add(cinsiyet,pos=(4,1),flag=wx.ALL,border=5)
            cinsiyet.SetFont(yaziBicimi2)

            geri = wx.Button(self.yuzey,label='Geri')
            dizilim.Add(geri,pos=(7,0),flag=wx.EXPAND|wx.ALL,border=7)
            geri.Bind(wx.EVT_BUTTON,self.cikis)

            txtKaydet = wx.Button(self.yuzey,label='TXT olarak kaydet')
            dizilim.Add(txtKaydet,pos=(7,3),flag=wx.EXPAND|wx.ALL,border=7)
            txtKaydet.Bind(wx.EVT_BUTTON,self.txtKydt)

            docKaydet = wx.Button(self.yuzey,label='DOC olarak kaydet')
            dizilim.Add(docKaydet,pos=(7,4),flag=wx.EXPAND|wx.ALL,border=7)
            docKaydet.Bind(wx.EVT_BUTTON,self.docKydet)

        self.yuzey.SetSizerAndFit(dizilim)
    def cikis(self,event):
        self.Destroy()
    def bolumBelirtec(self,blm):
        bolum = {
            'bio':'Biyoloji',
            'BIO':'Biyoloji',
            'fiz':'Fizik',
            'FIZ':'Fizik',
            'kim':'Kimya',
            'KIM':'Kimya',
            'bil':'Bilgisayar Mühendisliği',
            'BIL':'Bilgisayar Mühendisliği',
            'elek':'Elektirik-Elektronik Mühendisliği',
            'mak':'Makine Mühendisliği',
            'omt':'Orman Mekaniği ve Teknolojisi',
            'oem':'Orman Endistüri Mühendisliği',
            'om':'Orman Mühendisliği',
            'ELEK':'Elektirik-Elektronik Mühendisliği',
            'MAK':'Makine Mühendisliği',
            'OMT':'Orman Mekaniği ve Teknolojisi',
            'OEM':'Orman Endistüri Mühendisliği',
            'OM':'Orman Mühendisliği',
        }
        return bolum.get(blm,'olmadı')
    def anaBilim(self,blm):
        anaBlm = {
            'bio':'Fen Edebiyet Fakültesi',
            'BIO':'Fen Edebiyet Fakültesi',
            'fiz':'Fen Edebiyet Fakültesi',
            'FIZ':'Fen Edebiyet Fakültesi',
            'kim':'Fen Edebiyet Fakültesi',
            'KIM':'Fen Edebiyet Fakültesi',
            'bil':'Mühendislik Fakültesi',
            'BIL':'Mühendislik Fakültesi',
            'elek':'Mühendislik Fakültesi',
            'mak':'Mühendislik Fakültesi',
            'omt':'Orman Fakültesi',
            'oem':'Orman Fakültesi',
            'om':'Orman Fakültesi',
            'ELEK':'Mühendislik Fakültesi',
            'MAK':'Mühendislik Fakültesi',
            'OMT':'Orman Fakültesi',
            'OEM':'Orman Fakültesi',
            'OM':'Orman Fakültesi',
        }
        return anaBlm.get(blm,'olmadı')
    def ogrtm_durumu(self,durum):
        drm = {
            True:'İkinci Öğretim',
            False:'Normal Öğretim',
        }
        return drm.get(durum,'olmadı')
    def doktora_yuksek(self,durum):
        drm = {
            True:'Yüksek Lisans',
            False:'Doktora',
        }
        return drm.get(durum,'olmadı')
    def txtKydt(self,event):
        bilgiSQL = sqlIslem()
        cursor=bilgiSQL.baglan.cursor()
        try:
            cursor.execute(" exec udSP_ogrenciBilgiGoruntuleme ?,? ",(kullaniciAdi,sifresi))
            kayit = cursor.fetchall()
            wx.MessageBox('Text dosyası oluşturuldu!','BAŞARILI',wx.OK|wx.ICON_INFORMATION)
            with open(r"C:/Users/gthPK/Desktop/ogrenciBilgileri.txt","w") as f:
                csv.writer(f).writerows(kayit)
        except Exception as e:
            bilgiSQL.hata(e)
    def docKydet(self,event):
        bilgiSQL = sqlIslem()
        cursor=bilgiSQL.baglan.cursor()
        try:
            cursor.execute(" exec udSP_ogrenciBilgiGoruntuleme ?,? ",(kullaniciAdi,sifresi))
            kayit = cursor.fetchall()
            wx.MessageBox('DOC dosyası oluşturuldu!','BAŞARILI',wx.OK|wx.ICON_INFORMATION)
            with open(r"C:/Users/gthPK/Desktop/ogrenciBilgileri.doc","w") as f:
                csv.writer(f).writerows(kayit)
        except Exception as e:
            bilgiSQL.hata(e)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------   
class girisOgrenci(wx.Frame):
    def __init__(self,parent,title):
        super(girisOgrenci,self).__init__(parent,title=title,size=(255,200))
        self.Asikar()
        self.Centre()
        self.Show()

    def Asikar(self):
        yuzey = wx.Panel(self)
        diz = wx.GridBagSizer(0,0)

        dersSecim = wx.Button(yuzey,label='Ders Seçim')
        diz.Add(dersSecim,pos=(0,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        dersSecim.Bind(wx.EVT_BUTTON,self.dersSec)

        dersNot = wx.Button(yuzey,label='Sınav Sonuçları')
        diz.Add(dersNot,pos=(2,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        dersNot.Bind(wx.EVT_BUTTON,self.sinavSonuclari)

        #dersPrg = wx.Button(yuzey,label='Ders Programı')
        #diz.Add(dersPrg,pos=(4,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        #ogrenciEkleSil.Bind(wx.EVT_BUTTON,self.ogrencIslemleri)
        
        ogrnciBilgileri = wx.Button(yuzey,label='Öğrenci Bilgileri')
        diz.Add(ogrnciBilgileri,pos=(0,2),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        ogrnciBilgileri.Bind(wx.EVT_BUTTON,self.ogrenciBilgileriGetir)

        Cikis = wx.Button(yuzey,label='Çık')
        diz.Add(Cikis,pos=(6,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        Cikis.Bind(wx.EVT_BUTTON,self.Cik)

        oturumCikis = wx.Button(yuzey,label='Oturumu Kapat')
        diz.Add(oturumCikis,pos=(6,2),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)
        oturumCikis.Bind(wx.EVT_BUTTON,self.oturumCik)
        

        yuzey.SetSizerAndFit(diz)
    def Cik(self,event):
        self.Destroy()
    def oturumCik(self,event):
        kul_gir=kulGiris(None,title='Kullanıcı Girişi')
        self.Destroy()
    def ogrenciBilgileriGetir(self,event):
        ogrenci_bilgi=ogrenciBilgileriGoster(None,title='Öğrenci Bilgileri')
    def sinavSonuclari(self,event):
        sinav=sinavSonuclariniGorme(None,title='Sınav Sonuçları')
    def dersSec(self,event):
        dsec = ogrenciDersSec(None,title='Ders Seçim Ekranı')
class ogrenciBilgileriGoster(wx.Frame):
    def __init__(self,parent,title):
        super(ogrenciBilgileriGoster,self).__init__(parent,title=title,size=(800,350))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        self.yuzey = wx.Panel(self)
        dizilim = wx.GridBagSizer(0,0)

        yaziBicimi = wx.Font(10,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        yaziBicimi2 = wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        bilgiSQL = sqlIslem()
        cursor=bilgiSQL.baglan.cursor()
        try:
            cursor.execute(" exec udSP_ogrenciBilgiGoruntuleme ?,? ",(kullaniciAdi,sifresi))
            kayit = cursor.fetchall()
        except Exception as e:
            bilgiSQL.hata(e)
        for satir in kayit:
            #print("Öğrenci Belirtec = ",satir[4])
            ogrnciBlrtciYazi = wx.StaticText(self.yuzey,label='Öğrenci Belirteci : ')
            dizilim.Add(ogrnciBlrtciYazi,pos=(0,0),flag=wx.ALL,border=5)
            ogrnciBlrtciYazi.SetFont(yaziBicimi)
            ogrnciBlrtciYazi.SetForegroundColour((0, 153, 255))
            ogrnciBlrtci = wx.StaticText(self.yuzey,label=satir[0])
            dizilim.Add(ogrnciBlrtci,pos=(0,1),flag=wx.ALL,border=5)
            ogrnciBlrtci.SetFont(yaziBicimi2)

            ogrnciTcYazi = wx.StaticText(self.yuzey,label='TC Kimlik Numarası : ')
            dizilim.Add(ogrnciTcYazi,pos=(0,3),flag=wx.ALL,border=5)
            ogrnciTcYazi.SetFont(yaziBicimi)
            ogrnciTcYazi.SetForegroundColour((0, 153, 255))
            ogrnciTc = wx.StaticText(self.yuzey,label=satir[1])
            dizilim.Add(ogrnciTc,pos=(0,4),flag=wx.ALL,border=5)
            ogrnciTc.SetFont(yaziBicimi2)

            if satir[4] is None:
                if satir[3] is None:
                    ogrnciAdYazi = wx.StaticText(self.yuzey,label='Adı : ')
                    dizilim.Add(ogrnciAdYazi,pos=(1,0),flag=wx.ALL,border=5)
                    ogrnciAdYazi.SetFont(yaziBicimi)
                    ogrnciAdYazi.SetForegroundColour((0, 153, 255))
                    ogrnciAd = wx.StaticText(self.yuzey,label=satir[2])
                    dizilim.Add(ogrnciAd,pos=(1,1),flag=wx.ALL,border=5)
                    ogrnciAd.SetFont(yaziBicimi2)
                else:
                    ogrnciAdYazi = wx.StaticText(self.yuzey,label='Adı : ')
                    dizilim.Add(ogrnciAdYazi,pos=(1,0),flag=wx.ALL,border=5)
                    ogrnciAdYazi.SetFont(yaziBicimi)
                    ogrnciAdYazi.SetForegroundColour((0, 153, 255))
                    ogrnciAd = wx.StaticText(self.yuzey,label=satir[2]+' '+satir[3])
                    dizilim.Add(ogrnciAd,pos=(1,1),flag=wx.ALL,border=5)
                    ogrnciAd.SetFont(yaziBicimi2)
            else:
                ogrnciAdYazi = wx.StaticText(self.yuzey,label='Adı : ')
                dizilim.Add(ogrnciAdYazi,pos=(1,0),flag=wx.ALL,border=5)
                ogrnciAdYazi.SetFont(yaziBicimi)
                ogrnciAdYazi.SetForegroundColour((0, 153, 255))
                ogrnciAd = wx.StaticText(self.yuzey,label=satir[2]+' '+satir[3]+' '+satir[4])
                dizilim.Add(ogrnciAd,pos=(1,1),flag=wx.ALL,border=5)
                ogrnciAd.SetFont(yaziBicimi2)

            ogrnciSoyadYazi = wx.StaticText(self.yuzey,label='Soyadı : ')
            dizilim.Add(ogrnciSoyadYazi,pos=(1,3),flag=wx.ALL,border=5)
            ogrnciSoyadYazi.SetFont(yaziBicimi)
            ogrnciSoyadYazi.SetForegroundColour((0, 153, 255))
            ogrnciSoyad = wx.StaticText(self.yuzey,label=satir[5])
            dizilim.Add(ogrnciSoyad,pos=(1,4),flag=wx.ALL,border=5)
            ogrnciSoyad.SetFont(yaziBicimi2)

            ogrnciDogumYazi = wx.StaticText(self.yuzey,label='Doğum Tarihi : ')
            dizilim.Add(ogrnciDogumYazi,pos=(2,0),flag=wx.ALL,border=5)
            ogrnciDogumYazi.SetFont(yaziBicimi)
            ogrnciDogumYazi.SetForegroundColour((0, 153, 255))
            dTarih = satir[6].strftime('%d / %m / %Y')
            ogrnciDogum = wx.StaticText(self.yuzey,label=dTarih)
            dizilim.Add(ogrnciDogum,pos=(2,1),flag=wx.ALL,border=5)
            ogrnciDogum.SetFont(yaziBicimi2)

            ogrnciKayitYazi = wx.StaticText(self.yuzey,label='Kayıt Tarihi : ')
            dizilim.Add(ogrnciKayitYazi,pos=(2,3),flag=wx.ALL,border=5)
            ogrnciKayitYazi.SetFont(yaziBicimi)
            ogrnciKayitYazi.SetForegroundColour((0, 153, 255))
            dTarih = satir[7].strftime('%d / %m / %Y')
            ogrnciKayit = wx.StaticText(self.yuzey,label=dTarih)
            dizilim.Add(ogrnciKayit,pos=(2,4),flag=wx.ALL,border=5)
            ogrnciKayit.SetFont(yaziBicimi2)

            blmYazi = wx.StaticText(self.yuzey,label='Bölümü : ')
            dizilim.Add(blmYazi,pos=(3,0),flag=wx.ALL,border=5)
            blmYazi.SetFont(yaziBicimi)
            blmYazi.SetForegroundColour((0, 153, 255))
            blm = wx.StaticText(self.yuzey,label=self.bolumBelirtec(satir[8]))
            dizilim.Add(blm,pos=(3,1),flag=wx.ALL,border=5)
            blm.SetFont(yaziBicimi2)

            anablmYazi = wx.StaticText(self.yuzey,label='Ana Bilim Dalı : ')
            dizilim.Add(anablmYazi,pos=(3,3),flag=wx.ALL,border=5)
            anablmYazi.SetFont(yaziBicimi)
            anablmYazi.SetForegroundColour((0, 153, 255))
            anablm = wx.StaticText(self.yuzey,label=self.anaBilim(satir[8]))
            dizilim.Add(anablm,pos=(3,4),flag=wx.ALL,border=5)
            anablm.SetFont(yaziBicimi2)

            cnsytYazi = wx.StaticText(self.yuzey,label='Cinsiyeti : ')
            dizilim.Add(cnsytYazi,pos=(4,0),flag=wx.ALL,border=5)
            cnsytYazi.SetFont(yaziBicimi)
            cnsytYazi.SetForegroundColour((0, 153, 255))
            cinsiyet = wx.StaticText(self.yuzey,label=satir[9])
            dizilim.Add(cinsiyet,pos=(4,1),flag=wx.ALL,border=5)
            cinsiyet.SetFont(yaziBicimi2)

            aktsYazi = wx.StaticText(self.yuzey,label='AKTS : ')
            dizilim.Add(aktsYazi,pos=(4,3),flag=wx.ALL,border=5)
            aktsYazi.SetFont(yaziBicimi)
            aktsYazi.SetForegroundColour((0, 153, 255))
            akts = wx.StaticText(self.yuzey,label=str(satir[10]))
            dizilim.Add(akts,pos=(4,4),flag=wx.ALL,border=5)
            akts.SetFont(yaziBicimi2)

            ogrtmYazi = wx.StaticText(self.yuzey,label='Öğretim Durumu : ')
            dizilim.Add(ogrtmYazi,pos=(5,0),flag=wx.ALL,border=5)
            ogrtmYazi.SetFont(yaziBicimi)
            ogrtmYazi.SetForegroundColour((0, 153, 255))
            ogrtm = wx.StaticText(self.yuzey,label=self.ogrtm_durumu(satir[11]))
            dizilim.Add(ogrtm,pos=(5,1),flag=wx.ALL,border=5)
            ogrtm.SetFont(yaziBicimi2)

            dokyukYazi = wx.StaticText(self.yuzey,label='Doktora / Yüksek Lisans : ')
            dizilim.Add(dokyukYazi,pos=(5,3),flag=wx.ALL,border=5)
            dokyukYazi.SetFont(yaziBicimi)
            dokyukYazi.SetForegroundColour((0, 153, 255))
            dokyuk = wx.StaticText(self.yuzey,label=self.doktora_yuksek(satir[12]))
            dizilim.Add(dokyuk,pos=(5,4),flag=wx.ALL,border=5)
            dokyuk.SetFont(yaziBicimi2)

            geri = wx.Button(self.yuzey,label='Geri')
            dizilim.Add(geri,pos=(7,0),flag=wx.EXPAND|wx.ALL,border=7)
            geri.Bind(wx.EVT_BUTTON,self.cikis)

            txtKaydet = wx.Button(self.yuzey,label='TXT olarak kaydet')
            dizilim.Add(txtKaydet,pos=(7,3),flag=wx.EXPAND|wx.ALL,border=7)
            txtKaydet.Bind(wx.EVT_BUTTON,self.txtKydt)

            docKaydet = wx.Button(self.yuzey,label='DOC olarak kaydet')
            dizilim.Add(docKaydet,pos=(7,4),flag=wx.EXPAND|wx.ALL,border=7)
            docKaydet.Bind(wx.EVT_BUTTON,self.docKydet)

        self.yuzey.SetSizerAndFit(dizilim)
    def cikis(self,event):
        self.Destroy()
    def bolumBelirtec(self,blm):
        bolum = {
            'bio':'Biyoloji',
            'BIO':'Biyoloji',
            'fiz':'Fizik',
            'FIZ':'Fizik',
            'kim':'Kimya',
            'KIM':'Kimya',
            'bil':'Bilgisayar Mühendisliği',
            'BIL':'Bilgisayar Mühendisliği',
            'elek':'Elektirik-Elektronik Mühendisliği',
            'mak':'Makine Mühendisliği',
            'omt':'Orman Mekaniği ve Teknolojisi',
            'oem':'Orman Endistüri Mühendisliği',
            'om':'Orman Mühendisliği',
            'ELEK':'Elektirik-Elektronik Mühendisliği',
            'MAK':'Makine Mühendisliği',
            'OMT':'Orman Mekaniği ve Teknolojisi',
            'OEM':'Orman Endistüri Mühendisliği',
            'OM':'Orman Mühendisliği',
        }
        return bolum.get(blm,'olmadı')
    def anaBilim(self,blm):
        anaBlm = {
            'bio':'Fen Edebiyet Fakültesi',
            'BIO':'Fen Edebiyet Fakültesi',
            'fiz':'Fen Edebiyet Fakültesi',
            'FIZ':'Fen Edebiyet Fakültesi',
            'kim':'Fen Edebiyet Fakültesi',
            'KIM':'Fen Edebiyet Fakültesi',
            'bil':'Mühendislik Fakültesi',
            'BIL':'Mühendislik Fakültesi',
            'elek':'Mühendislik Fakültesi',
            'mak':'Mühendislik Fakültesi',
            'omt':'Orman Fakültesi',
            'oem':'Orman Fakültesi',
            'om':'Orman Fakültesi',
            'ELEK':'Mühendislik Fakültesi',
            'MAK':'Mühendislik Fakültesi',
            'OMT':'Orman Fakültesi',
            'OEM':'Orman Fakültesi',
            'OM':'Orman Fakültesi',
        }
        return anaBlm.get(blm,'olmadı')
    def ogrtm_durumu(self,durum):
        drm = {
            True:'İkinci Öğretim',
            False:'Normal Öğretim',
        }
        return drm.get(durum,'olmadı')
    def doktora_yuksek(self,durum):
        drm = {
            True:'Yüksek Lisans',
            False:'Doktora',
        }
        return drm.get(durum,'olmadı')
    def txtKydt(self,event):
        bilgiSQL = sqlIslem()
        cursor=bilgiSQL.baglan.cursor()
        try:
            cursor.execute(" exec udSP_ogrenciBilgiGoruntuleme ?,? ",(kullaniciAdi,sifresi))
            kayit = cursor.fetchall()
            wx.MessageBox('Text dosyası oluşturuldu!','BAŞARILI',wx.OK|wx.ICON_INFORMATION)
            with open(r"C:/Users/gthPK/Desktop/ogrenciBilgileri.txt","w") as f:
                csv.writer(f).writerows(kayit)
        except Exception as e:
            bilgiSQL.hata(e)
    def docKydet(self,event):
        bilgiSQL = sqlIslem()
        cursor=bilgiSQL.baglan.cursor()
        try:
            cursor.execute(" exec udSP_ogrenciBilgiGoruntuleme ?,? ",(kullaniciAdi,sifresi))
            kayit = cursor.fetchall()
            wx.MessageBox('DOC dosyası oluşturuldu!','BAŞARILI',wx.OK|wx.ICON_INFORMATION)
            with open(r"C:/Users/gthPK/Desktop/ogrenciBilgileri.doc","w") as f:
                csv.writer(f).writerows(kayit)
        except Exception as e:
            bilgiSQL.hata(e)
class sinavSonuclariniGorme(wx.Frame):
    def __init__(self,parent,title):
        super(sinavSonuclariniGorme,self).__init__(parent,title=title,size=(800,350))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        self.yuzey = wx.Panel(self)
        #self.ogrenciSiralama = wx.Panel(self.yuzey)
        self.dizilim = wx.GridBagSizer(0,0)
        self.sayac = 0

        yaziBicimi = wx.Font(13,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        yaziBicimi2 = wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)

        Numara = wx.StaticText(self.yuzey,-1,label='Numarası')
        dersAd = wx.StaticText(self.yuzey,-1,label='Dersin Adı')
        finalNotu = wx.StaticText(self.yuzey,-1,label='Final Notu')
        vizeNotu = wx.StaticText(self.yuzey,-1,label='Vize Notu')
        Odev = wx.StaticText(self.yuzey,-1,label='Ödev')
        Numara.SetFont(yaziBicimi)
        Numara.SetForegroundColour((122, 0, 37))
        dersAd.SetFont(yaziBicimi)
        dersAd.SetForegroundColour((122, 0, 37))
        finalNotu.SetFont(yaziBicimi)
        finalNotu.SetForegroundColour((122, 0, 37))
        vizeNotu.SetFont(yaziBicimi)
        vizeNotu.SetForegroundColour((122, 0, 37))
        Odev.SetFont(yaziBicimi)
        Odev.SetForegroundColour((122, 0, 37))

        #Numara.SetPosition((10,10))
        #ad1.SetPosition((90,10))
        #ad2.SetPosition((170,10))
        #ad3.SetPosition((250,10))
        #soyad.SetPosition((330,10))
        #finalNotu.SetPosition((410,10))
        #vizeNotu.SetPosition((520,10))
        #Odev.SetPosition((630,10))

        self.dizilim.Add(Numara,pos=(0,0),flag=wx.ALL,border=5)
        self.dizilim.Add(dersAd,pos=(0,1),flag=wx.ALL,border=5)
        self.dizilim.Add(finalNotu,pos=(0,2),flag=wx.ALL,border=5)
        self.dizilim.Add(vizeNotu,pos=(0,3),flag=wx.ALL,border=5)
        self.dizilim.Add(Odev,pos=(0,4),flag=wx.ALL,border=5)


        sqlBaglan = sqlIslem()
        cursor=sqlBaglan.baglan.cursor()
        cursor.execute("exec udSP_ogrenciSinavSonucGorme ?",(kullaniciAdi))
        satir = cursor.fetchone()
        while satir:
            print(satir)
            self.sayac = self.sayac + 1
            satir = cursor.fetchone()
        print(self.sayac)
        cursor.execute("exec udSP_ogrenciSinavSonucGorme ?",(kullaniciAdi))
        satir = cursor.fetchone()
        y=1
        
        while satir:
            z=0
            snc = wx.StaticText(self.yuzey,-1,label=satir[0])
            #snc.SetPosition((10+y,z))
            self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
            snc.SetFont(yaziBicimi2)
            snc.SetForegroundColour((1, 143, 143))
            z=z+1
            snc = wx.StaticText(self.yuzey,-1,label=satir[1])
            #snc.SetPosition((y,z))
            self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
            snc.SetFont(yaziBicimi2)
            snc.SetForegroundColour((1, 143, 143))
            if satir[2] is not None:
                z=z+1
                snc = wx.StaticText(self.yuzey,-1,label=str(satir[2]))
                #snc.SetPosition((y,z))
                self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
                snc.SetFont(yaziBicimi2)
                snc.SetForegroundColour((1, 143, 143))
            else:
                z=z+1
                snc = wx.StaticText(self.yuzey,-1,label='Açıklanmadı')
                self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
                snc.SetFont(yaziBicimi2)
                snc.SetForegroundColour((1, 143, 143))
                #snc.SetPosition((y,z))
            if satir[3] is not None:
                z=z+1
                snc = wx.StaticText(self.yuzey,-1,label=str(satir[3]))
                self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
                #snc.SetPosition((y,z))
                snc.SetFont(yaziBicimi2)
                snc.SetForegroundColour((1, 143, 143))
            else:
                z=z+1
                snc = wx.StaticText(self.yuzey,-1,label='Açıklanmadı')
                self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
                #snc.SetPosition((y,z))
                snc.SetFont(yaziBicimi2)
                snc.SetForegroundColour((1, 143, 143))
            if satir[4] is not None:
                z=z+1
                snc = wx.StaticText(self.yuzey,-1,label=str(satir[4]))
                self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
                #snc.SetPosition((y,z))
                snc.SetFont(yaziBicimi2)
                snc.SetForegroundColour((1, 143, 143))
            else:
                z=z+1
                snc = wx.StaticText(self.yuzey,-1,label='Açıklanmadı')
                self.dizilim.Add(snc,pos=(y,z),flag=wx.ALL,border=5)
                #snc.SetPosition((y,z))
                snc.SetFont(yaziBicimi2)
                snc.SetForegroundColour((1, 143, 143))
            y=y+1
            satir=cursor.fetchone()           
        self.sayac=0
        self.yuzey.SetSizerAndFit(self.dizilim)
class ogrenciDersSec(wx.Frame):
    def __init__(self,parent,title):
        super(ogrenciDersSec,self).__init__(parent,title=title,size=(800,600))
        self.Asikar()
        self.Centre()
        self.Show()

    def Asikar(self):
        self.yuzey = wx.Panel(self)
        diz = wx.GridBagSizer(0,0)

        cikisDugme = wx.Button(self.yuzey,label='Çık')
        diz.Add(cikisDugme,pos=(0,0),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)
        cikisDugme.Bind(wx.EVT_BUTTON,self.cikis)

        sqlBaglan = sqlIslem()
        cursor = sqlBaglan.baglan.cursor()
        cursor.execute("select bolumBelirtec,akts from ogrenciTB where ogrenciBelirtec = ?",(kullaniciAdi))
        global blrtcBLM
        global akts_ogrenci
        satir = cursor.fetchone()
        while satir:
            blrtcBLM = satir[0]
            akts_ogrenci = satir[1]
            satir = cursor.fetchone()
        #print(blrtcBLM)
        #print(akts_ogrenci)
        cursor.close()
        sqlBaglan.baglan.close()

        self.sayac = 0
        aydi = 1
        x = 1
        sqlBaglan = sqlIslem()
        cursor = sqlBaglan.baglan.cursor()
        cursor.execute("exec udSP_dersleriGetir ?",(blrtcBLM))
        satir = cursor.fetchone()
        while satir:
            y = 2
            drsBrtc = wx.StaticText(self.yuzey,id=aydi,label=satir[0])
            diz.Add(drsBrtc,pos=(x,y),flag=wx.ALL,border=5)
            y=y+1
            aydi=aydi+1
            drsADI = wx.StaticText(self.yuzey,id=aydi,label=satir[1])
            diz.Add(drsADI,pos=(x,y),flag=wx.ALL,border=5)
            y=y+1
            aydi=aydi+1
            drsAKTS = wx.StaticText(self.yuzey,id=aydi,label=str(satir[2]))
            diz.Add(drsAKTS,pos=(x,y),flag=wx.ALL,border=5)
            y=y+1
            aydi=aydi+1
            blm_belirtec = wx.StaticText(self.yuzey,id=aydi,label=satir[3])
            diz.Add(blm_belirtec,pos=(x,y),flag=wx.ALL,border=5)
            y=y+1
            aydi=aydi+1
            self.sec = wx.Button(self.yuzey,id=aydi,label='Seç')
            diz.Add(self.sec,pos=(x,y),flag=wx.ALL,border=5)
            sc = functools.partial(self.drsSEC,sayi = aydi)
            self.sec.Bind(wx.EVT_BUTTON,sc)
            aydi=aydi+1

            satir = cursor.fetchone()
            x=x+1
            self.sayac = self.sayac + 1 
        #print(self.sayac)
        self.yuzey.SetSizerAndFit(diz)
    def cikis(self,event):
        self.Destroy()
    def drsSEC(self,event,sayi):
        dersSecSQL = sqlIslem()
        cursor = dersSecSQL.baglan.cursor()
        for x in range(1,(self.sayac*5)+1):
            if x==sayi:
                blrtc = self.yuzey.FindWindowById(x-4).GetLabel()
                ad = self.yuzey.FindWindowById(x-3).GetLabel()
                ts = self.yuzey.FindWindowById(x-2).GetLabel()
                print(blrtc)
                print(ad)
                print(ts)
                self.sec.Hide()
                #print(blrtc2)
        cursor.execute("exec udSP_ogrenciDersSecme ?, ? ",(blrtc,kullaniciAdi))
        dersSecSQL.baglan.commit()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
class girisYonetici(wx.Frame):
    def __init__(self,parent,title):
        super(girisYonetici,self).__init__(parent,title=title,size=(430,240))
        self.Asikar()
        self.Centre()
        self.Show()

    def Asikar(self):
        yuzey = wx.Panel(self)
        diz = wx.GridBagSizer(0,0)
        
        ogrenciEkleSil = wx.Button(yuzey,label='Öğrenci Ekle/Sil')
        diz.Add(ogrenciEkleSil,pos=(0,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        ogrenciEkleSil.Bind(wx.EVT_BUTTON,self.ogrencIslemleri)

        ogretmenEkleSil = wx.Button(yuzey,label='Öğretmen Ekle/Sil')
        diz.Add(ogretmenEkleSil,pos=(2,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        ogretmenEkleSil.Bind(wx.EVT_BUTTON,self.ogretmenIslemleri)

        dersEkleSil = wx.Button(yuzey,label='Ders Ekle/Sil')
        diz.Add(dersEkleSil,pos=(4,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        dersEkleSil.Bind(wx.EVT_BUTTON,self.dersIslemleri)

        gncllm = wx.Button(yuzey,label='Öğrenci/Ders/Öğretmen Güncelle')
        diz.Add(gncllm,pos=(6,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        gncllm.Bind(wx.EVT_BUTTON,self.guncelleme)

        yedek = wx.Button(yuzey,label='Veritabanını Yedekle')
        diz.Add(yedek,pos=(0,2),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        yedek.Bind(wx.EVT_BUTTON,self.yedek_FenBE)

        dondur = wx.Button(yuzey,label='Veritabanını Yedekten Döndür')
        diz.Add(dondur,pos=(2,2),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        dondur.Bind(wx.EVT_BUTTON,self.dondur_FenBE)

        dersATA = wx.Button(yuzey,label='Öğretmene Ders Atama')
        diz.Add(dersATA,pos=(4,2),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        dersATA.Bind(wx.EVT_BUTTON,self.drsAtama)

        txtVeriAlma = wx.Button(yuzey,label='TXT dosyasından veri alma')
        diz.Add(txtVeriAlma,pos=(6,2),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        txtVeriAlma.Bind(wx.EVT_BUTTON,self.veriCekme)

        Cikis = wx.Button(yuzey,label='Çık')
        diz.Add(Cikis,pos=(8,0),span=(2,2),flag=wx.EXPAND|wx.ALL,border=7)
        Cikis.Bind(wx.EVT_BUTTON,self.Cik)

        oturumCikis = wx.Button(yuzey,label='Oturumu Kapat')
        diz.Add(oturumCikis,pos=(8,2),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)
        oturumCikis.Bind(wx.EVT_BUTTON,self.oturumCik)

        yuzey.SetSizerAndFit(diz)
    def Cik(self,event):
        self.Destroy()
    def oturumCik(self,event):
        kul_gir=kulGiris(None,title='Kullanıcı Girişi')
        self.Destroy()
    def ogrencIslemleri(self,event):
        ogrenci_islemleri=ogrenciOlaylari(None,title='Öğrenci Ekleme / Silme')
    def ogretmenIslemleri(self,event):
        ogretmen_islemleri=ogretmenOlaylari(None,title='Öğretmen Ekleme / Silme')
    def dersIslemleri(self,event):
        ders_islemleri=dersOlaylari(None,title='Ders Ekleme / Silme')
    def yedek_FenBE(self,event):
        bilgiSQL = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};Server=DESKTOP-R71L9L2\SQLEXPRESS;Database=master;Trusted_Connection=yes;')
        cursor=bilgiSQL.cursor()
        bilgiSQL.autocommit = True
        cursor.execute(" exec udSP_yedekleme ")
        satir = cursor.fetchone()
        #cursor.close()
        #bilgiSQL.close()
    def dondur_FenBE(self,event):
        dondurDosya = wx.FileDialog(self,message='Yedek dosyasını seç',defaultDir='c:',defaultFile='',wildcard='bak dosyası (*.bak)|*.bak',style=wx.FD_OPEN|wx.FD_MULTIPLE|wx.FD_CHANGE_DIR)
        if dondurDosya.ShowModal()==wx.ID_OK:
            yol = dondurDosya.GetPaths()
            print(yol[0])
        dondurDosya.Destroy()

        dondurSQL = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};Server=DESKTOP-R71L9L2\SQLEXPRESS;Database=master;Trusted_Connection=yes;')
        cursor = dondurSQL.cursor()
        try:
            dondurSQL.autocommit=True
            cursor.execute(" exec udSP_yedektenDON ?",(yol))
        except Exception as e:
            wx.MessageBox('Hata : %s' %(e),'HATA',wx.OK|wx.ICON_INFORMATION)
    def veriCekme(self,event):
        vrCkmSQL = sqlIslem()
        cursor = vrCkmSQL.baglan.cursor()
        try:
            cursor.execute("exec udSP_dosyadanVeriAlma")
            vrCkmSQL.baglan.commit()
            wx.MessageBox('Başarılı','OLDU',wx.OK|wx.ICON_INFORMATION)
        except Exception as e:
            vrCkmSQL.hata(e)
    def guncelleme(self,event):
        guncel = guncellemeEkrani(None,title='Güncelleme Ekranı')
    def drsAtama(self,event):
        atama = ogretmenDersSec(None,title='Öğretmene Ders Atama')
class guncellemeEkrani(wx.Frame):
    def __init__(self,parent,title):
        super(guncellemeEkrani,self).__init__(parent,title=title,size=(1200,300))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        yuzey = wx.Panel(self)
        #self.diz = wx.GridBagSizer(0,0)
        self.panelDers = wx.Panel(yuzey)
        self.dizDers = wx.GridBagSizer(0,0)
        #self.panelOgrenci = wx.Panel(yuzey)
        #self.panelOgretmen = wx.Panel(yuzey)
        self.panelDers.SetPosition((10,75))

        secenekYazi= wx.StaticText(yuzey,label='Neyi güncelleyeceğinizi seçiniz : ')
        #self.diz.Add(secenekYazi,pos=(1,0),flag=wx.ALL,border=5)
        secenekYazi.SetPosition((150,25))
        self.secenek = wx.Choice(yuzey,choices=('Ders','Öğretmen','Öğrenci'))
        #self.diz.Add(self.secenek,pos=(1,1),flag=wx.ALL,border=5)
        self.secenek.SetPosition((330,20))

        scm = wx.Button(yuzey,label='Güncelle')
        #self.diz.Add(scm,pos=(1,2),flag=wx.ALL,border=5)
        scm.Bind(wx.EVT_BUTTON,self.secim)
        scm.SetPosition((430,18))

        ck = wx.Button(yuzey,label='Geri')
        #self.diz.Add(ck,pos=(0,0),flag=wx.ALL,border=5)
        ck.Bind(wx.EVT_BUTTON,self.Cik)
        ck.SetPosition((7,7))

        ###########------------------------------------------------Ders Güncelleme----###############################
        self.drs_belirtecYazi = wx.StaticText(self.panelDers,label='Dersin Belitecini Seçiniz : ')
        self.dizDers.Add(self.drs_belirtecYazi,pos=(0,0),flag=wx.ALL,border=5)
        
        self.drs_belirtec = wx.TextCtrl(self.panelDers)
        self.dizDers.Add(self.drs_belirtec,pos=(0,1),flag=wx.ALL,border=5)

        scm2 = wx.Button(self.panelDers,label='Seç')
        self.dizDers.Add(scm2,pos=(0,2),flag=wx.ALL,border=5)
        scm2.Bind(wx.EVT_BUTTON,self.ders_secim)

        self.blrtc = wx.StaticText(self.panelDers,label="",size=(30,10))
        self.dizDers.Add(self.blrtc,pos=(1,1),flag=wx.EXPAND|wx.ALL,border=5)

        self.drsADI = wx.StaticText(self.panelDers,label="",size=(200,10))
        self.dizDers.Add(self.drsADI,pos=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        self.saati = wx.StaticText(self.panelDers,label="",size=(50,10))
        self.dizDers.Add(self.saati,pos=(1,3),flag=wx.EXPAND|wx.ALL,border=5)

        self.sinif = wx.StaticText(self.panelDers,label="",size=(50,10))
        self.dizDers.Add(self.sinif,pos=(1,4),flag=wx.EXPAND|wx.ALL,border=5)

        self.gun = wx.StaticText(self.panelDers,label="",size=(55,10))
        self.dizDers.Add(self.gun,pos=(1,5),flag=wx.EXPAND|wx.ALL,border=5)
 
        self.teori = wx.StaticText(self.panelDers,label="",size=(30,10))
        self.dizDers.Add(self.teori,pos=(1,6),flag=wx.EXPAND|wx.ALL,border=5)
   
        self.uyg = wx.StaticText(self.panelDers,label="",size=(30,10))
        self.dizDers.Add(self.uyg,pos=(1,7),flag=wx.EXPAND|wx.ALL,border=5)

        self.kredi = wx.StaticText(self.panelDers,label="",size=(30,10))
        self.dizDers.Add(self.kredi,pos=(1,8),flag=wx.EXPAND|wx.ALL,border=5)

        self.akts = wx.StaticText(self.panelDers,label="",size=(30,10))
        self.dizDers.Add(self.akts,pos=(1,9),flag=wx.EXPAND|wx.ALL,border=5)

        self.blm_blrtc = wx.StaticText(self.panelDers,label="",size=(30,10))
        self.dizDers.Add(self.blm_blrtc,pos=(1,10),flag=wx.EXPAND|wx.ALL,border=5)

        self.blrtcDEGER = wx.StaticText(self.panelDers,label="Yeni değerleri : ",size=(30,20))
        self.dizDers.Add(self.blrtcDEGER,pos=(2,1),flag=wx.EXPAND|wx.ALL,border=5)

        self.drsADIdeger = wx.TextCtrl(self.panelDers,size=(200,10))
        self.dizDers.Add(self.drsADIdeger,pos=(2,2),flag=wx.EXPAND|wx.ALL,border=5)

        self.saatiDEGER = wx.TextCtrl(self.panelDers,size=(50,10))
        self.dizDers.Add(self.saatiDEGER,pos=(2,3),flag=wx.EXPAND|wx.ALL,border=5)

        self.sinifDEGER = wx.TextCtrl(self.panelDers,size=(50,10))
        self.dizDers.Add(self.sinifDEGER,pos=(2,4),flag=wx.EXPAND|wx.ALL,border=5)

        self.gunDEGER = wx.TextCtrl(self.panelDers,size=(55,10))
        self.dizDers.Add(self.gunDEGER,pos=(2,5),flag=wx.EXPAND|wx.ALL,border=5)
 
        self.teoriDEGER = wx.TextCtrl(self.panelDers,size=(30,10))
        self.dizDers.Add(self.teoriDEGER,pos=(2,6),flag=wx.EXPAND|wx.ALL,border=5)
   
        self.uygDEGER = wx.TextCtrl(self.panelDers,size=(30,10))
        self.dizDers.Add(self.uygDEGER,pos=(2,7),flag=wx.EXPAND|wx.ALL,border=5)

        self.krediDEGER = wx.TextCtrl(self.panelDers,size=(30,10))
        self.dizDers.Add(self.krediDEGER,pos=(2,8),flag=wx.EXPAND|wx.ALL,border=5)

        self.aktsDEGER = wx.TextCtrl(self.panelDers,size=(30,10))
        self.dizDers.Add(self.aktsDEGER,pos=(2,9),flag=wx.EXPAND|wx.ALL,border=5)

        self.blm_blrtcDEGER = wx.TextCtrl(self.panelDers,size=(30,10))
        self.dizDers.Add(self.blm_blrtcDEGER,pos=(2,10),flag=wx.EXPAND|wx.ALL,border=5)


        self.drsGncllm = wx.Button(self.panelDers,label='Güncelle')
        self.dizDers.Add(self.drsGncllm,pos=(4,11),flag=wx.EXPAND|wx.ALL,border=5)
        self.drsGncllm.Bind(wx.EVT_BUTTON,self.guncelle)
        ###########------------------------------------------------Ders Güncelleme----###############################


        #self.panelDers.SetBackgroundColour((179,179,179))
        #self.panelOgrenci.Hide()
        #self.panelOgretmen.Hide()
        self.panelDers.Hide()
        
        
        self.panelDers.SetSizerAndFit(self.dizDers)
        #self.yuzey.SetSizerAndFit(self.diz)
    def Cik(self,event):
        self.Destroy()
    def secim(self,event):
        secim_ = self.secenek.GetString(self.secenek.GetSelection())
        #print (secim_)
        if secim_ == 'Ders':
            print(secim_)
            self.panelDers.Show()
            #self.panelOgrenci.Hide()
            #self.panelOgretmen.Hide()
        elif secim_ == 'Öğrenci':
            print(secim_)
            self.panelDers.Hide()
            #self.panelOgrenci.Show()
            #self.panelOgretmen.Hide()
        else:
            print(secim_)
            self.panelDers.Hide()
            #self.panelOgrenci.Hide()
            #self.panelOgretmen.Show()
    def ders_secim(self,event):
        scm = self.drs_belirtec.GetValue()
        #print(scm)
        dersSQL = sqlIslem()
        cursor = dersSQL.baglan.cursor()
        cursor.execute('select dersBelirtec,dersADI,saati,sinif,dersinGunu,teori,uygulama,kredisi,akts,bolumBelirtec from derslerTB where dersBelirtec = ? ',(scm))
        try:
            satir = cursor.fetchone()
            self.blrtc.SetLabel(satir[0])
            self.drsADI.SetLabel(satir[1])
            #print(satir[2].strftime("%H:%M:%S"))
            st =  satir[2].strftime("%H:%M:%S")
            self.saati.SetLabel(st)
            self.sinif.SetLabel(satir[3])
            self.gun.SetLabel(satir[4])
            self.teori.SetLabel(str(satir[5]))
            self.uyg.SetLabel(str(satir[6]))
            self.kredi.SetLabel(str(satir[7]))
            self.akts.SetLabel(str(satir[8]))
            self.blm_blrtc.SetLabel(satir[9])
            #while satir:
                #print(satir)
                #satir = cursor.fetchone()
        except Exception as e:
            dersSQL.hata(e)
    def guncelle(self,event):
        gnclSQL = sqlIslem()
        cursor = gnclSQL.baglan.cursor()

        print(self.drsADI.GetLabel())

        drsAD = self.drsADIdeger.GetValue()
        st = self.saatiDEGER.GetValue()
        snf = self.sinifDEGER.GetValue()
        gn = self.gunDEGER.GetValue()
        tri = self.teoriDEGER.GetValue()
        uyglm = self.uygDEGER.GetValue()
        krdi = self.krediDEGER.GetValue()
        kts = self.aktsDEGER.GetValue()
        blmBlrtec = self.blm_blrtcDEGER.GetValue()

        if drsAD==" ":
            drsAd = self.drsADI.GetLabel()
        if st==" ":
            st = self.saati.GetLabel()
        if snf==" ":
            snf = self.sinif.GetLabel()
        if gn==" ":
            gn = self.gun.GetLabel()
        if tri==" ":
            tri = self.teori.GetLabel()
        if uyglm==" ":
            uyglm = self.uyg.GetLabel()
        if krdi==" ":
            krdi = self.kredi.GetLabel()
        if kts==" ":
            kts = self.akts.GetLabel()
        if blmBlrtec==" ":
            blmBlrtec = self.blm_blrtc.GetLabel()

        try:
            cursor.execute("exec udSP_dersGuncelleme ?,?,?,?,?,?,?,?,?,?",(self.blrtc.GetLabel(),drsAD,st,snf,gn,tri,uyglm,krdi,kts,blmBlrtec))
            gnclSQL.baglan.commit()
            wx.MessageBox('Başarılı','Başarılı',wx.OK|wx.ICON_INFORMATION)
        except Exception as e:
            gnclSQL.hata(e)
class ogrenciOlaylari(wx.Frame):
    def __init__(self,parent,title):
        super(ogrenciOlaylari,self).__init__(parent,title=title,size=(750,485))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        yuzey = wx.Panel(self)
        self.silP = wx.Panel(yuzey)
        self.ekleP = wx.Panel(yuzey)
        silDiz = wx.GridBagSizer(0,0)
        ekleDiz = wx.GridBagSizer(0,0)

        geri = wx.Button(yuzey,label='Geri')
        geri.SetPosition((10,10))
        geri.Bind(wx.EVT_BUTTON,self.geriGit)

        bos = wx.RadioButton(yuzey,110,label='BOŞ',style=wx.RB_GROUP)
        ogretmenEkle = wx.RadioButton(yuzey,111,label='Ekle')
        ogretmenSil = wx.RadioButton(yuzey,112,label='Sil')
        ogretmenEkle.Bind(wx.EVT_RADIOBUTTON,self.ekleSilGecis)
        ogretmenSil.Bind(wx.EVT_RADIOBUTTON,self.ekleSilGecis)
        bos.Hide()
        ogretmenEkle.SetPosition((120,15))
        ogretmenSil.SetPosition((170,15))
        self.silP.SetPosition((20,67))
        self.ekleP.SetPosition((20,67))

                #----------------Ekleme işlemleri __BAŞ__
        ogrnciBlrtciYazi = wx.StaticText(self.ekleP,label='Öğrenci Belirteci : ')
        ekleDiz.Add(ogrnciBlrtciYazi,pos=(0,0),flag=wx.ALL,border=5)
        self.ogrnciBlrtci = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrnciBlrtci,pos=(0,1),span=(1,2),flag=wx.ALL,border=5)

        ogrnciTCYazi = wx.StaticText(self.ekleP,label='Öğrencinin Kimlik Numarası(TC) : ')
        ekleDiz.Add(ogrnciTCYazi,pos=(1,0),flag=wx.ALL,border=5)
        self.ogrnciTC = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrnciTC,pos=(1,1),span=(1,2),flag=wx.ALL,border=5)

        ogrnciADYazi = wx.StaticText(self.ekleP,label='Ad : ')
        ekleDiz.Add(ogrnciADYazi,pos=(2,0),flag=wx.ALL,border=5)
        self.ogrnciAD = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrnciAD,pos=(2,1),span=(1,2),flag=wx.ALL,border=5)

        ogrnciSoyadYazi = wx.StaticText(self.ekleP,label='Soyad : ')
        ekleDiz.Add(ogrnciSoyadYazi,pos=(3,0),flag=wx.ALL,border=5)
        self.ogrnciSoyad = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrnciSoyad,pos=(3,1),span=(1,2),flag=wx.ALL,border=5)

        blm = ['BIO','FIZ','KIM','BIL','ELEK','MAK','OMT','OEM','OM']
        blmBlrtcYazi = wx.StaticText(self.ekleP,label='Bulunacağı Bölümün Belirteci : ')
        ekleDiz.Add(blmBlrtcYazi,pos=(4,0),flag=wx.ALL,border=5)
        self.blmBlrtc = wx.Choice(self.ekleP,choices=blm)
        ekleDiz.Add(self.blmBlrtc,pos=(4,1),span=(1,2),flag=wx.ALL,border=5)

        cinsiyetYazi = wx.StaticText(self.ekleP,label='Cinsiyet : ')
        ekleDiz.Add(cinsiyetYazi,pos=(5,0),flag=wx.ALL,border=5)
        self.cinsiyet = wx.Choice(self.ekleP, choices=('KADIN','ERKEK'))
        ekleDiz.Add(self.cinsiyet,pos=(5,1),span=(1,2),flag=wx.ALL,border=5)

        aktsYazi = wx.StaticText(self.ekleP,label='AKTS : ')
        ekleDiz.Add(aktsYazi,pos=(6,0),flag=wx.ALL,border=5)
        self.akts = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.akts,pos=(6,1),span=(1,2),flag=wx.ALL,border=5)

        self.normalOgretim = wx.RadioButton(self.ekleP,200,label='Normal Öğretim',style=wx.RB_GROUP)
        self.ikinciOgretim = wx.RadioButton(self.ekleP,201,label='İkinci Öğretim')
        ekleDiz.Add(self.normalOgretim,pos=(7,0),flag=wx.ALL,border=5)
        ekleDiz.Add(self.ikinciOgretim,pos=(7,1),flag=wx.ALL,border=5)

        self.doktora = wx.RadioButton(self.ekleP,200,label='Doktora',style=wx.RB_GROUP)
        self.yuksek = wx.RadioButton(self.ekleP,201,label='Yüksek Lisans')
        ekleDiz.Add(self.doktora,pos=(9,0),flag=wx.ALL,border=5)
        ekleDiz.Add(self.yuksek,pos=(9,1),flag=wx.ALL,border=5)        

        dgmTrhYazi = wx.StaticText(self.ekleP,label='Doğum Tarihi : ')
        ekleDiz.Add(dgmTrhYazi,pos=(0,8),flag=wx.ALL,border=5)
        self.dgmTrh = wx.adv.CalendarCtrl(self.ekleP,10,wx.DateTime.Now())
        ekleDiz.Add(self.dgmTrh,pos=(0,9),span=(5,5),flag=wx.ALL,border=5)

        kyTrhYazi = wx.StaticText(self.ekleP,label='Kayıt Tarihi : ')
        ekleDiz.Add(kyTrhYazi,pos=(5,8),flag=wx.ALL,border=5)
        self.kyTrh = wx.adv.CalendarCtrl(self.ekleP,11,wx.DateTime.Now())
        ekleDiz.Add(self.kyTrh,pos=(5,9),span=(5,5),flag=wx.ALL,border=5)

        self.dugmeTemizle = wx.Button(self.ekleP,label='Temizle')
        ekleDiz.Add(self.dugmeTemizle,pos=(10,0),flag=wx.ALL,border=5)
        self.dugmeTemizle.Bind(wx.EVT_BUTTON,self.temizle)

        self.dugmeEkle = wx.Button(self.ekleP,label='Ekle')
        ekleDiz.Add(self.dugmeEkle,pos=(10,1),flag=wx.ALL,border=5)
        self.dugmeEkle.Bind(wx.EVT_BUTTON,self.ogrnciEkle)
                #----------------Ekleme işlemleri __SON__

                #----------------Silme işlemleri __BAŞ__
        sil_ogrnciBlrtciYazi = wx.StaticText(self.silP,label='Öğrenci Belirteci : ')
        silDiz.Add(sil_ogrnciBlrtciYazi,pos=(0,0),flag=wx.ALL,border=5)
        self.sil_ogrnciBlrtci = wx.TextCtrl(self.silP)
        silDiz.Add(self.sil_ogrnciBlrtci,pos=(0,1),span=(1,2),flag=wx.ALL,border=5)

        sil_ogrnciTCYazi = wx.StaticText(self.silP,label='Öğrencinin Kimlik Numarası(TC) : ')
        silDiz.Add(sil_ogrnciTCYazi,pos=(1,0),flag=wx.ALL,border=5)
        self.sil_ogrnciTC = wx.TextCtrl(self.silP)
        silDiz.Add(self.sil_ogrnciTC,pos=(1,1),span=(1,2),flag=wx.ALL,border=5)

        self.dugmeTemizle = wx.Button(self.silP,label='Temizle')
        silDiz.Add(self.dugmeTemizle,pos=(3,0),flag=wx.ALL,border=5)
        self.dugmeTemizle.Bind(wx.EVT_BUTTON,self.temizle2)

        self.dugmeEkle = wx.Button(self.silP,label='Sil')
        silDiz.Add(self.dugmeEkle,pos=(3,1),flag=wx.ALL,border=5)
        self.dugmeEkle.Bind(wx.EVT_BUTTON,self.ogrnciSil)
        
                #----------------Silme işlemleri __SON__


        self.silP.Hide()
        self.ekleP.Hide()
        self.silP.SetSizerAndFit(silDiz)
        self.ekleP.SetSizerAndFit(ekleDiz)
    def ekleSilGecis(self,event):
        deger = event.GetEventObject()
        if deger.GetLabel() in ['sil','Sil']:
            self.ekleP.Hide()
            self.silP.Show()
        else:
            self.silP.Hide()
            self.ekleP.Show()
    def geriGit(self,event):
        self.Destroy()
    def temizle(self,event):
        self.ogrnciBlrtci.SetValue("")
        self.ogrnciTC.SetValue("")
        self.ogrnciAD.SetValue("")
        self.ogrnciSoyad.SetValue("")
        self.akts.SetValue("")
    def temizle2(self,event):
        self.sil_ogrnciBlrtci.SetValue("")
        self.sil_ogrnciTC.SetValue("")
    def ogrnciSil(self,event):
        ogrenciSilSQL=sqlIslem()
        self.silOgrnciBlrtc = self.sil_ogrnciBlrtci.GetValue()
        self.silOgrnciTc = self.sil_ogrnciTC.GetValue()
        ogrenciSilSQL.ogrnciSilmeIslemi(self.silOgrnciBlrtc,self.silOgrnciTc)
        self.sil_ogrnciBlrtci.SetValue("")
        self.sil_ogrnciTC.SetValue("")
    def ogrnciEkle(self,event):
        ogrnciEkleSQL=sqlIslem()
        self.blm_ = self.blmBlrtc.GetSelection()
        self.cnsyt_ = self.cinsiyet.GetSelection()

        self.doktora_= self.doktora.GetValue()
        self.yuksek_ = self.ikinciOgretim.GetValue()
        print(self.doktora_)

        self.ogrenci_belirtec = self.ogrnciBlrtci.GetValue()
        self.ogrenci_tc = self.ogrnciTC.GetValue()
        self.ogrenci_ad = self.ogrnciAD.GetValue()
        self.ogrenci_soyad = self.ogrnciSoyad.GetValue()
        self.blm = self.blmBlrtc.GetString(self.blm_)
        self.cnsyt = self.cinsiyet.GetString(self.cnsyt_)
        self.kyt_tarihi = self.kyTrh.GetDate()
        self.dgm_tarihi = self.dgmTrh.GetDate()
        self.dgm_tarihi = self.dgm_tarihi.FormatISODate()
        self.kyt_tarihi = self.kyt_tarihi.FormatISODate()
        self.akts_ = self.akts.GetValue()
        if self.doktora_ is True:
            self.a= 0
            print(self.a)
            if self.ikinciOgretim is True:
                self.i = 1
                ogrnciEkleSQL.ogrnciEklemeIslemi(self.ogrenci_belirtec,self.ogrenci_tc,self.ogrenci_ad,self.ogrenci_soyad,self.dgm_tarihi,self.kyt_tarihi,self.blm,self.cnsyt,self.akts_,self.i,self.a)
            else:
                self.n = 0
                ogrnciEkleSQL.ogrnciEklemeIslemi(self.ogrenci_belirtec,self.ogrenci_tc,self.ogrenci_ad,self.ogrenci_soyad,self.dgm_tarihi,self.kyt_tarihi,self.blm,self.cnsyt,self.akts_,self.n,self.a)
                
        else: 
            self.y = 1
            print(self.y)
            if self.ikinciOgretim is True:
                self.i = 1
                print(self.i)
                ogrnciEkleSQL.ogrnciEklemeIslemi(self.ogrenci_belirtec,self.ogrenci_tc,self.ogrenci_ad,self.ogrenci_soyad,self.dgm_tarihi,self.kyt_tarihi,self.blm,self.cnsyt,self.akts_,self.i,self.y)
            else:
                self.n = 0
                print(self.n)
                ogrnciEkleSQL.ogrnciEklemeIslemi(self.ogrenci_belirtec,self.ogrenci_tc,self.ogrenci_ad,self.ogrenci_soyad,self.dgm_tarihi,self.kyt_tarihi,self.blm,self.cnsyt,self.akts_,self.n,self.y)
class ogretmenOlaylari(wx.Frame):
    def __init__(self,parent,title):
        super(ogretmenOlaylari,self).__init__(parent,title=title,size=(750,475))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        yuzey = wx.Panel(self)
        self.silP = wx.Panel(yuzey)
        self.ekleP = wx.Panel(yuzey)
        silDiz = wx.GridBagSizer(0,0)
        ekleDiz = wx.GridBagSizer(0,0)

        geri = wx.Button(yuzey,label='Geri')
        geri.SetPosition((10,10))
        geri.Bind(wx.EVT_BUTTON,self.geriGit)

        bos = wx.RadioButton(yuzey,110,label='BOŞ',style=wx.RB_GROUP)
        ogretmenEkle = wx.RadioButton(yuzey,111,label='Ekle')
        ogretmenSil = wx.RadioButton(yuzey,112,label='Sil')
        ogretmenEkle.Bind(wx.EVT_RADIOBUTTON,self.ekleSilGecis)
        ogretmenSil.Bind(wx.EVT_RADIOBUTTON,self.ekleSilGecis)
        bos.Hide()
        ogretmenEkle.SetPosition((120,15))
        ogretmenSil.SetPosition((170,15))
        self.silP.SetPosition((20,67))
        self.ekleP.SetPosition((20,67))

                    #--------------------Ekleme işlemi __BAŞ__
        ogretmenBelirtecYazi = wx.StaticText(self.ekleP,label='Öğretmen Belirteci : ')
        ekleDiz.Add(ogretmenBelirtecYazi,pos=(0,0),flag=wx.ALL,border=5)
        self.ogrtmnBlrtc = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrtmnBlrtc,pos=(0,1),span=(1,2),flag=wx.ALL,border=5)

        ogrtmnTCyazi= wx.StaticText(self.ekleP,label='Öğretmen Kimlik Numarası(TC) : ')
        ekleDiz.Add(ogrtmnTCyazi,pos=(1,0),flag=wx.ALL,border=5)
        self.ogrtmnTC = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrtmnTC,pos=(1,1),span=(1,2),flag=wx.ALL,border=5)

        ogrtmnADYazi = wx.StaticText(self.ekleP,label='Ad : ')
        ekleDiz.Add(ogrtmnADYazi,pos=(2,0),flag=wx.ALL,border=5)
        self.ogrtmnAD = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrtmnAD,pos=(2,1),span=(1,2),flag=wx.ALL,border=5)

        ogrtmnSADYazi = wx.StaticText(self.ekleP,label='Soyad : ')
        ekleDiz.Add(ogrtmnSADYazi,pos=(3,0),flag=wx.ALL,border=5)
        self.ogrtmnSAD = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.ogrtmnSAD,pos=(3,1),span=(1,2),flag=wx.ALL,border=5)

        blm = ['BIO','FIZ','KIM','BIL','ELEK','MAK','OMT','OEM','OM']
        blmBlrtcYazi = wx.StaticText(self.ekleP,label='Bulunacağı Bölümün Belirteci : ')
        ekleDiz.Add(blmBlrtcYazi,pos=(4,0),flag=wx.ALL,border=5)
        self.blmBlrtc = wx.Choice(self.ekleP,choices=blm)
        ekleDiz.Add(self.blmBlrtc,pos=(4,1),span=(1,2),flag=wx.ALL,border=5)

        cinsiyetYazi = wx.StaticText(self.ekleP,label='Cinsiyet : ')
        ekleDiz.Add(cinsiyetYazi,pos=(5,0),flag=wx.ALL,border=5)
        self.cinsiyet = wx.Choice(self.ekleP, choices=('KADIN','ERKEK'))
        ekleDiz.Add(self.cinsiyet,pos=(5,1),span=(1,2),flag=wx.ALL,border=5)

        dgmTrhYazi = wx.StaticText(self.ekleP,label='Doğum Tarihi : ')
        ekleDiz.Add(dgmTrhYazi,pos=(0,8),flag=wx.ALL,border=5)
        self.dgmTrh = wx.adv.CalendarCtrl(self.ekleP,10,wx.DateTime.Now())
        ekleDiz.Add(self.dgmTrh,pos=(0,9),span=(5,5),flag=wx.ALL,border=5)

        kyTrhYazi = wx.StaticText(self.ekleP,label='Kayıt Tarihi : ')
        ekleDiz.Add(kyTrhYazi,pos=(5,8),flag=wx.ALL,border=5)
        self.kyTrh = wx.adv.CalendarCtrl(self.ekleP,11,wx.DateTime.Now())
        ekleDiz.Add(self.kyTrh,pos=(5,9),span=(5,5),flag=wx.ALL,border=5)

        self.dugmeTemizle = wx.Button(self.ekleP,label='Temizle')
        ekleDiz.Add(self.dugmeTemizle,pos=(7,0),flag=wx.ALL,border=5)
        self.dugmeTemizle.Bind(wx.EVT_BUTTON,self.temizle)

        self.dugmeEkle = wx.Button(self.ekleP,label='Ekle')
        ekleDiz.Add(self.dugmeEkle,pos=(7,1),flag=wx.ALL,border=5)
        self.dugmeEkle.Bind(wx.EVT_BUTTON,self.ogrtmnEkle)
                    #--------------------Ekleme işlemi __SON__
                    
                    #-------------------Silme işlemleri __BAŞ__

        sil_ogtmnBlrtcYazi = wx.StaticText(self.silP,label='Öğretmenin Belirteci : ')
        silDiz.Add(sil_ogtmnBlrtcYazi,pos=(0,0),flag=wx.ALL,border=5)
        self.sil_ogrtmnBlrtc = wx.TextCtrl(self.silP)
        silDiz.Add(self.sil_ogrtmnBlrtc,pos=(0,1),span=(1,2),flag=wx.ALL,border=5)

        sil_ogrtmnTCYazi= wx.StaticText(self.silP,label='Öğretmenin Kimlik Numarası(TC) : ')
        silDiz.Add(sil_ogrtmnTCYazi,pos=(1,0),flag=wx.ALL,border=5)
        self.sil_ogrtmnTC = wx.TextCtrl(self.silP)
        silDiz.Add(self.sil_ogrtmnTC,pos=(1,1),span=(1,2),flag=wx.ALL,border=5)

        self.dugmeTemizle2 = wx.Button(self.silP,label='Temizle')
        silDiz.Add(self.dugmeTemizle2,pos=(2,1),flag=wx.ALL,border=5)
        self.dugmeTemizle2.Bind(wx.EVT_BUTTON,self.temizle2)

        self.dugmeSil = wx.Button(self.silP,label='Sil')
        silDiz.Add(self.dugmeSil,pos=(2,2),flag=wx.ALL,border=5)
        self.dugmeSil.Bind(wx.EVT_BUTTON,self.ogrtmnSil)
                    #-------------------Silme işlemleri __SON__


        self.silP.Hide()
        self.ekleP.Hide()
        self.silP.SetSizerAndFit(silDiz)
        self.ekleP.SetSizerAndFit(ekleDiz)
    def geriGit(self,event):
        self.Destroy()
    def ekleSilGecis(self,event):
        deger = event.GetEventObject()
        if deger.GetLabel() in ['sil','Sil']:
            self.ekleP.Hide()
            self.silP.Show()
        else:
            self.silP.Hide()
            self.ekleP.Show()
    def temizle(self,event):
        self.ogrtmnBlrtc.SetValue("")
        self.ogrtmnTC.SetValue("")
        self.ogrtmnAD.SetValue("")
        self.ogrtmnSAD.SetValue("")
    def temizle2(self,event):
        self.sil_ogrtmnBlrtc.SetValue("")
        self.sil_ogrtmnTC.SetValue("")
    def ogrtmnEkle(self,event):
        ogrtmnEkleSQL = sqlIslem()
        self.blmINDEX = self.blmBlrtc.GetSelection()
        self.cnsytINDEX = self.cinsiyet.GetSelection()
        self.ogrtmnNO = self.ogrtmnBlrtc.GetValue()
        self.ogrtmnTC = self.ogrtmnTC.GetValue()
        self.ogrtmnIsim = self.ogrtmnAD.GetValue()
        self.ogrtmnSoyad = self.ogrtmnSAD.GetValue()
        self.blm = self.blmBlrtc.GetString(self.blmINDEX)
        self.cnsyt = self.cinsiyet.GetString(self.cnsytINDEX)
        self.kyTARIH = self.kyTrh.GetDate()
        self.dgmTARIH = self.dgmTrh.GetDate()
        self.dgmTARIH = self.dgmTARIH.FormatISODate()
        self.kyTARIH = self.kyTARIH.FormatISODate()

        ogrtmnEkleSQL.ogrtmnEklemeIslemi(self.ogrtmnNO,self.ogrtmnTC,self.ogrtmnIsim,self.ogrtmnSoyad,self.blm,self.cnsyt,self.kyTARIH,self.dgmTARIH)

        self.ogrtmnBlrtc.SetValue("")
        self.ogrtmnTC.SetValue("")
        self.ogrtmnAD.SetValue("")
        self.ogrtmnSAD.SetValue("")
    def ogrtmnSil(self,olay):
        ogrtmnSilSQL=sqlIslem()
        self.sil_ogrtmnBlrtci = self.sil_ogrtmnBlrtc.GetValue()
        self.sil_ogrtmnTCsi = self.sil_ogrtmnTC.GetValue()
        ogrtmnSilSQL.ogrtmnSilmeIslemi(self.sil_ogrtmnBlrtci,self.sil_ogrtmnTCsi)
        self.sil_ogrtmnBlrtc.SetValue("")
        self.sil_ogrtmnTC.SetValue("")
class dersOlaylari(wx.Frame):
    def __init__(self,parent,title):
        super(dersOlaylari,self).__init__(parent,title=title,size=(650,350))
        self.Asikar()
        self.Centre()
        self.Show()
    def Asikar(self):
        yuzey = wx.Panel(self)
        self.silP = wx.Panel(yuzey)
        self.ekleP = wx.Panel(yuzey)
        silDiz = wx.GridBagSizer(0,0)
        ekleDiz = wx.GridBagSizer(0,0)

        geri = wx.Button(yuzey,label='Geri')
        geri.SetPosition((10,10))
        geri.Bind(wx.EVT_BUTTON,self.geriGit)
        
        bos = wx.RadioButton(yuzey,110,label='BOŞ',style=wx.RB_GROUP)
        bos.Hide()
        dersEkle = wx.RadioButton(yuzey,111,label='Ekle')
        dersSil = wx.RadioButton(yuzey,112,label='Sil')
        dersEkle.Bind(wx.EVT_RADIOBUTTON,self.ekleSilGecis)
        dersSil.Bind(wx.EVT_RADIOBUTTON,self.ekleSilGecis)
        
        dersEkle.SetPosition((120,15))
        dersSil.SetPosition((170,15))
        self.silP.SetPosition((20,67))
        self.ekleP.SetPosition((20,67))

                
                            #-----------------Ekleme için gereken bileşenler   __BAŞ__
        dersKodYazi = wx.StaticText(self.ekleP,label='Dersin Belirteci : ')
        ekleDiz.Add(dersKodYazi,pos=(0,0),flag=wx.EXPAND|wx.ALL,border=5)
        self.dersKod = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.dersKod,pos=(0,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        dersAdYazi = wx.StaticText(self.ekleP,label='Dersin Adı : ')
        ekleDiz.Add(dersAdYazi,pos=(1,0),flag=wx.EXPAND|wx.ALL,border=5)
        self.dersAd = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.dersAd,pos=(1,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        bolumKodYazi = wx.StaticText(self.ekleP,label='Dersin bölüm belirteci : ')
        ekleDiz.Add(bolumKodYazi,pos=(2,0),flag=wx.EXPAND|wx.ALL,border=5)
        self.bolumKod = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.bolumKod,pos=(2,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        saatYazi = wx.StaticText(self.ekleP,label='Dersin Saati : ')
        ekleDiz.Add(saatYazi,pos=(3,0),flag=wx.EXPAND|wx.ALL,border=5)
        self.saati = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.saati,pos=(3,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        sinifYazi = wx.StaticText(self.ekleP,label='Dersin Sınıfı : ')
        ekleDiz.Add(sinifYazi,pos=(4,0),flag=wx.EXPAND|wx.ALL,border=5)
        self.sinifi = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.sinifi,pos=(4,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        teoriYazi = wx.StaticText(self.ekleP,label='Teori : ')
        ekleDiz.Add(teoriYazi,pos=(0,8),flag=wx.EXPAND|wx.ALL,border=5)
        self.teori = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.teori,pos=(0,9),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        uygulamaYazi = wx.StaticText(self.ekleP,label='Uygulama : ')
        ekleDiz.Add(uygulamaYazi,pos=(1,8),flag=wx.EXPAND|wx.ALL,border=5)
        self.uygulama = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.uygulama,pos=(1,9),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        krediYazi = wx.StaticText(self.ekleP,label='Kredi : ')
        ekleDiz.Add(krediYazi,pos=(2,8),flag=wx.EXPAND|wx.ALL,border=5)
        self.kredi = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.kredi,pos=(2,9),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        aktsYazi = wx.StaticText(self.ekleP,label='AKTS : ')
        ekleDiz.Add(aktsYazi,pos=(3,8),flag=wx.EXPAND|wx.ALL,border=5)
        self.akts = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.akts,pos=(3,9),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        gunYazi = wx.StaticText(self.ekleP,label='Dersin Günü : ')
        ekleDiz.Add(gunYazi,pos=(4,8),flag=wx.EXPAND|wx.ALL,border=5)
        self.gun = wx.TextCtrl(self.ekleP)
        ekleDiz.Add(self.gun,pos=(4,9),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)

        self.dugmeEkle = wx.Button(self.ekleP,label='Ekle')
        ekleDiz.Add(self.dugmeEkle,pos=(5,8),flag=wx.ALL,border=5)
        self.dugmeEkle.Bind(wx.EVT_BUTTON,self.dersEkle)

        self.dugmeTemizle = wx.Button(self.ekleP,label='Temizle')
        ekleDiz.Add(self.dugmeTemizle,pos=(5,9),flag=wx.ALL,border=5)
        self.dugmeTemizle.Bind(wx.EVT_BUTTON,self.temizle)
        
                            #-----------------Ekleme için gereken bileşenler __SON__
                            
                            
                            #-----------------Silme İşlemi için gereken bileşenler __BAŞ__
        dersBelirYazi = wx.StaticText(self.silP,label='Silinecek Dersin Belirteci : ')
        silDiz.Add(dersBelirYazi,pos=(0,0),flag=wx.EXPAND|wx.ALL,border=5)
        self.sil_dersBelir = wx.TextCtrl(self.silP)
        silDiz.Add(self.sil_dersBelir,pos=(0,1),span=(1,2),flag=wx.EXPAND|wx.ALL,border=5)
        
        dugmeSil = wx.Button(self.silP,label='Sil')
        dugmeSil.Bind(wx.EVT_BUTTON,self.dersSil)
        silDiz.Add(dugmeSil,pos=(2,1),flag=wx.ALL,border=5)
                            #-----------------Silme İşlemi için gereken bileşenler __SON__
                    
        self.silP.Hide()
        self.ekleP.Hide()
        self.silP.SetSizerAndFit(silDiz)
        self.ekleP.SetSizerAndFit(ekleDiz)

    def geriGit(self,event):
        self.Destroy()
    def ekleSilGecis(self,event):
        deger = event.GetEventObject()
        if deger.GetLabel() in ['sil','Sil']:
            self.ekleP.Hide()
            self.silP.Show()
        else:
            self.silP.Hide()
            self.ekleP.Show()
    def dersSil(self,event):
        silCalistir = sqlIslem()
        self.dBlrtc = self.sil_dersBelir.GetValue()
        silCalistir.dersSilmeIslemi(self.dBlrtc)
        self.sil_dersBelir.SetValue("")
        

    def dersEkle(self,event):
        ekleCalistir=sqlIslem()
        self.dKOD = self.dersKod.GetValue()
        self.bKOD = self.bolumKod.GetValue()
        self.st = self.saati.GetValue()
        self.snf = self.sinifi.GetValue()
        self.dAD = self.dersAd.GetValue()
        self.tri = self.teori.GetValue()
        self.ugylm = self.uygulama.GetValue()
        self.krd = self.kredi.GetValue()
        self.kts = self.akts.GetValue()
        self.dersGun = self.gun.GetValue()
        ekleCalistir.dersEklemeIslemi(self.dKOD,self.dAD,self.st,self.snf,self.dersGun,self.tri,self.ugylm,self.krd,self.kts,self.bKOD)
        self.dersKod.SetValue("")
        self.bolumKod.SetValue("")
        self.saati.SetValue("")
        self.sinifi.SetValue("")
        self.dersAd.SetValue("")
        self.teori.SetValue("")
        self.uygulama.SetValue("")
        self.kredi.SetValue("")
        self.akts.SetValue("")
        self.gun.SetValue("")
    def temizle(self,event):
        self.dersKod.SetValue("")
        self.bolumKod.SetValue("")
        self.saati.SetValue("")
        self.sinifi.SetValue("")
        self.dersAd.SetValue("")
        self.teori.SetValue("")
        self.uygulama.SetValue("")
        self.kredi.SetValue("")
        self.akts.SetValue("")
        self.gun.SetValue("")
class ogretmenDersSec(wx.Frame):
    def __init__(self,parent,title):
        super(ogretmenDersSec,self).__init__(parent,title=title,size=(800,600))
        self.Asikar()
        self.Centre()
        self.Show()

    def Asikar(self):
        self.yuzey = wx.Panel(self)
        diz = wx.GridBagSizer(0,0)

        cikisDugme = wx.Button(self.yuzey,label='Çık')
        diz.Add(cikisDugme,pos=(0,0),span=(1,2),flag=wx.EXPAND|wx.ALL,border=7)
        cikisDugme.Bind(wx.EVT_BUTTON,self.cikis)

        ogrtmn_BelirtecYazi = wx.StaticText(self.yuzey,label='Öğretmen Seç') 
        diz.Add(ogrtmn_BelirtecYazi,pos=(2,1),flag=wx.ALL,border=5)

        sayac = 0
        ogretmenSQL = sqlIslem()
        cursor = ogretmenSQL.baglan.cursor()
        cursor.execute("select ad1 from ogretmenTB")
        satir = cursor.fetchone()
        while satir:
            sayac=sayac+1
            satir = cursor.fetchone()
        liste = ['']*sayac
        liste2 = ['']*sayac
        cursor.close()
        sayac = 0
        cursor = ogretmenSQL.baglan.cursor()
        cursor.execute("select ad1,soyad,bolumBelirtec from ogretmenTB")
        satir = cursor.fetchone()
        print(satir)
        while satir:
            liste[sayac] = str(satir[sayac]) + ' ' + str(satir[sayac+1])
            liste2[sayac] = str(satir[sayac+2])
            satir = cursor.fetchone()
            print(satir)

        self.ogrtmn_Sec = wx.Choice(self.yuzey,choices=liste)
        diz.Add(self.ogrtmn_Sec,pos=(2,2),flag=wx.ALL,border=5)
        self.ogrtmn_Sec.Bind(wx.EVT_CHOICE,self.ogretmenSEC)

        

        self.yuzey.SetSizerAndFit(diz)
    def cikis(self,event):
        self.Destroy()
    def ogretmenSEC(self,event):
        a = self.ogrtmn_Sec.GetSelection()
        print(a)

        

class sqlIslem():
    def __init__(self):
        self.baglan = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};Server=DESKTOP-R71L9L2\SQLEXPRESS;Database=FenBE;Trusted_Connection=yes;')
    def deneme(self):
        cursor = self.baglan.cursor()
        cursor.execute("select @@version;")
        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()
    def dersEklemeIslemi(self,drsBlrtci,drsAdi,sti,snfi,dGun,tri,uyglma,krdi,aktsSi,blmBlrtci):
        cursor = self.baglan.cursor()
        try:    
            cursor.execute("exec udSP_dersEkleme ?,?,?,?,?,?,?,?,?,?",(drsBlrtci,drsAdi,sti,snfi,dGun,tri,uyglma,krdi,aktsSi,blmBlrtci))
            self.baglan.commit()
        except Exception as e:
            self.hata(e)
    def dersSilmeIslemi(self,dBelirteci):
        cursor = self.baglan.cursor()
        try:
            cursor.execute("exec udSP_dersSilme ?",(dBelirteci))
            self.baglan.commit()
        except Exception as e:
            self.hata(e)
    def ogrtmnEklemeIslemi(self,ogrtmnBlrtc,ogrtmTC,ogrtmnAD,ogrtmnSAd,ogrtmnBLM,cnsyt,kyYrhi,dgmTrhi):
        cursor = self.baglan.cursor()
        try:
            cursor.execute("insert into FenBE.dbo.ogretmenTB(ogretmenBelirtec,TC,ad1,soyad,dogumTarihi,kayiTarihi,bolumBelirtec,cinsiyet) values (?,?,?,?,?,?,?,?)",(ogrtmnBlrtc,ogrtmTC,ogrtmnAD,ogrtmnSAd,dgmTrhi,kyYrhi,ogrtmnBLM,cnsyt))
            self.baglan.commit()
        except Exception as e:
            self.hata(e)
    def ogrtmnSilmeIslemi(self,ogrtmnBlrtc,ogrtmnTC):
        cursor = self.baglan.cursor()
        try:
            cursor.execute("delete from FenBE.dbo.ogretmenTB where ogretmenBelirtec = ? and TC = ?",(ogrtmnBlrtc,ogrtmnTC))
            self.baglan.commit()
        except Exception as e:
            self.hata(e)
    def ogrnciEklemeIslemi(self,ogrnciBlrtc,ogrnciTC,ogrnciAD,ogrnciSAd,dgmTarihi,kytTarihi,ogrnciBLM,cnsyt,akts,ogretimDRM,dokYuk):
        cursor = self.baglan.cursor()
        try:
            cursor.execute("insert into FenBE.dbo.ogrenciTB(ogrenciBelirtec,TC,ad1,soyad,dogumTarihi,kayiTarihi,bolumBelirtec,cinsiyet,akts,ogretimDurumu,doktoraYuksek) values(?,?,?,?,?,?,?,?,?,?,?)",(ogrnciBlrtc,ogrnciTC,ogrnciAD,ogrnciSAd,dgmTarihi,kytTarihi,ogrnciBLM,cnsyt,akts,ogretimDRM,dokYuk))
            self.baglan.commit()
        except Exception as e:
            self.hata(e)
    def ogrnciSilmeIslemi(self,ogrnciBlrtc,ogrnciTc):
        cursor = self.baglan.cursor()
        try:
            cursor.execute("delete from FenBE.dbo.ogrenciTB where ogrenciBelirtec = ? and TC = ?",(ogrnciBlrtc,ogrnciTc))
            self.baglan.commit()
        except Exception as e:
            self.hata(e)
    def hata(self,e):
         wx.MessageBox('Hata : %s' %(e),'HATA',wx.OK|wx.ICON_INFORMATION)

def main():
    vtOdev=wx.App()
    kul_gir=kulGiris(None,title='Kullanıcı Girişi')
    #sql=sqlIslem()
    #sql.deneme()
    #sql.cursor.close()
    #sql.baglan.close()
    vtOdev.MainLoop()

if __name__=='__main__':
    main()

