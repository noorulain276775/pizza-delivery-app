#!/usr/bin/env python3
"""
Seed script to populate the database with initial pizza data
"""
from app import create_app
from app.database import db
from app.models import Pizza

def seed_pizzas():
    """Seed the database with initial pizza data"""
    app = create_app()
    
    with app.app_context():
        # Check if pizzas already exist
        existing_pizzas = Pizza.query.count()
        if existing_pizzas > 0:
            print(f"Database already contains {existing_pizzas} pizzas. Skipping seed.")
            return
        
        # Create initial pizza data
        pizzas_data = [
            {
                'name': 'Margherita',
                'ingredients': 'Fresh mozzarella, tomato sauce, fresh basil',
                'price': 12.99,
                'image': 'images/margherita.jpg'
            },
            {
                'name': 'Pepperoni',
                'ingredients': 'Pepperoni, mozzarella, tomato sauce',
                'price': 15.99,
                'image': 'images/pepperoni.jpg'
            },
            {
                'name': 'Vegetarian',
                'ingredients': 'Bell peppers, mushrooms, onions, olives, mozzarella, tomato sauce',
                'price': 14.99,
                'image': 'images/vegetarian.jpg'
            },
            {
                'name': 'Hawaiian',
                'ingredients': 'Ham, pineapple, mozzarella, tomato sauce',
                'price': 16.99,
                'image': 'images/hawaiian.jpg'
            },
            {
                'name': 'BBQ Chicken',
                'ingredients': 'Grilled chicken, red onions, mozzarella, BBQ sauce',
                'price': 18.99,
                'image': 'images/bbq_chicken.jpg'
            },
            {
                'name': 'Supreme',
                'ingredients': 'Pepperoni, sausage, bell peppers, onions, mushrooms, olives, mozzarella, tomato sauce',
                'price': 20.99,
                'image': 'images/supreme.jpg'
            }
        ]
        
        # Add pizzas to database
        for pizza_data in pizzas_data:
            pizza = Pizza(**pizza_data)
            db.session.add(pizza)
        
        # Commit the changes
        db.session.commit()
        print(f"Successfully seeded {len(pizzas_data)} pizzas to the database!")

if __name__ == '__main__':
    seed_pizzas()
