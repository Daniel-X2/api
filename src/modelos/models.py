from sqlalchemy import String,Boolean
from sqlalchemy import INTEGER
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column

class Base(DeclarativeBase):
    pass

class Elenco(Base):
    __tablename__="elenco"

    id:Mapped[int]=mapped_column(primary_key=True)
    nome:Mapped[str]=mapped_column(String(30))
    ator:Mapped[str]=mapped_column(String(30))
    vivo:Mapped[bool]=mapped_column(Boolean)
    habilidades:Mapped[list]=mapped_column(JSON)
    upvote:Mapped[int]=mapped_column(INTEGER)
    

