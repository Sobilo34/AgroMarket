from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from datetime import datetime

class Delivery(BaseModel, Base):
    """Representation of a delivery data and methods"""
    __tablename__ = 'deliveries'
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    delivery_date = Column(DateTime, nullable=True)
    delivered = Column(Boolean, default=False)
    address = Column(String(128), nullable=False)
    
    user = relationship('User', back_populates='user')
    order = relationship('Order', back_populates='delivery')

    def __init__(self, *args, **kwargs):
        """Initializes delivery"""
        super().__init__(*args, **kwargs)

    def set_order(self, order):
        """Sets the order for the delivery"""
        self.order_id = order.id

    def set_delivery_date(self, delivery_date):
        """Sets the delivery date"""
        self.delivery_date = delivery_date

    def set_delivered(self, delivered):
        """Sets the delivered status"""
        self.delivered = delivered

    def set_address(self, address):
        """Sets the delivery address"""
        self.address = address
