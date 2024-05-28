// function showUploadForm() {
//     document.getElementById('uploadFormContainer').style.display = 'block';
// }

// function hideUploadForm() {
//     document.getElementById('uploadFormContainer').style.display = 'none';
// }

// async function submitProduct() {
//     const productName = document.getElementById('productName').value;
//     const productDescription = document.getElementById('productDescription').value;
//     const productPrice = document.getElementById('productPrice').value;
//     const productQuantity = document.getElementById('productQuantity').value;

//     const productData = {
//         name: productName,
//         description: productDescription,
//         price: productPrice,
//         quantity: productQuantity
//     };

//     try {
//         const response = await fetch('http://127.0.0.1:5001/api/v1/products', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(productData)
//         });

//         if (response.ok) {
//             alert('Product uploaded successfully!');
//             hideUploadForm();
//             // Optionally, refresh the product list to include the new product
//         } else {
//             alert('Failed to upload product.');
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred while uploading the product.');
//     }
// }

// // JavaScript code for dynamically appending product information
// fetch('http://127.0.0.1:5001/api/v1/products')
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok ' + response.statusText);
//         }
//         return response.json();
//     })
//     .then(data => {
//         const productContent = document.querySelector('.product_content');
//         data.forEach(product => {
//             const productElement = document.createElement('div');
//             productElement.classList.add('a_product');

//             const imageElement = document.createElement('div');
//             imageElement.innerHTML = `<img src="${product.image || '../static/images/farm 4.jpg'}" alt="product_img">`;
//             productElement.appendChild(imageElement);
            

//             const headingElement = document.createElement('h5');
//             headingElement.innerHTML = `<span id="des_caption">${product.name}</span><br>
//                                         Description: ${product.description}<br>
//                                         Price: ${product.price}<br>
//                                         Quantity: ${product.quantity}<br>
//                                         Date of Harvest: ${product.date_of_harvest ? product.date_of_harvest : 'N/A'}`;
//             productElement.appendChild(headingElement);

//             productContent.appendChild(productElement);
//         });
//     })
//     .catch(error => console.error('Error fetching products:', error));
