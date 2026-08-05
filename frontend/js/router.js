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
                nombre: "🏠 Inicio",
                accion: "inicio"
            },

            {
                nombre: "👤 Usuarios",
                accion: "usuarios"
            },

            {
                nombre: "🏫 Aulas",
                accion: "aulas"
            },

            {
                nombre: "📚 Materias",
                accion: "materias"
            },

            {
                nombre: "👥 Grupos",
                accion: "grupos"
            },

            {
                nombre: "🕒 Horarios",
                accion: "horarios"
            },

            {
                nombre: "📅 Períodos",
                accion: "periodos"
            },

            {
                nombre: "📊 Horario General",
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
// CARGA DE MÓDULOS (SPA)
// ===============================

async function cargarModulo(opcion) {

    try {

        mostrarLoading();

        switch (opcion) {

            case "inicio":

                document.getElementById("contenido").innerHTML = `
                    <h2>🏠 Inicio</h2>
                    <p>Bienvenido a RoomApp.</p>
                `;
                break;

            case "usuarios":

                document.getElementById("contenido").innerHTML = `
                    <h2>👤 Usuarios</h2>
                    <p>Módulo en construcción.</p>
                `;
                break;

            case "aulas":

                document.getElementById("contenido").innerHTML = `
                    <h2>🏫 Aulas</h2>
                    <p>Módulo en construcción.</p>
                `;
                break;

            case "materias":

                document.getElementById("contenido").innerHTML = `
                    <h2>📚 Materias</h2>
                    <p>Módulo en construcción.</p>
                `;
                break;

            case "grupos":

                document.getElementById("contenido").innerHTML = `
                    <h2>👥 Grupos</h2>
                    <p>Módulo en construcción.</p>
                `;
                break;

            case "horarios":

                document.getElementById("contenido").innerHTML = `
                    <h2>🕒 Horarios</h2>
                    <p>Módulo en construcción.</p>
                `;
                break;

            case "periodos":

                document.getElementById("contenido").innerHTML = `
                    <h2>📅 Períodos Académicos</h2>
                    <p>Módulo en construcción.</p>
                `;
                break;

            case "general":

                await cargarHorarioGeneral();
                break;

            case "horario":

                const data = await cargarMiHorario();
                mostrarHorarios(data);
                break;

            default:

                document.getElementById("contenido").innerHTML = `
                    <h2>Módulo no encontrado</h2>
                `;

        }

    }
    catch (error) {

        console.error("Error cargando módulo:", error);

        mostrarError("No se pudo cargar el módulo.");

    }

}