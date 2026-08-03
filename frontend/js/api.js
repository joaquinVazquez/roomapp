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

function authHeaders() {

    const token = getToken();

    console.log("TOKEN ENVIADO:", token);

    return {
        "Authorization": `Bearer ${token}`
    };
}


// ==========================
// USUARIO
// ==========================

async function getCurrentUser() {

    const response = await fetch(`${API_URL}/users/me`, {
        headers: authHeaders()
    });

    if (!response.ok) {
        throw new Error("Error obteniendo usuario");
    }

    return await response.json();
}


// ==========================
// HORARIOS
// ==========================

async function getHorariosDocente() {

    const response = await fetch(
        `${API_URL}/horarios/mis-horarios-docente`,
        { headers: authHeaders() }
    );

    if (!response.ok) {
        throw new Error("Error horarios docente");
    }

    return await response.json();
}


async function getHorariosEstudiante() {

    const response = await fetch(
        `${API_URL}/horarios/mis-horarios-estudiante`,
        { headers: authHeaders() }
    );

    if (!response.ok) {
        throw new Error("Error horarios estudiante");
    }

    return await response.json();
}


async function getHorariosGenerales() {

    const response = await fetch(
        `${API_URL}/horarios/general`,
        { headers: authHeaders() }
    );

    if (!response.ok) {
        throw new Error("Error horarios generales");
    }

    return await response.json();
}


// ==========================
// EXPORT GLOBAL (CONTROLADO)
// ==========================

window.API = {
    getToken,
    requireAuth,
    getCurrentUser,
    getHorariosDocente,
    getHorariosEstudiante,
    getHorariosGenerales
};