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


        // =========================
        // SIN USUARIOS
        // =========================

        if (!usuarios || usuarios.length === 0) {

            contenedor.innerHTML = `

                <h2>👥 Usuarios</h2>

                <button
                    onclick="mostrarFormularioCrear()"
                    class="btn-primary"
                >
                    + Nuevo Usuario
                </button>

                <br><br>

                <div class="card">

                    <p>
                        No existen usuarios registrados.
                    </p>

                </div>

            `;

            return;
        }


        // =========================
        // TABLA
        // =========================

        contenedor.innerHTML = `

            <h2>👥 Usuarios</h2>

            <button
                onclick="mostrarFormularioCrear()"
                class="btn-primary"
            >
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
                                ${usuario.nombre ?? ""}
                                ${usuario.apellido ?? ""}
                            </td>

                            <td>
                                ${usuario.email}
                            </td>

                            <td>
                                ${usuario.rol}
                            </td>

                            <td>

                                <strong>
                                    ${
                                        usuario.activo
                                        ? "Activo"
                                        : "Inactivo"
                                    }
                                </strong>

                            </td>

                            <td>

                                <button
                                    onclick="editarUsuario(${usuario.id})"
                                >
                                    ✏️
                                </button>


                                <button
                                    onclick="toggleUsuarioUI(${usuario.id})"
                                >
                                    ${
                                        usuario.activo
                                        ? "⛔"
                                        : "✅"
                                    }
                                </button>


                                <button
                                    onclick="eliminarUsuario(${usuario.id})"
                                >
                                    🗑️
                                </button>

                            </td>

                        </tr>

                    `).join("")}

                </tbody>

            </table>

        `;

    }
    catch (error) {

        console.error(
            "Error usuarios:",
            error
        );

        mostrarError(
            "No se pudieron cargar los usuarios."
        );

    }

}


// ===============================
// ACTIVAR / DESACTIVAR
// ===============================

async function toggleUsuarioUI(userId) {

    try {

        console.log(
            "Cambiando estado usuario:",
            userId
        );


        await toggleUsuario(userId);


        // Recargar tabla

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
// FORMULARIO CREAR USUARIO
// ===============================

function mostrarFormularioCrear() {

    const contenedor =
        document.getElementById("contenido");


    if (!contenedor) return;


    contenedor.innerHTML = `

        <h2>👤 Nuevo Usuario</h2>


        <div class="card">

            <form
                id="form-crear-usuario"
            >


                <!-- NOMBRE -->

                <div class="form-group">

                    <label for="nuevo-nombre">
                        Nombre
                    </label>

                    <input
                        type="text"
                        id="nuevo-nombre"
                        required
                    >

                </div>


                <!-- APELLIDO -->

                <div class="form-group">

                    <label for="nuevo-apellido">
                        Apellido
                    </label>

                    <input
                        type="text"
                        id="nuevo-apellido"
                        required
                    >

                </div>


                <!-- EMAIL -->

                <div class="form-group">

                    <label for="nuevo-email">
                        Correo electrónico
                    </label>

                    <input
                        type="email"
                        id="nuevo-email"
                        required
                    >

                </div>


                <!-- PASSWORD -->

                <div class="form-group">

                    <label for="nuevo-password">
                        Contraseña
                    </label>

                    <input
                        type="password"
                        id="nuevo-password"
                        required
                        minlength="6"
                    >

                </div>


                <!-- ROL -->

                <div class="form-group">

                    <label for="nuevo-rol">
                        Rol
                    </label>

                    <select
                        id="nuevo-rol"
                        required
                    >

                        <option value="">
                            Seleccionar rol
                        </option>

                        <option value="1">
                            Administrador
                        </option>

                        <option value="2">
                            Coordinador académico
                        </option>

                        <option value="3">
                            Docente
                        </option>

                        <option value="4">
                            Estudiante
                        </option>

                        <option value="5">
                            Personal administrativo
                        </option>

                    </select>

                </div>


                <br>


                <!-- BOTONES -->

                <button
                    type="submit"
                    class="btn-primary"
                >
                    Crear usuario
                </button>


                <button
                    type="button"
                    onclick="cargarUsuarios()"
                >
                    Cancelar
                </button>


            </form>

        </div>

    `;


    // =========================
    // EVENTO FORMULARIO
    // =========================

    const formulario =
        document.getElementById(
            "form-crear-usuario"
        );


    formulario.addEventListener(
        "submit",
        crearUsuarioUI
    );

}


// ===============================
// PROCESAR CREACIÓN
// ===============================

async function crearUsuarioUI(event) {

    event.preventDefault();


    try {

        const nombre =
            document.getElementById(
                "nuevo-nombre"
            ).value.trim();


        const apellido =
            document.getElementById(
                "nuevo-apellido"
            ).value.trim();


        const email =
            document.getElementById(
                "nuevo-email"
            ).value.trim();


        const password =
            document.getElementById(
                "nuevo-password"
            ).value;


        const rolId =
            Number(
                document.getElementById(
                    "nuevo-rol"
                ).value
            );


        // =========================
        // VALIDACIONES
        // =========================

        if (!nombre || !apellido) {

            alert(
                "Nombre y apellido son obligatorios."
            );

            return;
        }


        if (!email) {

            alert(
                "El correo electrónico es obligatorio."
            );

            return;
        }


        if (password.length < 6) {

            alert(
                "La contraseña debe tener al menos 6 caracteres."
            );

            return;
        }


        if (!rolId) {

            alert(
                "Selecciona un rol."
            );

            return;
        }


        // =========================
        // DATOS
        // =========================

        const usuario = {

            nombre: nombre,

            apellido: apellido,

            email: email,

            password: password,

            rol_id: rolId

        };


        console.log(
            "Creando usuario:",
            {
                ...usuario,
                password: "***"
            }
        );


        // =========================
        // API
        // =========================

        await crearUsuario(usuario);


        // =========================
        // ÉXITO
        // =========================

        alert(
            "Usuario creado correctamente."
        );


        // Volver a la tabla

        await cargarUsuarios();

    }
    catch (error) {

        console.error(
            "Error creando usuario:",
            error
        );


        alert(
            "No se pudo crear el usuario.\n\n" +
            error.message
        );

    }

}


// ===============================
// EDITAR USUARIO
// ===============================
// MVP: pendiente

function editarUsuario(id) {

    alert(
        "La edición de usuarios se implementará posteriormente.\n\n" +
        "Usuario ID: " + id
    );

}


// ===============================
// ELIMINAR USUARIO
// ===============================
// MVP: pendiente

function eliminarUsuario(id) {

    alert(
        "La eliminación de usuarios se implementará posteriormente.\n\n" +
        "Usuario ID: " + id
    );

}


// ===============================
// EXPOSICIÓN GLOBAL
// ===============================

window.cargarUsuarios =
    cargarUsuarios;


window.toggleUsuarioUI =
    toggleUsuarioUI;


window.mostrarFormularioCrear =
    mostrarFormularioCrear;


window.crearUsuarioUI =
    crearUsuarioUI;


window.editarUsuario =
    editarUsuario;


window.eliminarUsuario =
    eliminarUsuario;