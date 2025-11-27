from fastapi import FastAPI
from fastapi import HTTPException
from src.Erros_personalizado.erros import *
from src.service.main_service import ElencoService
app=FastAPI()
service=ElencoService()


@app.get("/")
def home():
    return "ola mano"
@app.get("/elenco")
def elenco():
    try:
        return service.retornar_elenco()
    except ValorVazio:
        raise HTTPException(status_code=404,
                            detail="O valor retornado e vazio")
@app.get("/busca/")
def busca_com_filtro(vivo:bool=True,habilidade:str=None,mais_votado:bool=False):
    try:
        dados=service.buscar_com_filtro(vivo=vivo,
                                        habilidade=habilidade,
                                        mais_votado=mais_votado)
    except ErroNenhumResultado:
        raise HTTPException(
                            status_code=404,
                            detail="nenhum personagem encontrado com essas caracteristicas")
    except ErroValidacao:
        raise HTTPException(
                            status_code=400, 
                            detail="Erro ao validar os dados inseridos")
    except ErroSemParametros:
        raise HTTPException(
                            status_code=400, 
                            detail="Nenhum parametro selecionado")
    except ErroValorMinimo:
        raise HTTPException(
                            status_code=400, 
                            detail="o parametro habilidade nao tem o valor minimo")
    return dados
@app.get("/elenco/{ator}")
def busca_ator(ator:str):
    try:
        
        dados_ator=service.buscar_no_elenco(nome=ator,modo="ator")

        return dados_ator
    except ErroValorMinimo:
        raise HTTPException(status_code=400,
                            detail="Valor minimo de caracteres nao foram cumpridos")
    except ErroValidacao:
        raise HTTPException(status_code=400,
                            detail="erro na validaçao dos dados inseridos")
    except ErroNenhumResultado:
        raise HTTPException(status_code=404,
                            detail="ator nao enconstrado")
@app.get("/personagem/{personagem}")
def buscar_personagem(personagem:str):
    try:
        dados_personagem=service.buscar_no_elenco(nome=personagem,modo="personagem")
        
        return dados_personagem
    except ErroValorMinimo:
        raise HTTPException(status_code=400,
                            detail="Valor minimo de caracteres nao foram cumpridos")
    except ErroNenhumResultado:
        raise HTTPException(status_code=404,
                            detail="personagem nao enconstrado")
    except ErroValidacao:
        raise HTTPException(status_code=400,
                            detail="erro na validaçao dos dados inseridos")
@app.post("/votar/{personagem}")
def upvote(personagem:str):
    try:
        service.votar(personagem)
        return "sucesso"
    except ErroNenhumResultado:
        raise HTTPException(status_code=404,
                            detail="personagem não encontrado")
    except ErroValorMinimo:
        raise HTTPException(status_code=404,
                            detail="o Valor minimo de caracteres nao foram alcançados")
@app.get("/ranking/")
def ranking(top:int=3):
    try:
        if(top<=0):
            raise HTTPException(status_code=404,
                                detail="Foi inserido valor zero ou negativo")
        return service.ranking(top)
    except ValorVazio:
        raise HTTPException(status_code=404,
                            detail="o Valor retornado e vazio")
    except Exception as e:
        print(f"erro no {e}")
@app.get("/stats")
def estatisticas():
    try:
        return service.stats()
    except ValorVazio:
         raise  HTTPException(status_code=404,
                            detail="O valor retornado e vazio")
#uvicorn main:app --reload
