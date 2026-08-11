async function cargarMaterias(){

    const contenedor =
        document.getElementById("contenido");


    contenedor.innerHTML = `

        <div class="card">

            <h2>
                📚 Materias
            </h2>


            <p>
                Gestión de materias académicas.
            </p>


        </div>

    `;

}


window.cargarMaterias = cargarMaterias;