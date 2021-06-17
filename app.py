import secrets
import sqlite3
import random
from flask import Flask, request, redirect, render_template
from os import getcwd, path, makedirs
from api.pix import Pix
from decimal import Decimal

from urllib.parse import quote_plus

QR_FOLDER = 'media/qrcode/'
LOGO_FOLDER = 'static/media/img/'
DATABASE_DIR = 'data/'
BASE_DIR = getcwd()

if not path.exists(path.join(BASE_DIR, QR_FOLDER)):
    makedirs(path.join(BASE_DIR, QR_FOLDER))
    makedirs(path.join(BASE_DIR, DATABASE_DIR))

app = Flask(__name__, template_folder='templates')
app.config['QR_FOLDER'] = QR_FOLDER
app.config['LOGO_FOLDER'] = LOGO_FOLDER
app.config['SECRET_KEY'] = secrets.token_hex(16)

app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)

alpha_number = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_token():
    result = []
    count = 0
    while count < len(alpha_number):
        result.append(random.choice(alpha_number))
        count += 1
    return ''.join(result)


def set_pix_params(model, **kwargs):
    model.set_name_receiver(kwargs['full_name'])
    model.set_city_receiver(kwargs['city'])
    if kwargs['location']:
        model.set_default_url_pix(kwargs['location'])
    model.set_key(kwargs['pix_key'])
    model.set_identification(kwargs['identification'])
    model.set_zipcode_receiver(kwargs['zip_code'])
    model.set_description(kwargs['description'])
    model.set_amount(kwargs['amount'])


def get_db_connection():
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = sqlite3.Row
    return conn


cursor = get_db_connection()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pix (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        pix_key TEXT NOT NULL,
        city TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        amount FLOAT NOT NULL,
        description TEXT,
        identification TEXT NOT NULL,
        location TEXT,
        br_code TEXT NOT NULL,
        base64_qr TEXT NOT NULL,
        hash_id TEXT NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        clicks INTEGER NOT NULL DEFAULT 0
        )
""")


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/qrcode')


@app.route('/api/v1/qrcode', methods=['POST'])
def qrcode_api():
    conn = get_db_connection()
    if request.method == 'POST':
        result = request.get_json()
        args = {}
        args['full_name'] = result['nome']
        args['city'] = result['city']
        args['zip_code'] = ''.join(filter(str.isdigit, result['zipcode']))
        args['location'] = None
        if result['location'] != '':
            args['location'] = result['location']
        args['pix_key'] = ''.join(filter(str.isdigit, result['chave'])) \
            if '@' not in result['chave'] else result['chave']
        args['identification'] = result['txid']
        args['description'] = result['info']
        args['amount'] = Decimal(result['valor']if result['valor'] != '' else 0.0)

        pix = Pix()
        set_pix_params(pix, **args)
        result['brcode'] = pix.get_br_code()
        # base64qr = pix.save_qrcode('./qrcode.png')

        result['base64qr'] = pix.save_qrcode('./qrcode.png', color="black", box_size=7,
                                             border=1, custom_logo=path.join(LOGO_FOLDER, 'logo-pypix.png')
                                             )

        shared_link = request.host_url + 'invoices/' + generate_token()
        result['shared_link'] = shared_link

        conn.execute("""
        INSERT INTO Pix (
            full_name,
            pix_key,
            city,
            zip_code,
            amount,
            description,
            identification,
            location,
            br_code,
            base64_qr,
            hash_id
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (pix.name_receiver, pix.key, pix.city_receiver, pix.zipcode_receiver,
              pix.amount, pix.description, pix.identification, pix.default_url_pix if pix.default_url_pix else '',
              str(result['brcode']), str(result['base64qr']), shared_link.split('/')[-1]
              )
                     )

        conn.commit()
        conn.close()

        return {
            "result": True,
            "object": result,
            "message": "Ficou super fácil criar links de doação, pagamento e cobranças Pix!"
        }


@app.route('/qrcode', methods=['GET', 'POST'])
def get_qrcode():
    conn = get_db_connection()
    if request.method == 'POST':
        result = request.form.to_dict(flat=False)
        args = {}
        args['full_name'] = result['nome'][0]
        args['city'] = result['city'][0]
        args['zip_code'] = ''.join(filter(str.isdigit, result['zipcode'][0]))
        args['location'] = None
        if result['location'][0] != '':
            args['location'] = result['location'][0]
        args['pix_key'] = ''.join(filter(str.isdigit, result['chave'][0])) \
            if '@' not in result['chave'][0] else result['chave'][0]
        args['identification'] = result['txid'][0]
        args['description'] = result['info'][0]
        args['amount'] = Decimal(result['valor'][0].split(' ')[1].replace(',', '.')
                                 if result['valor'][0] != '' else 0.0
                                 )

        pix = Pix()
        set_pix_params(pix, **args)
        result['brcode'] = [pix.get_br_code()]
        # base64qr = pix.save_qrcode('./qrcode.png')

        result['base64qr'] = [pix.save_qrcode('./qrcode.png', color="black", box_size=7,
                                              border=1, custom_logo=path.join(LOGO_FOLDER, 'logo-pypix.png')
                                              )]

        shared_link = request.host_url + 'invoices/' + generate_token()
        result['shared_link'] = [shared_link]

        conn.execute("""
        INSERT INTO Pix (
            full_name,
            pix_key,
            city,
            zip_code,
            amount,
            description,
            identification,
            location,
            br_code,
            base64_qr,
            hash_id
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (pix.name_receiver, pix.key, pix.city_receiver, pix.zipcode_receiver,
              pix.amount, pix.description, pix.identification, pix.default_url_pix if pix.default_url_pix else '',
              str(result['brcode'][0]), str(result['base64qr'][0]), shared_link.split('/')[-1]
              )
                     )

        conn.commit()
        conn.close()

        return render_template('payment.html', result=result)

    return render_template('index.html')


@app.route('/invoices/<hash_id>', methods=['GET'])
def invoices(hash_id):
    conn = get_db_connection()
    result_dict = {}
    if hash_id:
        url_data = conn.execute('SELECT * FROM Pix'
                                ' WHERE hash_id = (?)', (hash_id,)
                                ).fetchone()
        clicks = url_data['clicks']

        conn.execute('UPDATE Pix SET clicks = ? WHERE hash_id = ?',
                     (clicks + 1, hash_id))

        conn.commit()
        conn.close()

        result_dict['nome'] = [url_data['full_name']]
        result_dict['chave'] = [url_data['pix_key']]
        result_dict['city'] = [url_data['city']]
        result_dict['zipcode'] = [url_data['zip_code']]
        result_dict['txid'] = [url_data['identification']]
        result_dict['info'] = [url_data['description']]
        result_dict['valor'] = [url_data['amount']]
        result_dict['base64qr'] = [url_data['base64_qr']]
        result_dict['brcode'] = [url_data['br_code']]
        result_dict['shared_link'] = [request.host_url + 'invoices/' + url_data['hash_id']]
        result_dict['clicks'] = [url_data['clicks']]

    return render_template('payment.html', result=result_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
