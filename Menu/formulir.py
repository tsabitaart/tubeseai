from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

HASURA_API_URL = 'https://burgerplanet.hasura.app/v1/graphql'
HASURA_API_KEY = 'kp2SL81BuVRoK4IhX1yGrSauTX9Ng5HyPIb7Vu3rURZK770dPTdx1puj6jhCAxjz'

def fetch_foods_from_hasura():
    query = '''
        query GetFoods {
            formulir {
                nama
                barang
                id
                quantity
            }
        }
    '''
    
    headers = {
        'Content-Type': 'application/json',
        'x-hasura-admin-secret': HASURA_API_KEY
    }

    response = requests.post(HASURA_API_URL, json={'query': query}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print('GraphQL Errors:', data['errors'])
            return []
        return data['data']['formulir']
    else:
        print('Error fetching users from Hasura:', response.status_code, response.text)
        return []

@app.route('/')
def form():
    return render_template('formulir.html')

@app.route('/formulir', methods=['POST'])
def checkout_last():
    nama = request.form.get('nama')
    barang = request.form.get('barang')
    quantity = request.form.get('quantity')
    metode_pembayaran = request.form.get('metode_pembayaran')
    return f'Nama: {nama}, Barang yang Dibeli: {barang}, Quantity: {quantity}, Metode Pembayaran: {metode_pembayaran}'

@app.route('/formulir')
def get_burger():
    burgers = fetch_foods_from_hasura()
    return jsonify(burgers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
