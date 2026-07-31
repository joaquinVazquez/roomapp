document.addEventListener(
"DOMContentLoaded",
async()=>{


const container =
document.getElementById(
"horarios-container"
);



try{


const data =
await getHorariosEstudiante();



container.innerHTML="";



data.dias.forEach(dia=>{


let html=`

<h2>${dia.dia}</h2>

`;



dia.clases.forEach(clase=>{


html+=`

<div class="card">

<h3>${clase.materia}</h3>

<p>
⏰ ${clase.hora}
</p>

<p>
👨‍🏫 ${clase.docente}
</p>

<p>
🏫 ${clase.aula}
</p>

<p>
👥 ${clase.grupo}
</p>


</div>


`;


});



container.innerHTML+=html;


});



}
catch(error){


container.innerHTML=
"Error cargando horario";


console.error(error);


}



});