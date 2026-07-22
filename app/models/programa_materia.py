from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ProgramaMateria(Base):

    __tablename__ = "programa_materias"

    __table_args__ = (
        UniqueConstraint(
            "programa_id",
            "materia_id",
            name="uq_programa_materia"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    programa_id = Column(
        Integer,
        ForeignKey("programas.id"),
        nullable=False
    )

    materia_id = Column(
        Integer,
        ForeignKey("materias.id"),
        nullable=False
    )

    programa = relationship(
        "Programa"
    )

    materia = relationship(
        "Materia"
    )