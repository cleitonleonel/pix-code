# _Pix-code_

<img src="https://github.com/cleitonleonel/pypix/blob/master/pypix.png?raw=true" alt="pypix" width="450"/>

Pix-code é baseado no projeto [Pix.ae](https://pix.ae/renatofrota@gmail.com), usando motor de um outro projeto meu chamado [Pypix](https://github.com/cleitonleonel/pypix.git).

![pix-code.gif](pix_app/static/media/img/pix-code.gif)

# Instalação e uso:

```shell
git clone https://github.com/cleitonleonel/pix-code.git
cd pix-code
poetry install
poetry run python app.py
```

# Consumindo a nossa api via Python:
```python
import os
import json
import requests


BASE_URL = 'https://pix-code.isolutionstech.com.br'  # 'http://localhost:5000'

data = {
    "nome": "cleiton leonel creton",
    "city": "cariacica",
    "zipcode": "29148613",
    "location": "",
    "chave": "cleiton.leonel@gmail.com",
    "txid": "123",
    "info": "paga aê pow...nunca te pedi nada, mão de vaca...",
    "valor": 15.00
}
logo = os.path.join('/home/cleiton/PyJobs/MeusProjetos/pypix/', 'pro_bots.png')  # Opcional

files = {
    'json': (None, json.dumps(data), 'application/json'),
}
if logo:
    files['file'] = (os.path.basename(logo), open(logo, 'rb'), 'application/octet-stream')

result = requests.post(url=f'{BASE_URL}/api/v1/qrcode', files=files)
if result.status_code == 200:
    print(result.json())
```

## Saída:
```json
    {"message": "Ficou super fácil criar links de doação, pagamento e cobranças Pix!",
    "object": {
        "base64qr": "data:image/png;base64,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",
        "brcode": "00020101021126980014br.gov.bcb.pix0124cleiton.leonel@gmail.com0248paga ae pow...nunca te pedi nada, mao de vaca...520400005303986540515.005802BR5921cleiton leonel creton6009cariacica6108291486136207050312363041C10",
        "chave": "cleiton.leonel@gmail.com",
        "city": "cariacica",
        "info": "paga aê pow...nunca te pedi nada, mão de vaca...",
        "location": "",
        "nome": "cleiton leonel creton",
        "shared_link": "https://pix-code.isolutionstech.com.br/invoices/dguGvVTc7T7VztQGGDqSu180fVfQGVhSjdJSqVwZouituHiRZ53lcf0vuF49se",
        "txid": "123",
        "valor": 15.0,
        "zipcode": "29148613"
    },
    "result": true
    }
```

# Consumindo a nossa api via Curl:

```shell
curl -i -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/home/cleiton/PyJobs/MeusProjetos/pypix/pro_bots.png" \
  -F "json={
    \"nome\": \"cleiton leonel creton\",
    \"city\": \"cariacica\",
    \"zipcode\": \"29148613\",
    \"location\": \"\",
    \"chave\": \"cleiton.leonel@gmail.com\",
    \"txid\": \"123\",
    \"info\": \"paga aê pow...nunca te pedi nada, mão de vaca...\",
    \"valor\": 15.00
  };type=application/json" \
  "https://pix-code.isolutionstech.com.br/api/v1/qrcode"
```

# Este projeto ajudou você?

Se esse projeto lhe ajudar de alguma forma, sinta-se livre para me pagar um café, kkkk...Basta apontar a câmera do seu celular para um dos qrcodes abaixo.

<img src="https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true" alt="QRCode Doação" width="250"/>

<img src="https://github.com/cleitonleonel/pypix/blob/master/artistic.gif?raw=true" alt="QRCode Doação" width="250"/>

# Author

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com