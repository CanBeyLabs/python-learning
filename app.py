from flask import Flask, render_template, request, send_file

from audit import website_analiz_et

from pdf_generator import pdf_olustur


app = Flask("localai")


@app.route("/", methods=["GET", "POST"])
def ana_sayfa():

    sonuc = None

    if request.method == "POST":

        isletme_adi = request.form.get(
            "isletme_adi"
        )

        sektor = request.form.get(
            "sektor"
        )

        sehir = request.form.get(
            "sehir"
        )

        website = request.form.get(
            "website"
        )

        sonuc = website_analiz_et(
            website
        )

        sonuc["isletme_adi"] = isletme_adi
        sonuc["sektor"] = sektor
        sonuc["sehir"] = sehir

    return render_template(
        "index.html",
        sonuc=sonuc
    )


@app.route(
    "/pdf",
    methods=["POST"]
)
def pdf():

    isletme_adi = request.form.get(
        "isletme_adi"
    )

    sektor = request.form.get(
        "sektor"
    )

    sehir = request.form.get(
        "sehir"
    )

    website = request.form.get(
        "website"
    )

    sonuc = website_analiz_et(
        website
    )

    sonuc["isletme_adi"] = isletme_adi
    sonuc["sektor"] = sektor
    sonuc["sehir"] = sehir

    pdf_yolu = pdf_olustur(
        sonuc
    )

    return send_file(
        pdf_yolu,
        as_attachment=True
    )


app.run(
    debug=True
)