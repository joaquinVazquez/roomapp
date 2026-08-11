// ===============================
// MÓDULO: HORARIOS
// ===============================


// ===============================
// MI HORARIO
// ===============================

async function cargarMiHorario() {

    try {

        const usuario =
            await getCurrentUser();


        // -------------------------
        // ESTUDIANTE
        // -------------------------

        if (
            usuario.rol === "ESTUDIANTE"
        ) {

            return await getHorariosEstudiante();

        }


        // -------------------------
        // DOCENTE
        // -------------------------

        if (
            usuario.rol === "DOCENTE"
        ) {

            return await getHorariosDocente();

        }


        // -------------------------
        // OTROS ROLES
        // -------------------------

        return {
            dias: []
        };

    }
    catch (error) {

        console.error(
            "Error cargando horario:",
            error
        );

        return {
            dias: []
        };

    }

}


// ===============================
// HORARIO GENERAL
// ===============================

async function cargarHorarioGeneral() {

    try {

        console.log(
            "Cargando horario general..."
        );


        const data =
            await getHorariosGenerales();


        console.log(
            "HORARIO GENERAL:",
            data
        );


        mostrarHorarios(data);


    }
    catch (error) {

        console.error(
            "Error horario general:",
            error
        );


        mostrarError(
            "No se pudo cargar el horario general."
        );

    }

}


// ===============================
// RENDER HORARIOS
// ===============================

function mostrarHorarios(data) {

    const contenedor =
        document.getElementById(
            "contenido"
        );


    if (!contenedor) {

        console.error(
            "No existe #contenido"
        );

        return;
    }


    if (!data) {

        mostrarError(
            "No se recibieron datos."
        );

        return;
    }


    const dias =
        data.dias ??
        data.horarios ??
        [];


    // -------------------------
    // SIN HORARIOS
    // -------------------------

    if (
        !Array.isArray(dias) ||
        dias.length === 0
    ) {

        contenedor.innerHTML = `

            <div
                style="
                    text-align:center;
                    padding:40px;
                "
            >

                <h3>
                    📭 Sin horarios
                </h3>

                <p>
                    No hay información disponible
                    para el periodo seleccionado.
                </p>

            </div>

        `;

        return;
    }


    // -------------------------
    // LIMPIAR
    // -------------------------

    contenedor.innerHTML = "";


    // -------------------------
    // CREAR DÍAS
    // -------------------------

    dias.forEach(
        dia => {

            const bloque =
                document.createElement(
                    "section"
                );


            bloque.className =
                "dia";


            const clases =
                Array.isArray(dia.clases)
                ? dia.clases
                : [];


            bloque.innerHTML = `

                <h2>
                    ${dia.dia}
                </h2>

                ${
                    clases
                        .map(
                            crearCardHorario
                        )
                        .join("")
                }

            `;


            contenedor.appendChild(
                bloque
            );

        }
    );

}


// ===============================
// CARD DE HORARIO
// ===============================

function crearCardHorario(clase) {

    const aula =
        clase.aula === "SIN ASIGNAR"

        ? `
            <span class="sin-aula">
                SIN ASIGNAR
            </span>
        `

        : (
            clase.aula ??
            "SIN ASIGNAR"
        );


    const docente =
        clase.docente

        ? `
            <div class="detalle">

                👨‍🏫
                ${clase.docente}

            </div>
        `

        : "";


    return `

        <div class="card">

            <div class="hora">

                ⏰
                ${clase.hora ?? ""}

            </div>


            <div class="materia">

                ${clase.materia ?? ""}

            </div>


            <div class="detalle">

                👥 Grupo:
                ${clase.grupo ?? ""}

            </div>


            <div class="detalle">

                🏫 Aula:
                ${aula}

            </div>


            ${docente}

        </div>

    `;

}


// ===============================
// MENSAJE DE ERROR
// ===============================

function mostrarError(
    mensaje = "Ocurrió un error"
) {

    const contenedor =
        document.getElementById(
            "contenido"
        );


    if (!contenedor) {

        return;
    }


    contenedor.innerHTML = `

        <div
            style="
                text-align:center;
                padding:40px;
                color:red;
            "
        >

            <h3>
                ⚠️ Error
            </h3>

            <p>
                ${mensaje}
            </p>

        </div>

    `;

}


// ===============================
// EXPOSICIÓN CONTROLADA
// ===============================

// ===============================
// ERROR
// ===============================

function mostrarError(
    mensaje = "Ocurrió un error"
) {

    const contenedor =
        document.getElementById("contenido");

    if (!contenedor) return;

    contenedor.innerHTML = `

        <div
            style="
                text-align:center;
                padding:40px;
                color:red;
            "
        >

            <h3>⚠️ Error</h3>

            <p>${mensaje}</p>

        </div>

    `;
}


// ===============================
// EXPOSICIÓN GLOBAL
// ===============================

window.cargarMiHorario = cargarMiHorario;
window.cargarHorarioGeneral = cargarHorarioGeneral;
window.mostrarHorarios = mostrarHorarios;