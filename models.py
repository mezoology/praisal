from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the MarketData model
class MarketData(db.Model):
    __tablename__ = 'market_data'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    volume_remain = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<MarketData {self.type_id} - {self.price} ISK>"
