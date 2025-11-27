from pydantic_core import _pydantic_core
from src.repository.main_repository import ElencoRepository
from src.dto.dto import ElencoDto,serializar_lista,serializar_dict
from src.Erros_personalizado.erros import *
repository=ElencoRepository()
class ElencoService():

    def __init__(self):
        pass
    def buscar_com_filtro(self,vivo:bool=True,habilidade:str=None,mais_votado:bool=False):
        smt=repository.get_select()
        smt=repository.filtro_status(status=vivo,smt=smt)
        if(habilidade!=None and habilidade!="" ):
            if( len(habilidade.strip())>=3):
                smt=repository.filtro_habilidades(habilidade=habilidade,smt=smt)
            else:
                raise ErroValorMinimo
        if (mais_votado==True):
            smt=repository.mais_votado(smt=smt)#depois preciso sicronizar com os outros filtros
            dados=repository.executar_first(smt)
            try:
                return ElencoDto(nome=dados.nome,
                      ator=dados.ator,
                      vivo=dados.vivo,
                      habilidades=dados.habilidades,
                      upvote=dados.upvote).model_dump()
            except  _pydantic_core.ValidationError:
                raise ErroValidacao
            except AttributeError:
                raise ErroNenhumResultado("filtros")
        dados=repository.executar_all(smt)
        
        if(len(dados)==0):
             raise ErroNenhumResultado("lista vazia")
        dados=serializar_lista(dados=dados)
        return dados
    def buscar_no_elenco(self,nome,modo="ator"):
        if(len(nome)<3):
            raise ErroValorMinimo
        smt=repository.get_select()
        
        if(modo=="ator"):
            smt=repository.buscar_ator(nome,smt)
        else:
            smt=repository.buscar_personagem(nome,smt)
        dados=repository.executar_first(smt)
        try:
            return ElencoDto(nome=dados.nome,
                      ator=dados.ator,
                      vivo=dados.vivo,
                      habilidades=dados.habilidades,
                      upvote=dados.upvote).model_dump()  
        except AttributeError:
            raise ErroNenhumResultado("nome")
        except _pydantic_core.ValidationError:
            raise ErroValidacao
    def retornar_elenco(self):
        smt=repository.get_select()
        dados=repository.executar_all(smt)
        if(dados==None or len(dados)==0):
            raise ValorVazio
        dados=serializar_lista(dados)
        return dados
    def votar(self,nome):
        if(len(nome)<3):
            raise ErroValorMinimo
        repository.update_voto(nome)
    def stats(self):
        total_vivos=repository.total_vivos_mortos(vivo=True)
        total_mortos=repository.total_vivos_mortos(vivo=False)
        
        smt=repository.mais_votado(smt=repository.get_select())
        dados=repository.executar_first(smt)
        total_personagem=repository.total_personagem()

        return  {"total de personagens":total_personagem,
                 "total de personagens vivos":total_vivos,
                 "total de personagens mortos": total_mortos,
                 "personagem com maior quantidade de votos":f"{dados.nome} {dados.upvote} votos",
                 }
    def ranking(self,top:int):
        
        smt=repository.mais_votado(smt=repository.get_select()).limit(limit=top)
        dados=repository.executar_all(smt)
        if(dados==None or len(dados)==0):
            raise ValorVazio
        dados=serializar_dict(dados)
        
        return dados