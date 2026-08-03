// ===============================
// ROUTER PRINCIPAL ROOMAPP
// ===============================


async function redirectByRole() {

    try {

        const user = await getCurrentUser();


        // Todos entran a la aplicación principal

        switch(user.rol){


            case "ADMINISTRADOR":

            case "COORDINADOR_ACADEMICO":

            case "DOCENTE":

            case "ESTUDIANTE":

            case "PERSONAL_ADMINISTRATIVO":

                window.location.href = "index.html";

            break;


            default:

                alert(
                    "Rol no configurado"
                );

        }


    }
    catch(error){

        console.error(error);

        alert(
            "Error identificando usuario"
        );

    }

}





// ===============================
// MENU POR ROL
// ===============================


function crearMenuPorRol(rol){


    const menu =
    document.getElementById(
        "menu"
    );


    menu.innerHTML="";



    switch(rol){


        case "DOCENTE":


            menu.innerHTML = `

            <button onclick="cargarModulo('horario')">
                📅 Mi horario
            </button>

            `;

        break;



        case "ESTUDIANTE":


            menu.innerHTML = `

            <button onclick="cargarModulo('horario')">
                📅 Mi horario
            </button>

            `;

        break;



        case "ADMINISTRADOR":


            menu.innerHTML = `

            <button onclick="cargarModulo('general')">
                📅 Horarios generales
            </button>

            `;


        break;



        case "COORDINADOR_ACADEMICO":


            menu.innerHTML = `

            <button onclick="cargarModulo('general')">
                📅 Horarios generales
            </button>

            `;


        break;



        case "PERSONAL_ADMINISTRATIVO":


            menu.innerHTML = `

            <button onclick="cargarModulo('general')">
                📅 Consultar horarios
            </button>

            `;


        break;



        default:

            menu.innerHTML =
            "Sin opciones";


    }


}