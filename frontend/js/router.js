// ===============================
// ROUTER PRINCIPAL ROOMAPP
// ===============================

async function redirectByRole() {

    try {

        const user = await API.getCurrentUser();

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

    }
    catch (error) {

        console.error(
            "Error en redirectByRole:",
            error
        );

        alert(
            "No fue posible iniciar sesión."
        );

    }

}


// ===============================
// MENÚ POR ROL
// ===============================

function crearMenuPorRol(rol) {

    const menu =
        document.getElementById("menu");

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
    // ADMINISTRADOR
    // ----------------------------

    else if (
        rol === "ADMINISTRADOR"
    ) {

        opciones = [

            {
                nombre: "📊 Dashboard",
                accion: "dashboard"
            },

            {
                nombre: "👥 Usuarios",
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
                nombre: "📆 Periodos académicos",
                accion: "periodos"
            },

            {
                nombre: "📅 Horario general",
                accion: "general"
            }

        ];

    }


    // ----------------------------
    // COORDINADOR ACADÉMICO
    // ----------------------------

    else if (
        rol === "COORDINADOR_ACADEMICO"
    ) {

        opciones = [

            {
                nombre: "🏫 Aulas",
                accion: "aulas"
            },

            {
                nombre: "📚 Materias",
                accion: "materias"
            },

            {
                nombre: "📆 Periodos académicos",
                accion: "periodos"
            },

            {
                nombre: "📅 Horario general",
                accion: "general"
            }

        ];

    }


    // ----------------------------
    // PERSONAL ADMINISTRATIVO
    // ----------------------------

    else if (
        rol === "PERSONAL_ADMINISTRATIVO"
    ) {

        opciones = [

            {
                nombre: "📅 Horario general",
                accion: "general"
            }

        ];

    }


    // ----------------------------
    // RENDER DEL MENÚ
    // ----------------------------

    menu.innerHTML = opciones
        .map(op => `

            <button
                class="menu-btn"
                data-accion="${op.accion}"
                onclick="activarMenu(
                    this,
                    '${op.accion}'
                )"
            >
                ${op.nombre}
            </button>

        `)
        .join("");


    activarPrimerBoton();

}


// ===============================
// ACTIVAR BOTÓN DEL MENÚ
// ===============================

function activarMenu(
    boton,
    accion
) {

    document
        .querySelectorAll(".menu-btn")
        .forEach(btn =>
            btn.classList.remove("activo")
        );


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
// CARGA DE MÓDULOS - SPA
// ===============================

async function cargarModulo(opcion) {

    try {

        mostrarLoading();


        switch (opcion) {


            // -------------------------
            // DASHBOARD
            // -------------------------

            case "dashboard":

                document.getElementById(
                    "contenido"
                ).innerHTML = `

                    <h2>📊 Dashboard</h2>

                    <p>
                        Panel en construcción
                    </p>

                `;

                break;


            // -------------------------
            // USUARIOS
            // -------------------------

            case "usuarios":

                await cargarUsuarios();

                break;


            // -------------------------
            // AULAS
            // -------------------------

            case "aulas":

                document.getElementById(
                    "contenido"
                ).innerHTML = `

                    <h2>🏫 Aulas</h2>

                    <p>
                        Módulo en construcción
                    </p>

                `;

                break;


            // -------------------------
            // MATERIAS
            // -------------------------

            case "materias":

                document.getElementById(
                    "contenido"
                ).innerHTML = `

                    <h2>📚 Materias</h2>

                    <p>
                        Módulo en construcción
                    </p>

                `;

                break;


            // -------------------------
            // GRUPOS
            // -------------------------

            case "grupos":

                document.getElementById(
                    "contenido"
                ).innerHTML = `

                    <h2>👥 Grupos</h2>

                    <p>
                        Módulo en construcción
                    </p>

                `;

                break;


            // -------------------------
            // PERIODOS ACADÉMICOS
            // -------------------------

            case "periodos":

                await cargarPeriodosModulo();

                break;

            // -------------------------
            // HORARIO GENERAL
            // -------------------------

            case "general":

                console.log(
                    "Cargando horario general"
                );


                await cargarHorarioGeneral();


                console.log(
                    "Horario general terminado"
                );

                break;


            // -------------------------
            // MI HORARIO
            // -------------------------

            case "horario":

                const data =
                    await cargarMiHorario();


                mostrarHorarios(data);

                break;


            // -------------------------
            // DEFAULT
            // -------------------------

            default:

                document.getElementById(
                    "contenido"
                ).innerHTML = `

                    <h2>
                        Módulo no encontrado
                    </h2>

                `;

        }

    }
    catch (error) {

        console.error(
            "Error cargando módulo:",
            error
        );


        mostrarError(
            "No se pudo cargar el módulo."
        );

    }

}