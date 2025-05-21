from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from scraper import scrape_amazon, scrape_price
from database import init_db, create_user, verify_user
import spacy
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Initialize Database
init_db()

# JWT secret key (in production, use environment variable)
SECRET_KEY = "your-secret-key-here"

def generate_token(user_id):
    return jwt.encode(
        {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=1)},
        SECRET_KEY,
        algorithm='HS256'
    )

@app.route("/")
def home():
    return "Flask server is running!"

@app.route("/compare", methods=["POST"])
def compare_prices():
    data = request.json
    product_name = data.get("product")
    urls = data.get("urls", [])

    results = []
    for url in urls:
        price = scrape_price(url)  # Use dynamic scraping function
        if price:
            results.append({"url": url, "price": price})
            conn = sqlite3.connect("prices.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO prices (product_name, url, price) VALUES (?, ?, ?)", 
                           (product_name, url, price))
            conn.commit()
            conn.close()
    
    return jsonify(results)

    if not results:
     return jsonify({"message": "No prices found for the given URLs"}), 404

@app.route("/price-history", methods=["GET"])
def price_history():
    product = request.args.get("product")
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, price, timestamp FROM prices WHERE product_name = ?", (product,))
    data = cursor.fetchall()
    conn.close()
    
    return jsonify([{"url": row[0], "price": row[1], "timestamp": row[2]} for row in data])

@app.route("/search", methods=["POST"])
def search_product():
    data = request.json
    query = data.get("query")
    doc = nlp(query)

    keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return jsonify({"keywords": keywords})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if create_user(data['username'], data['email'], data['password']):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'error': 'Username or email already exists'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user_id = verify_user(data['username'], data['password'])
    if user_id:
        token = generate_token(user_id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/api/compare', methods=['POST'])
def compare_price():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    
    user_id = verify_token(token.split(' ')[1])
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        price = scrape_price(url)
        return jsonify({'price': price}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
