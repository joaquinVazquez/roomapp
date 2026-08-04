// ===============================
// ROUTER PRINCIPAL ROOMAPP
// ===============================

async function redirectByRole() {

    try {

        const user = await getCurrentUser();

        // Todos los roles entran a la SPA
        switch (user.rol) {

            case "ADMINISTRADOR":
            case "COORDINADOR_ACADEMICO":
            case "DOCENTE":
            case "ESTUDIANTE":
            case "PERSONAL_ADMINISTRATIVO":

                window.location.href = "index.html";
                break;

            default:
                alert("Rol no configurado");
        }

    } catch (error) {

        console.error("Error en redirectByRole:", error);
        alert("Error identificando usuario");

    }

}



// ===============================
// MENÚ DINÁMICO POR ROL
// ===============================

function crearMenuPorRol(rol) {

    const menu = document.getElementById("menu");

    if (!menu) return;

    let opciones = [];


    // ======================
    // ROLES
    // ======================

    if (rol === "DOCENTE" || rol === "ESTUDIANTE") {

        opciones = [
            {
                nombre: "📅 Mi horario",
                accion: "horario"
            }
        ];

    }


    if (
        rol === "ADMINISTRADOR" ||
        rol === "COORDINADOR_ACADEMICO" ||
        rol === "PERSONAL_ADMINISTRATIVO"
    ) {

        opciones = [
            {
                nombre: "📊 Horario general",
                accion: "general"
            }
        ];

    }


    // ======================
    // RENDER DEL MENÚ
    // ======================

    menu.innerHTML = opciones.map(op => `
        <button onclick="cargarModulo('${op.accion}')">
            ${op.nombre}
        </button>
    `).join("");

}



// ===============================
// CARGA DE MÓDULOS (SPA)
// ===============================

async function cargarModulo(opcion) {

    try {

        const contenedor = document.getElementById("contenido");

        if (!contenedor) return;

        // Loader simple
        contenedor.innerHTML = "<p id='loading'>Cargando...</p>";


        switch (opcion) {

            case "horario":
                await cargarMiHorario();
                break;


            case "general":
                await cargarHorarioGeneral();
                break;


            default:
                contenedor.innerHTML = "<h2>Módulo en construcción</h2>";

        }

    } catch (error) {

        console.error("Error cargando módulo:", error);

        document.getElementById("contenido").innerHTML =
            "<p style='color:red;'>Error cargando módulo</p>";

    }

}