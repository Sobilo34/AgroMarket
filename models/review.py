from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """Representation of a review data and methods"""
    __tablename__ = 'reviews'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    
    user = relationship('User', back_populates='reviews')
    order = relationship('Order', back_populates='reviews')

    def __init__(self, *args, **kwargs):
        """Initializes review"""
        super().__init__(*args, **kwargs)

    def set_user(self, user):
        """Sets the user for the review"""
        self.user_id = user.id

    def set_order(self, order):
        """Sets the order for the review"""
        self.order_id = order.id

    def set_rating(self, rating):
        """Sets the rating for the review"""
        self.rating = rating

    def set_comment(self, comment):
        """Sets the comment for the review"""
        self.comment = comment
