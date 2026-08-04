// ===============================
// APP PRINCIPAL
// ===============================

document.addEventListener("DOMContentLoaded", async () => {

    try {

        // ==========================
        // 1. VALIDAR TOKEN
        // ==========================
        const token = localStorage.getItem("token");

        if (!token) {
            window.location.href = "/frontend/login.html";
            return;
        }

        // ==========================
        // 2. OBTENER USUARIO
        // ==========================
        const usuario = await getCurrentUser();

        // ==========================
        // 3. UI BASE
        // ==========================
        mostrarUsuario(usuario);
        crearMenuPorRol(usuario.rol);

        // ==========================
        // 4. PERIODOS
        // ==========================
        await cargarPeriodos();
        configurarSelectorPeriodo();

        // ==========================
        // 5. LOADING
        // ==========================
        mostrarLoading();

        // ==========================
        // 6. CARGA INICIAL
        // ==========================
        await cargarVistaInicial(usuario);

    } catch (error) {

        console.error("ERROR APP:", error);

        // 🔥 SOLO si es error de autenticación
        if (
            error.message.includes("401") ||
            error.message.includes("Unauthorized")
        ) {
            localStorage.removeItem("token");
            window.location.href = "/frontend/login.html";
        } else {
            mostrarError("Error cargando la aplicación");
        }
    }

});


// ===============================
// CONTROL DE VISTA INICIAL
// ===============================

async function cargarVistaInicial(usuario) {

    try {

        if (
            usuario.rol === "DOCENTE" ||
            usuario.rol === "ESTUDIANTE"
        ) {

            const data = await cargarMiHorario();
            mostrarHorarios(data);

        } else {

            const data = await getHorariosGenerales();
            mostrarHorarios(data);

        }

    } catch (error) {

        console.error("Error cargando vista:", error);
        mostrarError("No se pudo cargar la información");

    }

}


// ===============================
// SELECTOR DE PERIODO
// ===============================

function configurarSelectorPeriodo() {

    const selector = document.getElementById("selector-periodo");

    if (!selector) return;

    selector.addEventListener("change", async (e) => {

        const periodoId = e.target.value;

        localStorage.setItem("periodo_id", periodoId);

        mostrarLoading();

        try {

            await cargarModulo("horario");

        } catch (error) {

            console.error("Error cambiando periodo:", error);
            mostrarError("Error al cambiar periodo");

        }

    });

}


// ===============================
// PERIODOS
// ===============================

async function cargarPeriodos(){

    console.log("INICIANDO cargarPeriodos");


    const select = document.getElementById("selector-periodo");


    console.log(
        "SELECTOR:",
        select
    );


    if(!select) return;


    try{

        const periodos = await getPeriodos();


        console.log(
            "PERIODOS RECIBIDOS:",
            periodos
        );


        if(!periodos || periodos.length === 0){
            console.warn("No existen periodos");
            return;
        }


        select.innerHTML = periodos.map(p => `
            <option value="${p.id}">
                ${p.nombre}
            </option>
        `).join("");


        localStorage.setItem(
            "periodo_id",
            periodos[0].id
        );


        console.log(
            "PERIODO GUARDADO:",
            localStorage.getItem("periodo_id")
        );


    }
    catch(error){

        console.error(
            "ERROR PERIODOS:",
            error
        );

    }

}


// ===============================
// INFORMACIÓN DEL USUARIO
// ===============================

function mostrarUsuario(usuario) {

    const elemento = document.getElementById("usuario-info");

    if (!elemento) return;

    elemento.innerHTML = `
        Usuario: <strong>${usuario.email}</strong><br>
        Rol: ${usuario.rol}
    `;
}


// ===============================
// UI: LOADING
// ===============================

function mostrarLoading() {

    const contenedor = document.getElementById("contenido");

    if (!contenedor) return;

    contenedor.innerHTML = `
        <div style="text-align:center;padding:40px;">
            <div class="spinner"></div>
            <p id="loading">Cargando información...</p>
        </div>
    `;
}


// ===============================
// UI: ERROR
// ===============================

function mostrarError(mensaje = "Ocurrió un error") {

    const contenedor = document.getElementById("contenido");

    if (!contenedor) return;

    contenedor.innerHTML = `
        <div style="text-align:center;padding:40px;color:red;">
            <h3>⚠️ Error</h3>
            <p>${mensaje}</p>
        </div>
    `;
}


// ===============================
// EXPOSICIÓN GLOBAL CONTROLADA
// ===============================

window.cargarMiHorario = cargarMiHorario;
window.mostrarHorarios = mostrarHorarios;
window.cargarModulo = cargarModulo;