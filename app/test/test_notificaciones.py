from app.db.session import SessionLocal
from app.services.horario_service import reasignar_aula
from app.models.notificacion import Notificacion

def run():

    db = SessionLocal()

    print("\n--- TEST NOTIFICACIONES ---\n")

    # =========================
    # 1. REASIGNAR AULA
    # =========================
    print("🔄 Reasignando aula...")

    try:
        horario = reasignar_aula(
            db=db,
            horario_id=1,      # ⚠️ ajusta si no existe
            nueva_aula_id=2    # ⚠️ ajusta si no existe
        )

        print("✔ Aula reasignada")
        print("Horario ID:", horario.id)

    except Exception as e:
        print("❌ Error al reasignar:", e)
        return

    # =========================
    # 2. VERIFICAR NOTIFICACIONES
    # =========================
    print("\n📩 Buscando notificaciones...")

    notificaciones = db.query(Notificacion).all()

    if not notificaciones:
        print("⚠️ No hay notificaciones")
        return

    for n in notificaciones:
        print(f"""
            ID: {n.id}
            Usuario: {n.usuario_id}
            Mensaje: {n.mensaje}
            Tipo evento: {n.tipo_evento}
            Referencia: {n.referencia_id}
            Leído: {n.leido}
            Fecha: {n.created_at}
            """)

    print("\n✔ Test completado")


if __name__ == "__main__":
    run()