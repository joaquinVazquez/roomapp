// ===============================
// MODULO USUARIOS ADMIN
// ===============================


async function cargarUsuarios(){


    try{


        const usuarios =
            await getUsuarios();



        mostrarUsuarios(
            usuarios
        );


    }
    catch(error){

        console.error(
            "Error usuarios:",
            error
        );


        mostrarError(
            "No se pudieron cargar usuarios"
        );

    }

}





function mostrarUsuarios(usuarios){


    const contenedor =
        document.getElementById(
            "contenido"
        );


    if(!contenedor)
        return;



    let html = `

        <h2>
            👥 Gestión de Usuarios
        </h2>


        <table>

            <thead>

                <tr>

                    <th>
                    Nombre
                    </th>

                    <th>
                    Email
                    </th>

                    <th>
                    Rol
                    </th>

                    <th>
                    Estado
                    </th>

                </tr>

            </thead>


            <tbody>

    `;



    usuarios.forEach(usuario=>{


        html += `

            <tr>

                <td>
                ${usuario.nombre}
                ${usuario.apellido}
                </td>


                <td>
                ${usuario.email}
                </td>


                <td>
                ${usuario.rol}
                </td>


                <td>
                ${
                    usuario.activo
                    ?
                    "Activo"
                    :
                    "Inactivo"
                }
                </td>


            </tr>


        `;


    });



    html += `

            </tbody>

        </table>

    `;


    contenedor.innerHTML = html;

}


window.cargarUsuarios = cargarUsuarios;