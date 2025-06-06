import logging

from app import create_app

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
