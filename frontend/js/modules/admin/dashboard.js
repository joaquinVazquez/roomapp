// ===============================
// DASHBOARD ADMINISTRADOR
// ===============================


async function cargarDashboard(){

    const contenedor =
        document.getElementById("contenido");


    if(!contenedor){
        return;
    }


    contenedor.innerHTML = `

        <div class="card">

            <h2>
                📊 Dashboard Administrador
            </h2>


            <p>
                Bienvenido al panel de administración.
            </p>


            <hr>


            <p>
                Desde aquí podrá gestionar:
            </p>


            <ul>
                <li>Usuarios</li>
                <li>Aulas</li>
                <li>Materias</li>
                <li>Configuración general</li>
            </ul>


        </div>

    `;

}


window.cargarDashboard = cargarDashboard;