function getProduct() {
    fetch('http://localhost:5000/product')
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = `Nom : ${data.name}, Prix : ${data.price} €`;
        })
        .catch(err => {
            document.getElementById('result').innerText = 'Erreur lors de la récupération du produit';
        });
}
