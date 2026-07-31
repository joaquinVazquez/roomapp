async function redirectByRole(){


    try{


        const user = await getCurrentUser();



        switch(user.rol){


            case "ADMINISTRADOR":

                window.location.href =
                "admin/dashboard.html";

            break;



            case "COORDINADOR_ACADEMICO":

                window.location.href =
                "coordinador/dashboard.html";

            break;



            case "DOCENTE":

                window.location.href =
                "docente/horarios.html";

            break;



            case "ESTUDIANTE":

                window.location.href =
                "estudiante/horarios.html";

            break;



            case "PERSONAL_ADMINISTRATIVO":

                window.location.href =
                "administrativo/horarios.html";

            break;



            default:

                alert(
                "Rol no configurado"
                );

        }



    }catch(error){

        console.error(error);

        alert(
        "No se pudo identificar usuario"
        );

    }

}