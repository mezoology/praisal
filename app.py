import requests
from flask import Flask, render_template, request
from models import db, MarketData

app = Flask(__name__)

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# EVE Online API endpoint for Jita market data
JITA_MARKET_API_URL = 'https://esi.evetech.net/latest/markets/10000002/orders/'

# Function to fetch market data from Jita
def fetch_jita_market_data():
    try:
        response = requests.get(JITA_MARKET_API_URL, params={'order_type': 'sell'})
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Function to populate the database with market data
def populate_database():
    market_data = fetch_jita_market_data()
    for item in market_data:
        existing_item = MarketData.query.filter_by(type_id=item['type_id']).first()
        if not existing_item:
            new_item = MarketData(
                type_id=item['type_id'],
                price=item['price'],
                volume_remain=item['volume_remain'],
                location_id=item['location_id']
            )
            db.session.add(new_item)
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        item_id = request.form['item_id']
        item = MarketData.query.filter_by(type_id=int(item_id)).order_by(MarketData.price.asc()).first()
        if item:
            return render_template('search_result.html', item=item)
        else:
            return render_template('search_result.html', message="Item not found.")
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
