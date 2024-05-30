from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HASURA_API_URL = 'https://tugas-graphql-1.hasura.app/v1/graphql'
HASURA_API_KEY = 'w1BEMIKlJwe8AGR0s7lbWjvfglWHk2uPuqsWQLLbM5n9SRhgACRSkekNj0KHvbtQ'

minuman = [
    {"id": 1, "nama": "Es Teh", "harga": 5000},
    {"id": 2, "nama": "Jus Jeruk", "harga": 10000}
]
def fetch_drinks_from_hasura():
    query = '''
        query GetDrinks {
            minuman {
                id
                nama
                harga
                foto
                deskripsi
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
        return data['data']['minuman']  
    else:
        print('Error fetching users from Hasura:', response.status_code, response.text)
        return []

@app.route('/minuman', methods=['GET'])
def get_minuman():
    drinks = fetch_drinks_from_hasura()
    return jsonify(drinks)

# @app.route('/minuman', methods=['GET'])
# def get_minuman():
#     return jsonify(minuman), 200

@app.route('/minuman', methods=['POST'])
def add_minuman():
    minuman_baru = request.json
    minuman_baru['id'] = len(minuman) + 1
    minuman.append(minuman_baru)
    return jsonify(minuman_baru), 201

if __name__ == '__main__':
    app.run(port=5002, debug=True)
