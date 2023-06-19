amount = document.querySelector("#amount")

function getPrice() {
    setInterval(
        function() {
            fetch("http://127.0.0.1:8000/get").then(
                function(response) {
                    return response.clone().json()
                }
            ).then(
                function(data) {
                    amount.textContent = data.price
                }
            ).catch(function(error) {
                console.log(error)
            })
        },
        1000
    )
}

document.addEventListener("DOMContentLoaded", function(e) {
    getPrice()
})
