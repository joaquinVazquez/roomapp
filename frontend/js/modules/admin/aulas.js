async function cargarAulas(){

    const contenedor =
        document.getElementById("contenido");


    contenedor.innerHTML = `

        <div class="card">

            <h2>
                🏫 Aulas
            </h2>


            <p>
                Gestión de espacios académicos.
            </p>


        </div>

    `;

}


window.cargarAulas = cargarAulas;