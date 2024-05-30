from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

# Function to fetch menus
def get_menus():
    response = requests.get('http://localhost:5003/burger')
    return response.json()

@app.route('/burger')
def get_menu():
    menu = get_menus()
    return render_template('index.html', menu=menu)

@app.route('/formulir', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        nama = request.form.get('nama')
        barang = request.form.get('barang')
        quantity = request.form.get('quantity')
        metode_pembayaran = request.form.get('metode_pembayaran')
        # Process the form data here, e.g., save to a database or send to an API
        return f'Nama: {nama}, Barang yang Dibeli: {barang}, Quantity: {quantity}, Metode Pembayaran: {metode_pembayaran}'
    return render_template('formulir.html')

if __name__ == "__main__":
    app.run(debug=True, port=5004)
