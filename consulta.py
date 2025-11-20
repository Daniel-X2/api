from sqlalchemy import update
from sqlalchemy.orm import Session
from banco import engine
from models import User
from erros import *

class consulta():
    def __init__(self):
        pass
    
    def buscar_com_filtro(self,habilidade_:str=None,status_=None,mais_votado_=False):
        with Session(engine) as session:
            # #
            # aqui faz a filtragem da pesquisa
            # #
            busca=session.query(User.nome,User.ator,User.status,
            User.habilidades,User.upvote)

            if(status_==None and habilidade_==None and mais_votado_==False):
                #aqui serve principalmente pra listar todos no elenco
                try:
                    return self.loop_busca(busca.all(),False)
                except ValorVazio:
                    raise ValorVazio
                except IndexError:
                    raise IndexError
            if(status_!=None):
                busca=busca.filter(User.status==status_)
            if(habilidade_!=None):
                busca=busca.filter(User.habilidades.contains(habilidade_))
            try:
                return self.loop_busca(busca.all(),mais_votado_)
            except ValorVazio:
                raise ValorVazio
            except IndexError:
                raise IndexError  
    def buscar_ator(self,ator_:str=None):
        
        with Session(engine) as session:

            quantidade_caracteres=len(ator_.replace(" ",""))
            if(quantidade_caracteres>=4):
                dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.ator.ilike(f"{ator_}%")).first()
                    
                if(dados!= None and dados !=""):
                    return {"nome":dados[0],"ator":dados[1],"status":dados[2],"habilidade":dados[3],"upvote":dados[4]}
                else:
                    raise ErroNenhumResultado("ator")
            else:
                raise ErroValorMinimo("ator",4,quantidade_caracteres)
    def buscar_personagem(self,personagem_:str=None):

        with Session(engine) as session:
            quantidade_caracteres=len(personagem_.replace(" ",""))
            if(quantidade_caracteres>=4):
                dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.nome.ilike(f"{personagem_}%")).first()
                if(dados!=None):
                    return {"nome":dados[0],"ator":dados[1],"status":dados[2],"habilidade":dados[3],"upvote":dados[4]}
                else:
                    raise ErroNenhumResultado("personagem")
            else:
                raise ErroValorMinimo("personagem",4,quantidade_caracteres)
    def loop_busca(self,dados_,mais_votado:bool):
        lista=list()

        if(dados_==None or dados_==""):
            raise ErroNenhumResultado("")
        try:
            for c in range(0,len(dados_)):
                            
                lista.append({"nome":dados_[c][0],"ator":dados_[c][1],"status":dados_[c][2],
                    "habilidade":dados_[c][3],"upvote":dados_[c][4]})
            if(mais_votado==True):
                
                maior=0
                personagem=""
                for c in range(0,len(lista)):
                    if(maior<=lista[c]["upvote"]):
                        maior=lista[c]["upvote"]
                        personagem=lista[c]
                    else:
                        continue
                
                
                return personagem
            
            
            return lista
        
        except IndexError:
            raise IndexError
    def atualizar_voto(self,personagem):
        with Session(engine) as session: 
            
            try:
                
                smt=(update(User).filter(User.nome.ilike(f"{personagem}%")).values(upvote=User.upvote+1))
                #n1=session.execute(smt)
                n2=session.connection().execute(smt)
                if(n2.rowcount==0):
                    raise ErroNenhumResultado("Personagem")
                session.commit()

            except Exception as e:
                
                raise ErroNoBancoSql(e)
            return 0
   
