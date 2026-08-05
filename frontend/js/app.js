// ======================================
// APP PRINCIPAL - ROOMAPP
// ======================================

document.addEventListener("DOMContentLoaded", iniciarAplicacion);


// ======================================
// INICIO
// ======================================

async function iniciarAplicacion() {

    try {

        validarSesion();

        // Obtener usuario una sola vez
        const usuario = await getCurrentUser();

        // Guardar usuario en memoria
        window.currentUser = usuario;

        // Construir interfaz
        mostrarUsuario(usuario);
        crearMenuPorRol(usuario.rol);

        // Marcar automáticamente el primer botón
        if (typeof activarPrimerBoton === "function") {
            activarPrimerBoton();
        }

        // Periodos
        await cargarPeriodos();

        configurarSelectorPeriodo();

        // Cargar vista inicial
        await cargarVistaInicial(usuario);

    }
    catch (error) {

        console.error("ERROR APP:", error);

        if (
            error.message.includes("401") ||
            error.message.includes("Unauthorized")
        ) {

            logout();
            return;

        }

        mostrarError("No fue posible iniciar la aplicación.");

    }

}



// ======================================
// VALIDAR SESIÓN
// ======================================

function validarSesion() {

    const token = getToken();

    if (!token) {

        window.location.href = "/frontend/login.html";
        throw new Error("Sin sesión");

    }

}



// ======================================
// VISTA INICIAL
// ======================================

async function cargarVistaInicial(usuario) {

    mostrarLoading();

    try {

        if (
            usuario.rol === "DOCENTE" ||
            usuario.rol === "ESTUDIANTE"
        ) {

            const data = await cargarMiHorario();

            mostrarHorarios(data);

        }
        else {

            const data = await getHorariosGenerales();

            mostrarHorarios(data);

        }

    }
    catch (error) {

        console.error(error);

        mostrarError(
            "No fue posible cargar la información."
        );

    }

}



// ======================================
// SELECTOR DE PERIODO
// ======================================

function configurarSelectorPeriodo() {

    const selector =
        document.getElementById(
            "selector-periodo"
        );

    if (!selector) return;


    selector.addEventListener(
        "change",
        async (e) => {

            localStorage.setItem(
                "periodo_id",
                e.target.value
            );

            await cargarModulo("horario");

        }
    );

}



// ======================================
// CARGAR PERIODOS
// ======================================

async function cargarPeriodos() {

    const selector =
        document.getElementById(
            "selector-periodo"
        );

    if (!selector) return;

    try {

        const periodos =
            await getPeriodos();

        if (
            !periodos ||
            periodos.length === 0
        ) {

            selector.innerHTML =
                "<option>No hay periodos</option>";

            return;

        }

        selector.innerHTML =
            periodos.map(p => `

                <option value="${p.id}">
                    ${p.nombre}
                </option>

            `).join("");

        localStorage.setItem(
            "periodo_id",
            periodos[0].id
        );

    }
    catch (error) {

        console.error(error);

    }

}



// ======================================
// INFORMACIÓN DEL USUARIO
// ======================================

function mostrarUsuario(usuario) {

    const elemento =
        document.getElementById(
            "usuario-info"
        );

    if (!elemento) return;

    elemento.innerHTML = `

        <strong>${usuario.email}</strong>

        <br>

        ${usuario.rol}

    `;

}



// ======================================
// LOADING
// ======================================

function mostrarLoading() {

    const contenedor =
        document.getElementById(
            "contenido"
        );

    if (!contenedor) return;

    contenedor.innerHTML = `

        <div style="text-align:center;padding:40px;">

            <div class="spinner"></div>

            <p id="loading">
                Cargando...
            </p>

        </div>

    `;

}



// ======================================
// ERROR
// ======================================

function mostrarError(
    mensaje = "Ocurrió un error"
) {

    const contenedor =
        document.getElementById(
            "contenido"
        );

    if (!contenedor) return;

    contenedor.innerHTML = `

        <div
            style="
                text-align:center;
                padding:40px;
                color:red;
            "
        >

            <h2>⚠️ Error</h2>

            <p>${mensaje}</p>

        </div>

    `;

}



// ======================================
// EXPOSICIÓN GLOBAL
// ======================================

window.mostrarLoading = mostrarLoading;
window.mostrarError = mostrarError;
window.cargarModulo = cargarModulo;