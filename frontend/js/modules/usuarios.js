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
            console.error("No existe #contenido");
            return;
        }

        if (!usuarios || usuarios.length === 0) {

            contenedor.innerHTML = `
                <h2>👥 Usuarios</h2>

                <div class="card">
                    <p>No existen usuarios registrados.</p>
                </div>
            `;
            return;
        }

        contenedor.innerHTML = `

            <h2>👥 Usuarios</h2>

            <button onclick="mostrarFormularioCrear()" class="btn-primary">
                + Nuevo Usuario
            </button>

            <br><br>

            <table class="tabla-usuarios">

                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Email</th>
                        <th>Rol</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>

                <tbody>

                    ${usuarios.map(usuario => `

                        <tr>

                            <td>
                                ${usuario.nombre} ${usuario.apellido}
                            </td>

                            <td>${usuario.email}</td>

                            <td>${usuario.rol}</td>

                            <td>
                                <strong>
                                    ${usuario.activo ? "Activo" : "Inactivo"}
                                </strong>
                            </td>

                            <td>

                                <button onclick="editarUsuario(${usuario.id})">
                                    ✏️
                                </button>

                                <button onclick="toggleUsuarioUI(${usuario.id})">
                                    ${usuario.activo ? "⛔" : "✅"}
                                </button>

                                <button onclick="eliminarUsuario(${usuario.id})">
                                    🗑
                                </button>

                            </td>

                        </tr>

                    `).join("")}

                </tbody>

            </table>
        `;

    }
    catch (error) {

        console.error("Error usuarios:", error);

        mostrarError("No se pudieron cargar los usuarios");

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
// NUEVO USUARIO (FASE SIGUIENTE)
// ===============================

function mostrarFormularioCrear() {
    alert("Aquí irá el formulario de creación");
}

// ===============================
// EDITAR USUARIO
// ===============================

function editarUsuario(id) {
    alert("Editar usuario ID: " + id);
}

// ===============================
// ELIMINAR USUARIO
// ===============================

function eliminarUsuario(id) {
    alert("Eliminar usuario ID: " + id);
}


// ===============================
// EXPOSICIÓN GLOBAL
// ===============================

window.cargarUsuarios =
    cargarUsuarios;

window.toggleUsuarioUI =
    toggleUsuarioUI;

window.mostrarFormularioCrear = mostrarFormularioCrear;
window.editarUsuario = editarUsuario;
window.eliminarUsuario = eliminarUsuario;