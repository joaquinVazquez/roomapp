from app.db.session import SessionLocal

from app.services.notificacion_service import (
    obtener_no_leidas,
    marcar_todas_leidas,
    contar_no_leidas
)



def run():

    db = SessionLocal()


    print("\n--- TEST ESTADO NOTIFICACIONES ---\n")


    # Usuario estudiante del seed
    usuario_id = 7


    # =================================
    # 1. CONTAR PENDIENTES
    # =================================

    cantidad = contar_no_leidas(
        db=db,
        usuario_id=usuario_id
    )


    print(
        "Notificaciones pendientes:",
        cantidad
    )



    # =================================
    # 2. OBTENER NO LEIDAS
    # =================================

    notificaciones = obtener_no_leidas(
        db=db,
        usuario_id=usuario_id
    )


    print("\nListado pendientes:\n")


    for n in notificaciones:

        print("----------------")

        print("ID:", n.id)

        print("Mensaje:", n.mensaje)

        print("Tipo:", n.tipo_evento)

        print("Leído:", n.leido)



    # =================================
    # 3. MARCAR TODAS LEIDAS
    # =================================

    actualizadas = marcar_todas_leidas(
        db=db,
        usuario_id=usuario_id
    )


    print(
        "\nMarcadas como leídas:",
        actualizadas
    )



    # =================================
    # 4. VALIDAR
    # =================================

    pendientes_final = contar_no_leidas(
        db=db,
        usuario_id=usuario_id
    )


    print(
        "Pendientes después:",
        pendientes_final
    )


    print(
        "\n✔ Test completado"
    )



if __name__ == "__main__":
    run()