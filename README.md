# AgroMarket
AgroMarket is a marketplace where farmers can sell their produce. This project was developed by a team of three contributors.


## Project Description
AgroMarket is a web-based platform that connects farmers with potential buyers. It provides a convenient and efficient way for farmers to showcase and sell their produce directly to consumers. The platform also offers features such as product categorization, search functionality, and secure payment options to enhance the user experience.

## Installation
To install AgroMarket, follow these steps:
1. Clone the repository: `git clone https://github.com/Sobilo34/AgroMarket.git`
2. Navigate to the project directory: `cd AgroMarket`
3. Create and activate a virtual environment: 

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the required packages: `pip install -r requirements.txt`
5. Install MySQL and MySQL client:
   - For Ubuntu: `sudo apt-get install mysql-server libmysqlclient-dev`
   - For macOS: `brew install mysql`

# Set up the .env file
vi .env
Update the necessary environment variables in the .env file with the database name, user.

6. Create a MySQL database and update the database configuration in `setup_mysql_dev.sql`

## Usage
### To use AgroMarket, follow these steps:
1. Start the api server: `python3 -m api.v1.app`
2. Start the web app server: `python3 -m web_app.app
3. Open your web browser and visit `http://localhost:5000`
4. Sign up or log in to your account
5. Browse through the available products or search for specific items
6. Add desired products to your cart and proceed to checkout
7. Track the status of your orders in the dashboard

## API Endpoints
The AgroMarket API provides the following endpoints:


### Users
- `POST /api/v1/login`: Logs a user in
- `GET /api/v1/users`: Get a list of all users
- `GET /api/v1/users/{id}`: Get details of a specific user
- `POST /api/v1/users`: Create a new user
- `PUT /api/v1/users/{id}`: Update details of a specific user
GET /users/<user_id>/orders': Returns all user orders
POST /users/<user_id>/image': uploads user image
- `DELETE /api/v1/users/{id}`: Delete a specific user


### Products
- `GET /api/v1/products`: Get a list of all products

- `GET /api/v1/products/{id}`: Get details of a specific product
- `POST /api/v1/products`: Create a new product
- `PUT /api/v1/products/{id}`: Update details of a specific product
- `DELETE /api/v1/products/{id}`: Delete a specific product

For more information on how to use these endpoints, please refer to the API documentation.
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

## License
AgroMarket is released under the MIT License. See [LICENSE](https://github.com/Sobilo34/AgroMarket/blob/main/LICENSE) for more information.

## Contributing
We welcome contributions from the community to improve AgroMarket. To contribute, please follow these guidelines:
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

## Contributors
<img src="https://avatars.githubusercontent.com/u/63774376?v=4" alt="Adigwe Dennis" height="30" width="30" style="border-radius: 50%;">  [Adigwe Dennis](https://github.com/talk2dennis)

<img src="https://avatars.githubusercontent.com/u/99018748?v=4" alt="Gideon Oba" height="30" width="30" style="border-radius: 50%;">  [Gideon Oba](https://github.com/Deyonoba)

<img src="https://avatars.githubusercontent.com/u/122975292?v=4" alt="Bilal Oyeleke" height="30" width="30" style="border-radius: 50%;">  [Bilal Oyeleke](https://github.com/Sobilo34)

## Contact
For any inquiries, please contact the project contributors:
- Adigwe Dennis: adigwedennis@gmail.com
- Gideon Oba: deyonoba@gmail.com
- Bilal Oyeleke: bilalsolih60@gmail.com
