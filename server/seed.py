from faker import Faker
from app import app, db, Restaurant, Pizzas, RestaurantPizza
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  # Import func from SQLAlchemy's sql module

fake = Faker()

def seed_restaurants(num_restaurants=10):
    for _ in range(num_restaurants):
        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address()
        )
        db.session.add(restaurant)
    db.session.commit()

def seed_pizzas(num_pizzas=10):
    for _ in range(num_pizzas):
        pizza = Pizzas(
            name=fake.word(),
            ingredients=', '.join(fake.words(nb=3))
        )
        db.session.add(pizza)
    db.session.commit()

def seed_restaurant_pizzas(num_combinations=20):
    for _ in range(num_combinations):
        restaurant = Restaurant.query.order_by(func.random()).first()  # Use func here
        pizza = Pizzas.query.order_by(func.random()).first()  # Use func here
        price = round(fake.pyfloat(min_value=5, max_value=20), 2)

        restaurant_pizza = RestaurantPizza(
            restaurant_id=restaurant.id,
            pizza_id=pizza.id,
            price=price
        )
        db.session.add(restaurant_pizza)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_restaurants()
        seed_pizzas()
        seed_restaurant_pizzas()
