// =====================================================
// ROOMAPP - API CLIENT
// =====================================================


// =====================================================
// CONFIGURACIÓN
// =====================================================

const API_URL = "http://127.0.0.1:8000";


// =====================================================
// TOKEN
// =====================================================

function getToken() {

    return localStorage.getItem("token");

}


// =====================================================
// AUTENTICACIÓN
// =====================================================

function requireAuth() {

    const token = getToken();


    if (!token) {

        window.location.href =
            "/frontend/login.html";

        return null;
    }


    return token;

}


// =====================================================
// HEADERS DE AUTENTICACIÓN
// =====================================================

function authHeaders() {

    const token = getToken();


    if (!token) {

        return {};

    }


    return {

        "Authorization":
            `Bearer ${token}`

    };

}


// =====================================================
// CORE REQUEST
// =====================================================

async function apiRequest(
    endpoint,
    method = "GET",
    body = null
) {

    const token = getToken();


    // ---------------------------------------------
    // CONFIGURACIÓN DE LA PETICIÓN
    // ---------------------------------------------

    const options = {

        method: method,

        headers: {

            "Authorization":
                `Bearer ${token}`,

            "Content-Type":
                "application/json"

        }

    };


    // ---------------------------------------------
    // BODY
    // ---------------------------------------------

    if (body !== null) {

        options.body =
            JSON.stringify(body);

    }


    // ---------------------------------------------
    // DEBUG
    // ---------------------------------------------

    console.log(
        `${method} ${API_URL}${endpoint}`
    );


    // ---------------------------------------------
    // FETCH
    // ---------------------------------------------

    const response =
        await fetch(
            `${API_URL}${endpoint}`,
            options
        );


    // ---------------------------------------------
    // TOKEN EXPIRADO / NO AUTORIZADO
    // ---------------------------------------------

    if (response.status === 401) {

        console.warn(
            "Sesión expirada o token inválido"
        );


        localStorage.removeItem(
            "token"
        );


        window.location.href =
            "/frontend/login.html";


        throw new Error(
            "401 Unauthorized"
        );

    }


    // ---------------------------------------------
    // OTROS ERRORES
    // ---------------------------------------------

    if (!response.ok) {

        let detalle = "";


        try {

            detalle =
                await response.text();

        }
        catch {

            detalle =
                "Sin detalles";

        }


        console.error(
            "Error API:",
            response.status,
            detalle
        );


        throw new Error(
            `Error API ${response.status}: ${detalle}`
        );

    }


    // ---------------------------------------------
    // RESPUESTA VACÍA
    // ---------------------------------------------

    if (
        response.status === 204
    ) {

        return null;

    }


    // ---------------------------------------------
    // JSON
    // ---------------------------------------------

    return await response.json();

}


// =====================================================
// USUARIO ACTUAL
// =====================================================

async function getCurrentUser() {

    return await apiRequest(
        "/users/me"
    );

}


// =====================================================
// USUARIOS - ADMINISTRACIÓN
// =====================================================

async function getUsuarios() {

    return await apiRequest(
        "/users/"
    );

}

// =====================================================
// CREAR USUARIO
// =====================================================

async function crearUsuario(usuario) {

    return await apiRequest(
        "/users/",
        "POST",
        usuario
    );

}

// =====================================================
// ACTIVAR / DESACTIVAR USUARIO
// =====================================================

async function toggleUsuario(
    userId
) {

    return await apiRequest(
        `/users/${userId}/toggle`,
        "PATCH"
    );

}


// =====================================================
// HORARIOS - DOCENTE
// =====================================================

async function getHorariosDocente() {

    let periodoId =
        localStorage.getItem(
            "periodo_id"
        );


    // ---------------------------------------------
    // FALLBACK
    // ---------------------------------------------

    if (!periodoId) {

        console.warn(
            "No existe periodo_id. Obteniendo periodo por defecto."
        );


        const periodos =
            await getPeriodos();


        if (
            !periodos ||
            periodos.length === 0
        ) {

            throw new Error(
                "No existen periodos académicos disponibles"
            );

        }


        periodoId =
            periodos[0].id;


        localStorage.setItem(
            "periodo_id",
            periodoId
        );

    }


    return await apiRequest(
        `/horarios/mis-horarios-docente?periodo_id=${periodoId}`
    );

}


// =====================================================
// HORARIOS - ESTUDIANTE
// =====================================================

async function getHorariosEstudiante() {

    let periodoId =
        localStorage.getItem(
            "periodo_id"
        );


    // ---------------------------------------------
    // FALLBACK
    // ---------------------------------------------

    if (!periodoId) {

        console.warn(
            "No existe periodo_id. Obteniendo periodo por defecto."
        );


        const periodos =
            await getPeriodos();


        if (
            !periodos ||
            periodos.length === 0
        ) {

            throw new Error(
                "No existen periodos académicos disponibles"
            );

        }


        periodoId =
            periodos[0].id;


        localStorage.setItem(
            "periodo_id",
            periodoId
        );

    }


    return await apiRequest(
        `/horarios/mis-horarios-estudiante?periodo_id=${periodoId}`
    );

}


// =====================================================
// HORARIO GENERAL
// =====================================================

async function getHorariosGenerales() {

    let periodoId =
        localStorage.getItem(
            "periodo_id"
        );


    // ---------------------------------------------
    // FALLBACK
    // ---------------------------------------------

    if (!periodoId) {

        console.warn(
            "No existe periodo_id. Obteniendo periodo por defecto."
        );


        const periodos =
            await getPeriodos();


        if (
            !periodos ||
            periodos.length === 0
        ) {

            throw new Error(
                "No existen periodos académicos disponibles"
            );

        }


        periodoId =
            periodos[0].id;


        localStorage.setItem(
            "periodo_id",
            periodoId
        );

    }


    return await apiRequest(
        `/horarios/general?periodo_id=${periodoId}`
    );

}


// =====================================================
// PERIODOS ACADÉMICOS
// =====================================================

async function getPeriodos() {

    return await apiRequest(
        "/periodos-academicos/"
    );

}


// =====================================================
// LOGOUT
// =====================================================

function logout() {

    localStorage.removeItem(
        "token"
    );


    localStorage.removeItem(
        "periodo_id"
    );


    window.location.href =
        "/frontend/login.html";

}


// =====================================================
// EXPOSICIÓN GLOBAL
// =====================================================
//
// Actualmente RoomApp todavía utiliza scripts
// tradicionales y el router necesita acceder a
// determinadas funciones desde otros archivos.
//
// Más adelante podremos migrar a ES Modules.
//

window.getToken =
    getToken;


window.requireAuth =
    requireAuth;


window.authHeaders =
    authHeaders;


window.apiRequest =
    apiRequest;


window.getCurrentUser =
    getCurrentUser;


window.getUsuarios =
    getUsuarios;


window.toggleUsuario =
    toggleUsuario;


window.getHorariosDocente =
    getHorariosDocente;


window.getHorariosEstudiante =
    getHorariosEstudiante;


window.getHorariosGenerales =
    getHorariosGenerales;


window.getPeriodos =
    getPeriodos;


window.logout =
    logout;

window.crearUsuario = crearUsuario;


// =====================================================
// OBJETO API
// =====================================================

window.API = {

    getToken,

    requireAuth,

    authHeaders,

    apiRequest,

    getCurrentUser,

    getUsuarios,

    crearUsuario,

    toggleUsuario,

    getHorariosDocente,

    getHorariosEstudiante,

    getHorariosGenerales,

    getPeriodos,

    logout

};