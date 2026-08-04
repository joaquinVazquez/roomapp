// ===============================
// HORARIOS
// ===============================


async function cargarMiHorario(){

    try {

        const usuario = await getCurrentUser();


        if(usuario.rol === "ESTUDIANTE"){

            return await getHorariosEstudiante();

        }


        if(usuario.rol === "DOCENTE"){

            return await getHorariosDocente();

        }


        return {
            dias:[]
        };


    }
    catch(error){

        console.error(
            "Error cargando horario:",
            error
        );

        mostrarError(
            "No fue posible cargar el horario"
        );

        return {
            dias:[]
        };

    }

}



// ===============================
// HORARIO GENERAL
// ===============================

async function cargarHorarioGeneral(){

    try{

        const data =
            await getHorariosGenerales();


        mostrarHorarios(data);


    }
    catch(error){

        console.error(error);

        mostrarError(
            "Error cargando horario general"
        );

    }

}



// ===============================
// RENDER HORARIOS
// ===============================

function mostrarHorarios(data){


    const contenedor =
        document.getElementById(
            "contenido"
        );


    if(!contenedor){
        return;
    }


    if(!data){

        mostrarError(
            "No se recibieron datos"
        );

        return;

    }


    const dias =
        data.dias ??
        data.horarios ??
        [];



    if(dias.length === 0){

        contenedor.innerHTML = `

            <div style="
                text-align:center;
                padding:40px;
            ">

                <h3>
                📭 Sin horarios
                </h3>

                <p>
                No hay información disponible
                </p>

            </div>

        `;

        return;

    }



    contenedor.innerHTML = "";



    dias.forEach(dia=>{


        const bloque =
            document.createElement(
                "div"
            );


        bloque.className =
            "dia";



        let html = `

            <h2>
                ${dia.dia}
            </h2>

        `;



        dia.clases.forEach(clase=>{


            html += `

            <div class="card">


                <div class="hora">
                    ⏰ ${clase.hora}
                </div>


                <div class="materia">
                    ${clase.materia}
                </div>


                <div class="detalle">
                    👥 Grupo:
                    ${clase.grupo}
                </div>


                <div class="detalle">
                    🏫 Aula:

                    ${
                    clase.aula === "SIN ASIGNAR"
                    ?
                    `<span class="sin-aula">
                    SIN ASIGNAR
                    </span>`
                    :
                    clase.aula
                    }

                </div>


                ${
                clase.docente
                ?
                `
                <div class="detalle">
                    👨‍🏫
                    ${clase.docente}
                </div>
                `
                :
                ""
                }


            </div>

            `;


        });



        bloque.innerHTML = html;


        contenedor.appendChild(
            bloque
        );


    });


}



// ===============================
// ERROR
// ===============================

function mostrarError(
    mensaje="Ocurrió un error"
){


    const contenedor =
        document.getElementById(
            "contenido"
        );


    if(!contenedor){
        return;
    }



    contenedor.innerHTML = `

        <div style="
            text-align:center;
            padding:40px;
            color:red;
        ">

            <h3>
            ⚠️ Error
            </h3>

            <p>
            ${mensaje}
            </p>

        </div>

    `;

}