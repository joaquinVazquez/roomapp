const API_URL = "http://127.0.0.1:8000";


// ==========================
// TOKEN
// ==========================

function getToken() {
    return localStorage.getItem("token");
}

function requireAuth() {

    const token = getToken();

    if (!token) {
        window.location.href = "/frontend/login.html";
        return null;
    }

    return token;
}


// ==========================
// CORE REQUEST (🔥 CLAVE)
// ==========================

async function apiRequest(endpoint) {

    const token = getToken();

    const response = await fetch(`${API_URL}${endpoint}`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    // 🔥 manejo centralizado
    if (response.status === 401) {

        console.warn("Sesión expirada");

        localStorage.removeItem("token");
        window.location.href = "/frontend/login.html";

        throw new Error("401 Unauthorized");
    }

    if (!response.ok) {
        throw new Error(`Error API: ${endpoint}`);
    }

    return await response.json();
}


// ==========================
// USUARIO
// ==========================

async function getCurrentUser() {
    return await apiRequest("/users/me");
}


// ==========================
// HORARIOS
// ==========================

async function getHorariosDocente() {

    let periodoId = localStorage.getItem("periodo_id");

    // 🔥 fallback de seguridad
    if (!periodoId) {

        console.warn("No hay periodo_id, obteniendo por defecto...");

        const periodos = await getPeriodos();

        if (!periodos || periodos.length === 0) {
            throw new Error("No hay periodos disponibles");
        }

        periodoId = periodos[0].id;
        localStorage.setItem("periodo_id", periodoId);
    }

    return await apiRequest(
        `/horarios/mis-horarios-docente?periodo_id=${periodoId}`
    );
}


async function getHorariosEstudiante() {

    let periodoId = localStorage.getItem("periodo_id");

    if (!periodoId) {

        const periodos = await getPeriodos();

        if (!periodos || periodos.length === 0) {
            throw new Error("No hay periodos disponibles");
        }

        periodoId = periodos[0].id;
        localStorage.setItem("periodo_id", periodoId);
    }

    return await apiRequest(
        `/horarios/mis-horarios-estudiante?periodo_id=${periodoId}`
    );
}


async function getHorariosGenerales() {

    return await apiRequest("/horarios/general");
}


// ==========================
// PERIODOS
// ==========================

async function getPeriodos() {

    return await apiRequest("/periodos-academicos");
}


// ==========================
// EXPORT GLOBAL
// ==========================

window.API = {
    getToken,
    requireAuth,
    getCurrentUser,
    getHorariosDocente,
    getHorariosEstudiante,
    getHorariosGenerales,
    getPeriodos
};