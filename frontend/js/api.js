const API_URL = "http://127.0.0.1:8000";


function getToken(){

    return localStorage.getItem("token");

}


function requireAuth(){

    const token = getToken();

    if(!token){

        window.location.href="../login.html";
        return null;

    }

    return token;

}


// ==========================
// USUARIO ACTUAL
// ==========================

async function getCurrentUser(){

    const token = requireAuth();

    const response = await fetch(
        `${API_URL}/users/me`,
        {
            headers:{
                "Authorization": `Bearer ${token}`
            }
        }
    );


    if(!response.ok){

        throw new Error("Error obteniendo usuario");

    }


    return await response.json();

}



// ==========================
// HORARIO ESTUDIANTE
// ==========================

async function getHorariosEstudiante(){

    const token = requireAuth();


    const response = await fetch(
        `${API_URL}/horarios/mis-horarios-estudiante`,
        {
            headers:{
                "Authorization":`Bearer ${token}`
            }
        }
    );


    if(!response.ok){

        throw new Error("Error horarios estudiante");

    }


    return await response.json();

}



// ==========================
// HORARIO DOCENTE
// ==========================

async function getHorariosDocente(){

    const token = requireAuth();


    const response = await fetch(
        `${API_URL}/horarios/mis-horarios-docente`,
        {
            headers:{
                "Authorization":`Bearer ${token}`
            }
        }
    );


    if(!response.ok){

        throw new Error("Error horarios docente");

    }


    return await response.json();

}



// ==========================
// HORARIO GENERAL
// ==========================

async function getHorariosGenerales(){

    const token = requireAuth();


    const response = await fetch(
        `${API_URL}/horarios/general`,
        {
            headers:{
                "Authorization":`Bearer ${token}`
            }
        }
    );


    if(!response.ok){

    const errorText = await response.text();

    console.error(
        "STATUS:",
        response.status
    );

    console.error(
        "ERROR API:",
        errorText
    );


    throw new Error(
        errorText
    );

}
}