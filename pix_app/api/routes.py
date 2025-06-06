import json
import logging

from flask import Blueprint, redirect, render_template, request

from pix_app.db.crud.pix_crud import get_pix_by_hash, increment_pix_clicks
from pix_app.services.pix_service import process_pix_data

main = Blueprint("main", __name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@main.route("/")
def index():
    return redirect("/qrcode")


@main.route("/api/v1/qrcode", methods=["POST"])
def qrcode_api():
    try:
        # Parse JSON data
        if request.content_type == "application/json":
            form_data = request.get_json()
        else:
            form_data = json.loads(request.form["json"])

        files = request.files if hasattr(request, "files") else None
        result = process_pix_data(request, form_data, files)

        return result

    except ValueError as e:
        return {"result": False, "message": str(e)}, 400
    except Exception as e:
        logger.error(f"Erro na API: {str(e)}")
        return {"result": False, "message": "Erro interno do servidor"}, 500


@main.route("/qrcode", methods=["GET", "POST"])
def get_qrcode():
    if request.method == "POST":
        try:
            result = process_pix_data(
                request, request.form.to_dict(), files=request.files
            )
            return render_template("payment.html", result=result.get("object", {}))
        except ValueError as e:
            return render_template("index.html", error=str(e))
        except Exception as e:
            logger.error(f"Erro no QR code: {str(e)}")
            return render_template("index.html", error="Erro ao gerar QR code")

    return render_template("index.html")


@main.route("/invoices/<hash_id>")
def invoices(hash_id):
    try:
        # Buscar pelo hash_id usando SQLAlchemy ORM
        pix_obj = get_pix_by_hash(hash_id)

        if not pix_obj:
            return render_template("404.html"), 404

        # Incrementar contador de cliques
        increment_pix_clicks(pix_obj)

        result_dict = {
            "nome": pix_obj.full_name,
            "chave": pix_obj.pix_key,
            "city": pix_obj.city,
            "zipcode": pix_obj.zip_code,
            "txid": pix_obj.identification,
            "info": pix_obj.description,
            "valor": str(pix_obj.amount),
            "base64qr": pix_obj.base64_qr,
            "brcode": pix_obj.br_code,
            "shared_link": f"{request.host_url}invoices/{pix_obj.hash_id}",
            "clicks": pix_obj.clicks + 1,  # já incrementado
        }

        return render_template("payment.html", result=result_dict)

    except Exception as e:
        logger.error(f"Erro ao buscar invoice: {str(e)}")
        return render_template("404.html"), 404
