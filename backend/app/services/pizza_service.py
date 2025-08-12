"""
Pizza service layer for business logic
"""
from typing import List
from sqlalchemy.orm import Session
from ..models import Pizza

class PizzaService:
    """Service class for pizza operations"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_all_pizzas(self) -> List[Pizza]:
        """Get all available pizzas"""
        try:
            return self.db.query(Pizza).order_by(Pizza.name).all()
        except Exception as e:
            raise ValueError(f"Failed to retrieve pizzas: {str(e)}")
    
    def get_pizza_by_id(self, pizza_id: int) -> Pizza:
        """Get pizza by ID"""
        try:
            pizza = self.db.get(Pizza, pizza_id)
            if not pizza:
                raise ValueError(f"Pizza with ID {pizza_id} not found")
            return pizza
        except Exception as e:
            raise ValueError(f"Failed to retrieve pizza: {str(e)}")
