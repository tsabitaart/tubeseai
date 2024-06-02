from flask import Flask, jsonify, request, render_template
import requests
import random

app = Flask(__name__)

# menu
def get_menus():
    response = requests.get(f'http://localhost:5003/burger')
    return response.json()

@app.route('/burger')
def get_menu():
    menu = get_menus()
    return render_template('index.html', menu=menu)

HASURA_API_URL = 'https://burgerplanet.hasura.app/v1/graphql'
HASURA_API_KEY = 'kp2SL81BuVRoK4IhX1yGrSauTX9Ng5HyPIb7Vu3rURZK770dPTdx1puj6jhCAxjz'

def get_max_id_formulir_from_hasura():
    query = '''
        query GetFormulir {
            formulir_aggregate {
                aggregate {
                    max {
                        id
                    }
                }
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
            return None
        return data['data']['formulir_aggregate']['aggregate']['max']['id']
    else:
        print('Error fetching max idUlasan from Hasura:', response.status_code, response.text)
        return None

def send_to_hasura(id, nama, barang, quantity):

    max_id_formulir = get_max_id_formulir_from_hasura()
    if max_id_formulir is None:
        return False

    new_id_formulir = max_id_formulir + 1

    
    variables = {
        "id": new_id_formulir,
        "nama": nama,
        "barang": barang,
        "quantity": quantity,
    }

    print(variables)

    payload = {
        "query": """
        mutation InsertFormulir($id: Int, $nama: String, $barang: String, $quantity: String) {
            insert_formulir(objects: {id: $id, nama: $nama, barang: $barang, quantity: $quantity}) {
                affected_rows
                returning {
                    id
                    nama
                    barang
                    quantity
                }
            }
        }
        """,
        "variables": variables
    }

    headers = {
        'Content-Type': 'application/json',
        'x-hasura-admin-secret': HASURA_API_KEY
    }

    # Mengirim POST request ke endpoint Hasura
    response = requests.post(HASURA_API_URL, json=payload, headers=headers)

    # Debugging: Print the response status and data
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

    return response.json()

@app.route('/beli', methods=['GET', 'POST'])
def beli():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        barang = request.form['barang']
        quantity = request.form['quantity']
        
        # Proses pembelian
        # Mengirim data ke endpoint Hasura
        response = send_to_hasura(id, nama, barang, quantity)
        if response is False:
            return jsonify({"error": "Gagal melakukan pembelian. ID tidak valid."})
        elif 'errors' not in response:
            return jsonify({"message": "Pembelian berhasil."})
        else:
            return jsonify({"error": "Gagal melakukan pembelian.", "details": response['errors']})
    else:
        return render_template('beli.html')
    
if __name__ == "__main__":
    app.run(debug=True, port=5004)