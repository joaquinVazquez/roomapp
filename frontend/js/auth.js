function saveToken(token) {
    localStorage.setItem("token", token);
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "../login.html";
}

function requireAuth() {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "../login.html";
        return null;
    }

    return token;
}

// ==========================
// LOGIN
// ==========================
async function login(email, password) {

    const response = await fetch(
        "http://127.0.0.1:8000/login",
        {
            method: "POST",
            headers: {
                "Content-Type":
                "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: email,
                password: password
            })
        }
    );

    if (!response.ok) {
        throw new Error("Credenciales incorrectas");
    }

    const data = await response.json();

    saveToken(data.access_token);

    return data;
}