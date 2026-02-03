from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class PersonajeDisney(Base):
    """SQLAlchemy model para la tabla personajes_master basada en Disney API."""
    __tablename__ = "personajes_master"

    # Primary Key (usamos el id de la API como PK)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Nombre del personaje
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    # Información multimedia
    imageUrl: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Apariciones en películas, series y atracciones,etc... (guardamos como texto plano concatenado)
    films: Mapped[str | None] = mapped_column(Text, nullable=True)
    tvShows: Mapped[str | None] = mapped_column(Text, nullable=True)
    parkAttractions: Mapped[str | None] = mapped_column(Text, nullable=True)

    
    allies: Mapped[str | None] = mapped_column(Text, nullable=True)
    enemies: Mapped[str | None] = mapped_column(Text, nullable=True)
    videoGames: Mapped[str | None] = mapped_column(Text, nullable=True)
    shortFilms: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<PersonajeDisney(id={self.id}, name='{self.name}')>"