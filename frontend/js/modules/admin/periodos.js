// ===============================
// MÓDULO: PERIODOS ACADÉMICOS
// ===============================

// ===============================
// CARGAR PERIODOS
// ===============================

async function cargarPeriodosModulo() {

    try {

        console.log(
            "Cargando módulo Periodos Académicos..."
        );


        const periodos =
            await getPeriodos();


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


        // -------------------------
        // SIN PERIODOS
        // -------------------------

        if (
            !periodos ||
            periodos.length === 0
        ) {

            contenedor.innerHTML = `

                <h2>
                    📆 Periodos Académicos
                </h2>

                <div class="card">

                    <p>
                        No existen periodos académicos registrados.
                    </p>

                </div>

            `;

            return;
        }


        // -------------------------
        // TABLA
        // -------------------------

        contenedor.innerHTML = `

            <h2>
                📆 Periodos Académicos
            </h2>

            <table class="tabla-usuarios">

                <thead>

                    <tr>

                        <th>
                            Clave
                        </th>

                        <th>
                            Nombre
                        </th>

                        <th>
                            Fecha inicio
                        </th>

                        <th>
                            Fecha fin
                        </th>

                        <th>
                            Estado
                        </th>

                    </tr>

                </thead>


                <tbody>

                    ${periodos.map(periodo => `

                        <tr>

                            <td>
                                ${periodo.clave}
                            </td>

                            <td>
                                ${periodo.nombre}
                            </td>

                            <td>
                                ${formatearFechaPeriodo(
                                    periodo.fecha_inicio
                                )}
                            </td>

                            <td>
                                ${formatearFechaPeriodo(
                                    periodo.fecha_fin
                                )}
                            </td>

                            <td>

                                <strong>
                                    ${
                                        periodo.activo
                                            ? "Activo"
                                            : "Inactivo"
                                    }
                                </strong>

                            </td>

                        </tr>

                    `).join("")}

                </tbody>

            </table>

        `;

    }
    catch (error) {

        console.error(
            "Error cargando periodos:",
            error
        );


        mostrarError(
            "No se pudieron cargar los periodos académicos."
        );

    }

}


// ===============================
// FORMATEAR FECHA
// ===============================

function formatearFechaPeriodo(
    fecha
) {

    if (!fecha) {

        return "-";

    }


    const partes =
        fecha.split("-");


    if (
        partes.length !== 3
    ) {

        return fecha;

    }


    return `${partes[2]}/${partes[1]}/${partes[0]}`;

}


// ===============================
// EXPOSICIÓN GLOBAL
// ===============================

window.cargarPeriodosModulo =
    cargarPeriodosModulo;