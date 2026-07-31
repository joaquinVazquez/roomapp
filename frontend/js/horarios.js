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
    await getHorarioGeneral();



    mostrarHorarios(data);


}





function mostrarHorarios(data){


    const contenedor =
    document.getElementById(
        "contenido"
    );



    contenedor.innerHTML="";



    const dias =
    data.dias ??
    data.horarios;



    dias.forEach(dia=>{


        contenedor.innerHTML += `


        <h2>
        ${dia.dia}
        </h2>


        ${
        dia.clases.map(clase=>`


        <div class="card">


            <strong>
            ${clase.hora}
            </strong>


            <p>
            ${clase.materia}
            </p>


            <p>
            Grupo:
            ${clase.grupo}
            </p>


            <p>
            Aula:
            ${clase.aula}
            </p>


            ${
            clase.docente
            ?
            `<p>
            Docente:
            ${clase.docente}
            </p>`
            :
            ""
            }


        </div>


        `).join("")
        }


        `;


    });


}