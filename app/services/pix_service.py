import os
from decimal import Decimal, InvalidOperation
from flask import current_app
from werkzeug.utils import secure_filename
from app.core.pix import Pix
from app.db.crud.pix_crud import save_pix
from app.db.models.pix_model import PixModel
from app.utils.security import generate_secure_token


def set_pix_params(model, **kwargs):
    """Configura parâmetros do objeto Pix."""
    model.set_name_receiver(kwargs["full_name"])
    model.set_city_receiver(kwargs["city"])
    if kwargs["location"]:
        model.set_default_url_pix(kwargs["location"])
    model.set_key(kwargs["pix_key"])
    model.set_identification(kwargs["identification"])
    model.set_zipcode_receiver(kwargs["zip_code"])
    model.set_description(kwargs["description"])
    model.set_amount(kwargs["amount"])


def convert_form_data(form_data: dict) -> dict:
    """Converte dados do formulário para o formato necessário para gerar o PIX."""
    args = {}
    args["full_name"] = form_data.get("nome", "").strip()
    args["city"] = form_data.get("city", "").strip()

    # Ajuste: verificar se a chave é 'zipcode' ou 'zip_code'
    zip_code = form_data.get("zipcode", "").strip()  # ou 'zip_code'
    args["zip_code"] = "".join(filter(str.isdigit, zip_code))

    location = form_data.get("location", "").strip()
    args["location"] = location if location else None

    chave = form_data.get("chave", "").strip()
    args["pix_key"] = "".join(filter(str.isdigit, chave)) if "@" not in chave else chave

    args["identification"] = form_data.get("txid", "").strip()
    args["description"] = form_data.get("info", "").strip()

    # Parse seguro do valor
    amount = form_data.get("valor", "")
    try:
        if isinstance(amount, str):
            cleaned_amount = amount.split(" ")[-1].strip().replace(",", ".")
            args["amount"] = Decimal(cleaned_amount)
        else:
            args["amount"] = Decimal(amount)
    except (InvalidOperation, IndexError):
        args["amount"] = Decimal("0.0")

    return args


def process_pix_data(request, form_data, files=None):
    """Processa os dados do formulário e gera o PIX, QR Code e salva no banco."""

    # Conversão e preparação
    args = convert_form_data(form_data)
    pix = Pix()
    set_pix_params(pix, **args)

    result_data = {**form_data}  # Cópia segura dos dados

    brcode = pix.get_br_code()
    result_data["brcode"] = brcode

    # Logo padrão
    logo = os.path.join(current_app.config["LOGO_FOLDER"], "logo-pypix.png")

    # Se enviou arquivo, sobrescreve logo
    if files and "file" in files:
        file = files["file"]
        filename = secure_filename(file.filename)
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)
        logo = os.path.join(upload_folder, filename)
        file.save(logo)

    # Geração do QR Code
    qr_output = os.path.join(current_app.config["QR_FOLDER"], "qrcode.png")
    os.makedirs(os.path.dirname(qr_output), exist_ok=True)

    result_data["base64qr"] = pix.save_qrcode(
        output=qr_output,
        custom_logo=logo,
    )

    # Geração do token
    token = generate_secure_token()
    shared_link = f"{request.host_url}invoices/{token}"
    result_data["shared_link"] = shared_link

    # Criação do modelo para persistência
    pix_model = PixModel(
        full_name=pix.name_receiver,
        pix_key=pix.key,
        city=pix.city_receiver,
        zip_code=pix.zipcode_receiver,
        amount=pix.amount,
        description=pix.description,
        identification=pix.identification,
        location=pix.default_url_pix or "",
        br_code=brcode,
        base64_qr=result_data["base64qr"],
        hash_id=token,
    )

    # Persistência
    save_pix(pix_model)

    return {
        "result": True,
        "object": result_data,
        "message": "Ficou super fácil criar links de doação, pagamento e cobranças Pix!",
    }
