async function cargarMiHorario(){


    const usuario =
    await getCurrentUser();



    let data;



    if(usuario.rol==="ESTUDIANTE"){


        data =
        await getHorariosEstudiante();


    }


    if(usuario.rol==="DOCENTE"){


        data =
        await getHorariosDocente();


    }



    mostrarHorarios(data);

}





async function cargarHorarioGeneral(){


    const data =
    await getHorariosGenerales();



    mostrarHorarios(data);


}

function mostrarHorarios(data){

    const contenedor = document.getElementById("contenido");

    contenedor.innerHTML = "";

    const dias = data.dias ?? data.horarios ?? [];

    // =========================
    // ESTADO VACÍO
    // =========================

    if(dias.length === 0){

        contenedor.innerHTML = `
            <p>No hay horarios disponibles</p>
        `;
        return;
    }


    // =========================
    // RENDER
    // =========================

    dias.forEach(dia => {

        const bloque = document.createElement("div");
        bloque.className = "dia";

        let clasesHTML = dia.clases.map(clase => `

            <div class="card">

                <div class="hora">
                    ${clase.hora}
                </div>

                <div class="materia">
                    ${clase.materia}
                </div>

                <div class="detalle">
                    Grupo: ${clase.grupo}
                </div>

                <div class="detalle">
                    Aula: 
                    ${
                        clase.aula === "SIN ASIGNAR"
                        ? `<span class="sin-aula">${clase.aula}</span>`
                        : clase.aula
                    }
                </div>

                ${
                    clase.docente
                    ? `<div class="detalle">Docente: ${clase.docente}</div>`
                    : ""
                }

            </div>

        `).join("");

        bloque.innerHTML = `
            <h2>${dia.dia}</h2>
            ${clasesHTML}
        `;

        contenedor.appendChild(bloque);

    });

}