document.addEventListener(
    "DOMContentLoaded",
    async () => {

        try {

            const usuario =
                await getCurrentUser();


            mostrarUsuario(usuario);


            crearMenuPorRol(
                usuario.rol
            );


            // Carga inicial según rol

            if (
                usuario.rol === "DOCENTE" ||
                usuario.rol === "ESTUDIANTE"
            ) {

                await cargarMiHorario();

            }


            if (
                usuario.rol === "ADMINISTRADOR" ||
                usuario.rol === "COORDINADOR_ACADEMICO" ||
                usuario.rol === "PERSONAL_ADMINISTRATIVO"
            ) {

                await cargarHorarioGeneral();

            }


        }
        catch(error) {


            console.error(
                "ERROR APP:",
                error
            );


            localStorage.removeItem(
                "token"
            );


            window.location.href =
                "login.html";

        }

    }
);





// ===============================
// INFORMACIÓN DEL USUARIO
// ===============================

function mostrarUsuario(usuario) {


    const elemento =
        document.getElementById(
            "usuario-info"
        );


    if (!elemento) {
        return;
    }


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