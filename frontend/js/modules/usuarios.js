// ===============================
// MÓDULO: USUARIOS - ADMIN
// ===============================

// ===============================
// CARGAR USUARIOS
// ===============================

async function cargarUsuarios() {

    try {

        console.log("Cargando módulo Usuarios...");

        const usuarios = await getUsuarios();

        const contenedor =
            document.getElementById("contenido");


        if (!contenedor) {

            console.error(
                "No existe el contenedor #contenido"
            );

            return;
        }


        if (!usuarios || usuarios.length === 0) {

            contenedor.innerHTML = `

                <h2>👥 Usuarios</h2>

                <div class="card">

                    <p>
                        No existen usuarios registrados.
                    </p>

                </div>

            `;

            return;
        }


        contenedor.innerHTML = `

            <h2>👥 Usuarios</h2>

            <p>
                Gestión de usuarios del sistema.
            </p>

            <div id="lista-usuarios">

                ${usuarios.map(usuario => `

                    <div class="card">

                        <strong>
                            ${usuario.nombre}
                            ${usuario.apellido}
                        </strong>

                        <br>

                        📧 ${usuario.email}

                        <br>

                        🎭 Rol:
                        ${usuario.rol}

                        <br>

                        Estado:

                        <strong>
                            ${
                                usuario.activo
                                ? "Activo"
                                : "Inactivo"
                            }
                        </strong>

                        <br><br>

                        <button
                            onclick="toggleUsuarioUI(${usuario.id})"
                        >
                            ${
                                usuario.activo
                                ? "Desactivar"
                                : "Activar"
                            }
                        </button>

                    </div>

                `).join("")}

            </div>

        `;

    }
    catch (error) {

        console.error(
            "Error usuarios:",
            error
        );

        mostrarError(
            "No se pudieron cargar los usuarios"
        );

    }

}


// ===============================
// ACTIVAR / DESACTIVAR USUARIO
// ===============================

async function toggleUsuarioUI(userId) {

    try {

        console.log(
            "Cambiando estado usuario:",
            userId
        );

        await toggleUsuario(userId);

        // Recargar lista
        await cargarUsuarios();

    }
    catch (error) {

        console.error(
            "Error cambiando estado:",
            error
        );

        alert(
            "No se pudo cambiar el estado del usuario."
        );

    }

}


// ===============================
// EXPOSICIÓN GLOBAL
// ===============================

window.cargarUsuarios =
    cargarUsuarios;

window.toggleUsuarioUI =
    toggleUsuarioUI;