from sqlalchemy import Column, String, Text, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Product(BaseModel, Base):
    """Representation of a product data and methods """
    __tablename__ = 'products'
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, default=0)
    cover_img = Column(String(100), default='agromarket.jpg')
    location = Column(String(100), nullable=True)
    category_id = Column(String(60), ForeignKey('categories.id'),
                         nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='products')
    category = relationship('Category', back_populates='products')
    images = relationship('Image', back_populates='product')
    orders = relationship('Order', back_populates='product')

    def __init__(self, *args, **kwargs):
        """initializes product"""
        super().__init__(*args, **kwargs)

    def set_price(self, price):
        """ sets the price of the product """
        self.price = price

    def set_quantity(self, quantity):
        """ sets the quantity of the product """
        self.quantity = quantity

    def set_location(self, location):
        """ sets the location of the product """
        self.location = location

    # def set_harvest_date(self, date_of_harvest):
    #     """Sets the day of harvest of product"""
    #     self.date_of_harvest = date_of_harvest

    def set_category(self, category):
        """ sets the category of the product """
        self.category_id = category.id

    def set_user(self, user):
        """ sets the user of the product """
        self.user_id = user.id

    def add_image(self, image):
        """Adds an image to the product if under 5 images"""
        if self.images.count() < 5:
            self.images.append(image)
        else:
            raise Exception("Cannot add more than 5 images to a product")
