from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)
BASE_URL = "http://127.0.0.1"

# menu
def get_menus():
    response = requests.get(f'http://localhost:5003/burger')
    return response.json()

@app.route('/burger')
def get_menu():
    menu = get_menus()
    return render_template('index.html', menu=menu)

#Menampilkan hal menu minuman
@app.route('/drinks-menu')
def menu():
    minuman = requests.get(f"{BASE_URL}:5002/minuman").json()
    return render_template('drink_menu.html',minuman=minuman)

if __name__ == "__main__":
    app.run(debug=True, port=5004)
