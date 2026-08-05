// ===============================
// ROUTER PRINCIPAL ROOMAPP
// ===============================

async function redirectByRole() {

    try {

        const user = await getCurrentUser();

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
        alert("No fue posible iniciar sesión.");

    }

}



// ===============================
// MENÚ POR ROL
// ===============================

function crearMenuPorRol(rol) {

    const menu = document.getElementById("menu");

    if (!menu) return;

    let opciones = [];



    // ----------------------------
    // DOCENTE / ESTUDIANTE
    // ----------------------------

    if (
        rol === "DOCENTE" ||
        rol === "ESTUDIANTE"
    ) {

        opciones = [
            {
                nombre: "📅 Mi horario",
                accion: "horario"
            }
        ];

    }



    // ----------------------------
    // ADMINISTRATIVOS
    // ----------------------------

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



    // ----------------------------
    // RENDER
    // ----------------------------

    menu.innerHTML = opciones.map(op => `

        <button
            class="menu-btn"
            data-accion="${op.accion}"
            onclick="activarMenu(this,'${op.accion}')"
        >

            ${op.nombre}

        </button>

    `).join("");



    // Activar automáticamente
    activarPrimerBoton();

}



// ===============================
// ACTIVAR BOTÓN DEL MENÚ
// ===============================

function activarMenu(boton, accion) {

    document
        .querySelectorAll(".menu-btn")
        .forEach(btn => btn.classList.remove("activo"));

    boton.classList.add("activo");

    cargarModulo(accion);

}



// ===============================
// ACTIVAR EL PRIMER BOTÓN
// ===============================

function activarPrimerBoton() {

    const primerBoton =
        document.querySelector(".menu-btn");

    if (!primerBoton) return;

    activarMenu(
        primerBoton,
        primerBoton.dataset.accion
    );

}



// ===============================
// CARGA DE MÓDULOS
// ===============================

async function cargarModulo(opcion) {

    try {

        mostrarLoading();

        switch (opcion) {

            case "horario":

                const horario = await cargarMiHorario();
                mostrarHorarios(horario);
                break;

            case "general":

                const general = await getHorariosGenerales();
                mostrarHorarios(general);
                break;

            default:

                document.getElementById("contenido").innerHTML = `
                    <h2>Módulo en construcción</h2>
                `;

        }

    } catch (error) {

        console.error("Error cargando módulo:", error);

        mostrarError(
            "No fue posible cargar la información."
        );

    }

}