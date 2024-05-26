// JavaScript code for dynamically appending product information
fetch('http://127.0.0.1:5001/api/v1/products/')
.then(response => response.json())
.then(data => {
    data.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('a_product');

        const imageElement = document.createElement('img');
        imageElement.src = '../static/images/farm 4.jpg';
        imageElement.alt = 'product_img';
        productElement.appendChild(imageElement);

        const headingElement = document.createElement('h5');
        headingElement.innerHTML = `<span id="des_caption">${product.name}</span><br>
                                    Description: ${product.description}<br>
                                    Price: ${product.price}<br>
                                    Quantity: ${product.quantity}`;
        productElement.appendChild(headingElement);

        document.querySelector('.product_content').appendChild(productElement);
    });
})
.catch(error => console.error('Error fetching products:', error));