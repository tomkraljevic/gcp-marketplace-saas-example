from cryptography.x509 import load_pem_x509_certificate
import datetime
from flask import Flask, render_template, request
import json
import jwt
import requests

app = Flask(__name__)


def decode_jwt(encoded):
    unverified_header = jwt.get_unverified_header(encoded)
    kid = unverified_header['kid']
    unverified_decoded = jwt.decode(encoded, options={"verify_signature": False}, algorithms=["RS256"])
    iss = unverified_decoded['iss']
    # print(unverified_decoded)
    # print(iss)
    if iss != "https://www.googleapis.com/robot/v1/metadata/x509/cloud-commerce-partner@system.gserviceaccount.com":
        raise ValueError("Invalid ISS ({})".format(iss))
    response = requests.get(url=iss,
                            timeout=10)
    if response.status_code != 200:
        raise ValueError("Unable to fetch JWT certificate")
    response_dict = json.loads(response.text)
    cert_str = response_dict[kid]
    cert_obj = load_pem_x509_certificate(cert_str.encode())
    public_key = cert_obj.public_key()
    decoded = jwt.decode(encoded,
                         public_key,
                         algorithms=["RS256"],
                         leeway=datetime.timedelta(days=7),
                         audience="gcp-marketplace-h2o-ai-cloud-saas.h2o.ai")
    json_str = json.dumps(decoded, indent=4)
    print(json_str)
    return decoded


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def setup():
    encoded = request.form['x-gcp-marketplace-token']
    decoded = decode_jwt(encoded)
    account_id = decoded['sub']
    obfuscated_user_id = decoded['google']['user_identity']
    return render_template('signup.html', account_id=account_id, obfuscated_user_id=obfuscated_user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     encoded = ""
#     decoded = decode_jwt(encoded)
#     account_id = decoded['sub']
#     obfuscated_user_id = decoded['google']['user_identity']
#     return render_template('signup.html', account_id=account_id, obfuscated_user_id=obfuscated_user_id)
