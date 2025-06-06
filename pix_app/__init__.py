import secrets
import tempfile
from os import getcwd, makedirs, path
from urllib.parse import quote_plus

from flask import Flask

from pix_app.api.routes import main
from pix_app.db.base import init_database

# Configurações
STATIC_PATH = "pix_app/static/media"
QR_FOLDER = f"{STATIC_PATH}/qrcode/"
LOGO_FOLDER = f"{STATIC_PATH}/img/"
DATABASE_DIR = "pix_app/data/"
BASE_DIR = getcwd()

# Criação de diretórios
for folder in [QR_FOLDER, DATABASE_DIR]:
    folder_path = path.join(BASE_DIR, folder)
    if not path.exists(folder_path):
        makedirs(folder_path)


def create_app(config_class="config.Config"):
    """Cria e configura a aplicação Flask."""

    app = Flask(__name__, template_folder="templates")
    app.config.update(
        {
            "DATABASE_PATH": DATABASE_DIR,
            "QR_FOLDER": QR_FOLDER,
            "LOGO_FOLDER": LOGO_FOLDER,
            "SECRET_KEY": secrets.token_hex(32),  # Chave mais longa
            "UPLOAD_FOLDER": tempfile.gettempdir(),
            "MAX_CONTENT_LENGTH": 16 * 1024 * 1024,  # 16MB max file size
        }
    )

    app.jinja_env.filters["quote_plus"] = lambda u: quote_plus(u)

    # Inicializa extensões
    init_database()

    # Registra blueprints
    app.register_blueprint(main)

    return app
