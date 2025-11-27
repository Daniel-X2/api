from sqlalchemy import update, select,func
from sqlalchemy.orm import Session
from dados.banco import engine,Elenco

class ElencoRepository():

    def __init__(self):
        pass
    
    def get_select(self):
        smt = select(Elenco)
        return smt

    def mais_votado(self,smt):  
        #smt = select(Elenco)
        smt = smt.order_by(Elenco.upvote.desc())
        return smt
    def filtro_status(self,status,smt):
        
        smt = smt.filter(Elenco.vivo == status)
        return smt
    def filtro_habilidades(self,habilidade,smt):
        #smt = select(Elenco)
        smt = smt.filter(Elenco.habilidades.contains(habilidade))
        return smt
    def executar_all(self,smt):
        with Session(engine) as session:
            return session.scalars(smt).all()
    def executar_first(self,smt):
        with Session(engine) as session:
            return session.scalars(smt).first()   
    def update_voto(self,personagem):
        with Session(engine) as session:

            smt = (update(Elenco).filter(Elenco.nome.ilike(f"{personagem}%")).values(upvote=Elenco.upvote + 1))
            session.execute(smt)
            session.commit()
        
    def buscar_ator(self,nome,smt):
        smt = smt.filter(Elenco.ator.ilike(f"{nome}%"))
        return smt
    def buscar_personagem(self,nome,smt):
        smt = smt.filter(Elenco.nome.ilike(f"{nome}%"))
        return smt
    def total_personagem(self):
        with Session(engine) as session:
            smt=select(func.count(Elenco.id))
            total=session.execute(smt).scalars().first()
            return total
    def total_vivos_mortos(self,vivo:bool):
         with Session(engine) as session:
            smt=select(func.count(Elenco.vivo)).filter(Elenco.vivo==vivo)
            total=session.execute(smt).scalars().first()
            return total
        
            
            
                 