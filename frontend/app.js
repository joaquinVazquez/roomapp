document.addEventListener(
"DOMContentLoaded",
async()=>{


    try{


        const usuario =
        await getCurrentUser();



        mostrarUsuario(
            usuario
        );



        crearMenuPorRol(
            usuario.rol
        );



    }
    catch(error){


        console.error(error);


        localStorage.removeItem(
            "token"
        );


        window.location.href =
        "login.html";


    }


});





function mostrarUsuario(usuario){


    const elemento =
    document.getElementById(
        "usuario-info"
    );



    elemento.innerHTML = `

        Usuario:
        <strong>
        ${usuario.email}
        </strong>

        <br>

        Rol:
        ${usuario.rol}

    `;


}






async function cargarModulo(opcion){


    switch(opcion){


        case "horario":

            await cargarMiHorario();

        break;



        case "general":

            await cargarHorarioGeneral();

        break;



        default:

            document.getElementById(
                "contenido"
            ).innerHTML =
            "<h2>Módulo en construcción</h2>";

    }


}