from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Image(BaseModel, Base):
    """Representation of an image data and methods"""
    __tablename__ = 'images'
    url = Column(String(256), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
    product = relationship('Product', back_populates='images')
    user = relationship('User', back_populates='images')

    def __init__(self, *args, **kwargs):
        """Initializes image"""
        super().__init__(*args, **kwargs)

    def set_url(self, url):
        """Sets the URL for the image"""
        self.url = url

    def set_product(self, product):
        """Sets the product for the image"""
        self.product_id = product.id

    def set_user(self, user):
        """Sets the user for the image"""
        self.user_id = user.id
