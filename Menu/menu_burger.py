from flask import Flask, jsonify
import requests

app = Flask(__name__)

HASURA_API_URL = 'https://burgerplanet.hasura.app/v1/graphql'
HASURA_API_KEY = 'kp2SL81BuVRoK4IhX1yGrSauTX9Ng5HyPIb7Vu3rURZK770dPTdx1puj6jhCAxjz'

def fetch_foods_from_hasura():
    query = '''
        query GetFoods {
            table_makanan {
                gambar
                harga
                id
                nama_makanan
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
        return data['data']['table_makanan']
    else:
        print('Error fetching users from Hasura:', response.status_code, response.text)
        return []

@app.route('/burger')
def get_burger():
    burgers = fetch_foods_from_hasura()
    return jsonify(burgers)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)