from flask import (
    Flask,
    render_template,
    request,
    send_file
)

from audit import audit_website
from pdf_rapor import create_pdf

import os


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    sonuc = None
    hata = None

    if request.method == "POST":

        business_name = request.form.get(
            "business_name",
            ""
        ).strip()

        sector = request.form.get(
            "sector",
            ""
        ).strip()

        city = request.form.get(
            "city",
            ""
        ).strip()

        website = request.form.get(
            "website",
            ""
        ).strip()

        if not business_name:
            hata = "İşletme adı zorunludur."

        elif not sector:
            hata = "Sektör zorunludur."

        elif not city:
            hata = "Şehir zorunludur."

        elif not website:
            hata = "Web sitesi zorunludur."

        else:

            sonuc = audit_website(
                website,
                business_name,
                sector,
                city
            )

            if not sonuc.get("success"):
                hata = sonuc.get(
                    "error",
                    "Analiz sırasında hata oluştu."
                )

                sonuc = None

    return render_template(
        "index.html",
        sonuc=sonuc,
        hata=hata
    )


@app.route("/pdf", methods=["POST"])
def pdf():

    business_name = request.form.get(
        "business_name",
        ""
    ).strip()

    sector = request.form.get(
        "sector",
        ""
    ).strip()

    city = request.form.get(
        "city",
        ""
    ).strip()

    website = request.form.get(
        "website",
        ""
    ).strip()

    sonuc = audit_website(
        website,
        business_name,
        sector,
        city
    )

    if not sonuc.get("success"):

        return (
            sonuc.get(
                "error",
                "PDF oluşturulamadı."
            ),
            400
        )

    try:

        pdf_path = create_pdf(
            sonuc
        )

        if os.path.exists(pdf_path):

            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=(
                    "website_audit_raporu.pdf"
                )
            )

    except Exception as hata:

        print(
            "PDF HATASI:",
            hata
        )

        return (
            "PDF oluşturulurken hata oluştu: "
            + str(hata),
            500
        )

    return (
        "PDF dosyası oluşturulamadı.",
        500
    )


@app.route("/health")
def health():

    return {
        "status": "ok",
        "service": "LocalAI Website Audit",
        "version": "2.0"
    }


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )