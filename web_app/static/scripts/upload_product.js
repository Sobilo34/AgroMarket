function showUploadForm() {
    document.getElementById('uploadFormContainer').style.display = 'block';
}

function hideUploadForm() {
    document.getElementById('uploadFormContainer').style.display = 'none';
}

async function submitProduct() {
    const productName = document.getElementById('productName').value;
    const productDescription = document.getElementById('productDescription').value;
    const productPrice = document.getElementById('productPrice').value;
    const productQuantity = document.getElementById('productQuantity').value;

    const productData = {
        name: productName,
        description: productDescription,
        price: productPrice,
        quantity: productQuantity
    };

    try {
        const response = await fetch('http://127.0.0.1:5001/api/v1/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData)
        });

        if (response.ok) {
            alert('Product uploaded successfully!');
            hideUploadForm();
            // Optionally, refresh the product list to include the new product
        } else {
            alert('Failed to upload product.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the product.');
    }
}
