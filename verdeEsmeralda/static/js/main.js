const messages = [

"Conecta tu espacio con la naturaleza 🌿",
"Kokedamas hechas a mano",
"Transforma tu hogar con plantas vivas",
"Talleres botánicos cada mes"

]

let index = 0

setInterval(() => {

    index++

    if(index >= messages.length){
        index = 0
    }

    document.getElementById("top-message").textContent = messages[index]

}, 4000)

