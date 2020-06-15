# github.com/echtr
from flask import Flask, render_template, request
import sqlite3
import datetime
app = Flask(__name__)


def yorum_yaz(tarih,isim, yorum):
	baglan = sqlite3.connect("veritabani.db")
	imlec = baglan.cursor()
	degiskenler = (tarih,isim, yorum)
	imlec.execute("INSERT INTO yorumlar(tarih,isim,yorum) VALUES(?,?,?)", degiskenler)
	baglan.commit()
	baglan.close()

@app.route("/", methods=["GET","POST"])
def index():
	yorumlar = []
	isimler = []
	tarihler = []
	anahtar = 0
	baglan = sqlite3.connect("veritabani.db")
	imlec = baglan.cursor()
	imlec.execute("SELECT * FROM yorumlar")
	yorum = imlec.fetchall()
	yorum = list(yorum)
	if anahtar == 0:
		for i in yorum:
			yorumlar.append(i[2])
			isimler.append(i[1])
			tarihler.append(i[0])
		anahtar = 1
	baglan.commit()
	baglan.close()
	if request.method == "POST":
		tarih = datetime.datetime.now()
		gun = tarih.strftime("%d")
		ay = tarih.strftime("%m")
		if len(gun) == 1:
			gun = str("0" + str(gun))
		if len(ay) == 1:
			ay = str("0" + str(ay))	
		tarih = str(gun + "." + ay + "." + tarih.strftime("%Y"))
		isim = request.form["isim"]
		yorum = request.form["yorum"]
		if ((isim == "") or (yorum == "")):
			print("boş request atıldı")
			return render_template("index.html",yorum_uzunluk=len(yorumlar),yorumlar = yorumlar, isimler = isimler, tarihler=tarihler)
		else:
			yorum_yaz(tarih,isim,yorum)
			return render_template("yonlendir.html",yorum_uzunluk=len(yorumlar),yorumlar = yorumlar, isimler = isimler, tarihler=tarihler)
	else:
		return render_template("index.html",yorum_uzunluk=len(yorumlar),yorumlar = yorumlar, isimler = isimler, tarihler=tarihler)
app.run(debug=True)
