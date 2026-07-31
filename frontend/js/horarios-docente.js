document.addEventListener(
"DOMContentLoaded",
async()=>{


const container =
document.getElementById(
"horarios-container"
);


try{


const data =
await getHorariosDocente();


console.log(
"RESPUESTA DOCENTE:",
data
);



const dias =
data.horarios || data.dias || [];



container.innerHTML="";



dias.forEach(dia=>{


container.innerHTML+=
`

<h2>${dia.dia}</h2>


${dia.clases.map(c=>`

<div class="card">

<h3>${c.materia}</h3>

<p>
⏰ ${c.hora}
</p>

<p>
🏫 Aula: ${c.aula}
</p>

<p>
👥 Grupo: ${c.grupo}
</p>


</div>


`).join("")}


`;

});


}
catch(e){


console.error(
"ERROR COMPLETO:",
e
);


container.innerHTML=
"Error cargando horario";


}


});