// ===============================
// HORARIOS
// ===============================

async function cargarMiHorario() {

    try {

        const usuario = await getCurrentUser();

        if (usuario.rol === "DOCENTE") {
            return await getHorariosDocente();
        }

        if (usuario.rol === "ESTUDIANTE") {
            return await getHorariosEstudiante();
        }

        return { dias: [] };

    }
    catch (error) {

        console.error("Error cargando horario:", error);

        return { dias: [] };

    }

}



// ===============================
// HORARIO GENERAL
// ===============================

async function cargarHorarioGeneral() {

    try {

        return await getHorariosGenerales();

    }
    catch (error) {

        console.error("Error cargando horario general:", error);

        return { dias: [] };

    }

}



// ===============================
// RENDER
// ===============================

function mostrarHorarios(data) {

    const contenedor =
        document.getElementById("contenido");

    if (!contenedor) return;



    const dias =
        data?.dias ??
        data?.horarios ??
        [];



    if (dias.length === 0) {

        contenedor.innerHTML = `

            <div style="text-align:center;padding:40px;">

                <h3>📭 Sin horarios</h3>

                <p>No hay información disponible.</p>

            </div>

        `;

        return;

    }



    contenedor.innerHTML = "";



    dias.forEach(dia => {

        const bloque =
            document.createElement("section");

        bloque.className = "dia";



        bloque.innerHTML = `

            <h2>${dia.dia}</h2>

            ${dia.clases
                .map(crearCardHorario)
                .join("")}

        `;



        contenedor.appendChild(bloque);

    });

}



// ===============================
// CARD
// ===============================

function crearCardHorario(clase) {

    return `

        <div class="card">

            <div class="hora">

                ⏰ ${clase.hora}

            </div>

            <div class="materia">

                ${clase.materia}

            </div>

            <div class="detalle">

                👥 Grupo:
                ${clase.grupo}

            </div>

            <div class="detalle">

                🏫 Aula:

                ${
                    clase.aula === "SIN ASIGNAR"

                    ? `<span class="sin-aula">
                        SIN ASIGNAR
                      </span>`

                    : clase.aula
                }

            </div>

            ${
                clase.docente

                ? `

                <div class="detalle">

                    👨‍🏫 ${clase.docente}

                </div>

                `

                : ""

            }

        </div>

    `;

}



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