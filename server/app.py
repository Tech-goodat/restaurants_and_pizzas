from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_cors import CORS  # Assuming you are using CORS for handling Cross-Origin Resource Sharing
from models import db, Restaurant, Pizzas, RestaurantPizza  # Assuming Pizza is the correct name for your Pizza model

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/')
def home():
    response_dict = {
        'message': 'Welcome to the Pizza Restaurant',
        'description': 'Explore the world of restaurants and pizzas.',
    }

    response = make_response(
        jsonify(response_dict),
        200
    )

    return response

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants_list = []

    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }

        restaurants_list.append(restaurant_dict)

    response = make_response(
        jsonify(restaurants_list),
        200
    )

    return response

@app.route('/restaurants/<int:restaurant_id>', methods=['GET', 'DELETE'])
def restaurant_by_id(restaurant_id):
    if request.method == 'GET':
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            pizzas = Pizzas.query.join(RestaurantPizza).filter(RestaurantPizza.restaurant_id == restaurant_id).all()

            restaurant_dict = {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address,
                'pizzas': [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in pizzas]
            }
            response = make_response(
                jsonify(restaurant_dict),
                200
            )
        else:
            response_dict = {'error': 'Restaurant not found'}
            response = make_response(jsonify(response_dict), 404)

        return response
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).delete()

            db.session.delete(restaurant)
            db.session.commit()

            response = make_response('', 204)
        else:
            response_dict = {'error': 'Restaurant not found'}
            response = make_response(jsonify(response_dict), 404)

        return response

@app.route('/restaurant_pizza', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()

        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')

        if not all([price, pizza_id, restaurant_id]):
            raise ValueError("Missing required fields")

        pizza = Pizzas.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            raise ValueError("Invalid pizza or restaurant")

        restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
        db.session.add(restaurant_pizza)
        db.session.commit()

        pizza_data = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }

        response = make_response(jsonify(pizza_data), 201)

    except ValueError as e:
        response_data = {'errors': [str(e)]}
        response = make_response(jsonify(response_data), 400)

    return response

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas_list = []

    for pizza in Pizzas.query.all():
        pizza_dict = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }

        pizzas_list.append(pizza_dict)

    response = make_response(
            jsonify(pizzas_list),
            200
        )

    return response

@app.route('/pizzas/<int:pizza_id>', methods=['GET'])
def get_pizza_by_id(pizza_id):
    pizza = Pizzas.query.get(pizza_id)

    if not pizza:
        return make_response(
            jsonify({'error': 'Pizza not found'}),
            404
        )

    pizza_data = {
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }

    response = make_response(
        jsonify(pizza_data),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)