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

    <button 
        class="menu-btn"
        onclick="activarMenu(this, '${op.accion}')"
    >
        ${op.nombre}
    </button>

    `).join("");

}

function activarMenu(boton, accion){

    document.querySelectorAll(".menu-btn")
        .forEach(btn => btn.classList.remove("activo"));

    boton.classList.add("activo");

    cargarModulo(accion);

}


// ===============================
// CARGA DE MÓDULOS (SPA)
// ===============================

async function cargarModulo(opcion){

    try{

        mostrarLoading(); // 👈 AQUI VA

        switch(opcion){

            case "horario":
                await cargarMiHorario();
            break;

            case "general":
                await cargarHorarioGeneral();
            break;

            default:
                document.getElementById("contenido").innerHTML =
                "<h2>Módulo en construcción</h2>";
        }

    }
    catch(error){

        console.error("Error cargando módulo:", error);

        mostrarError("No se pudo cargar la información"); // 👈 AQUI VA

    }

}