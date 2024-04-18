import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import PizzaForm from "./PizzaForm";

function Home() {
  const [{ data: restaurant, error, status }, setRestaurant] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const { id } = useParams();``

  useEffect(() => {
    fetch(`http://127.0.0.1:5555/restaurants/${id}`).then((r) => {
      if (r.ok) {
        r.json().then((restaurant) =>
          setRestaurant({ data: restaurant, error: null, status: "resolved" })
        );
      } else {
        r.json().then((err) =>
          setRestaurant({ data: null, error: err.error, status: "rejected" })
        );
      }
    });
  }, [id]);

  function handleAddPizza(newRestaurantPizza) {
    setRestaurant({
      data: {
        ...restaurant,
        restaurant_pizzas: [
          ...restaurant.restaurant_pizzas,
          newRestaurantPizza,
        ],
      },
      error: null,
      status: "resolved",
    });
  }

  if (status === "pending") return <h1>Loading...</h1>;
  if (status === "rejected") return <h1>Error: {error.error}</h1>;

  return (
    <section className="container">
      <div className="card">
        <h1>{restaurant.name}</h1>
        <p>{restaurant.address}</p>
      </div>
      <div className="card">
        <h2>Pizza Menu</h2>
        {restaurant.restaurant_pizzas.map((restaurant_pizza) => (
          <div key={restaurant_pizza.pizza.id}>
            <h3>{restaurant_pizza.pizza.name}</h3>
            <p>
              <em>{restaurant_pizza.pizza.ingredients}</em>
            </p>
            <p>
              <em>Price ${restaurant_pizza.price}</em>
            </p>
          </div>
        ))}
      </div>
      <div className="card">
        <h3>Add New Pizza</h3>
        <PizzaForm restaurantId={restaurant.id} onAddPizza={handleAddPizza} />
      </div>
    </section>
  );
}

export default Home;
