document.addEventListener("DOMContentLoaded", async () => {

    requireAuth();

    const container = document.getElementById("horarios-container");

    try {

        const data = await getHorariosDocente();

        const dias = data.dias || data.horarios || [];

        container.innerHTML = "";

        dias.forEach(dia => {

            let html = `<h2>${dia.dia}</h2>`;

            dia.clases.forEach(c => {

                html += `
                <div class="card">
                    <h3>${c.materia}</h3>
                    <p>⏰ ${c.hora}</p>
                    <p>🏫 ${c.aula}</p>
                    <p>👥 ${c.grupo}</p>
                </div>
                `;
            });

            container.innerHTML += html;
        });

    } catch (e) {

        console.error(e);
        container.innerHTML = "Error cargando horario";
    }
});