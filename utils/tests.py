import os
import base64
import requests

BASE_URL = 'http://localhost:5000'
# BASE_URL = 'https://pix-code.herokuapp.com'


def make_qr(qr_string, output=None):
    type_string, string = qr_string.split(',')
    path_to_save = "../media/qrcode"
    if output:
        path_to_save = output
    filename = "my_qrcode_pix.png"
    with open(os.path.join(f"{path_to_save}", filename), "wb") as qr:
        qr.write(base64.urlsafe_b64decode(string))


class Browser(object):

    def __init__(self):
        self.response = None
        self.headers = self.get_headers()
        self.session = requests.Session()

    def get_headers(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36"
        }
        return self.headers

    def send_request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 200:
            return response
        return None


class PixCodeAPI(Browser):

    def __init__(self):
        super().__init__()

    def generate_qr(self, **kwargs):
        data = kwargs
        self.response = self.send_request('POST', f"{BASE_URL}/api/v1/qrcode", json=data, headers=self.headers)
        return self.response


if __name__ == '__main__':
    api = PixCodeAPI()

    params = {
        "nome": "cleiton leonel creton",
        "city": "cariacica",
        "zipcode": "29148613",
        "location": "",
        "chave": "cleiton.leonel@gmail.com",
        "txid": "123",
        "info": "paga aê pow...nunca te pedi nada, mão de vaca...",
        "valor": 15.00
    }

    qrcode = api.generate_qr(**params)
    if qrcode.status_code == 200:
        print(qrcode.json())
        base64_qr = qrcode.json()['object']['base64qr']
        make_qr(base64_qr, output='')
