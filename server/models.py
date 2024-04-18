from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(225), nullable=False)
    name = db.Column(db.String(225), nullable=False)

    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

class Pizzas(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    ingredients = db.Column(db.String(225), nullable=False)

    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    # Add the following lines to define the back references
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizzas', back_populates='restaurants')