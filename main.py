from fastapi import FastAPI
from fastapi import HTTPException

from banco import banco

app=FastAPI()

db=banco()
@app.get("/")
def home():
    return "ola mano"
   
@app.get("/elenco")
def elenco(status:str = "",habilidade:str="",mais_votado:bool=False):
    
    return db.elenco(status,habilidade,mais_votado)
@app.get("/elenco/{nome}")
def busca_ator(nome:str):
    ator=db.buscar(nome)
    if ator:
        return ator
    raise HTTPException(status_code=404, detail="Ator não encontrado")
@app.get("/personagem/{nome}")
def buscar_personagem(nome:str):
    personagem=db.buscar("",nome)
    if personagem:
        return personagem
    raise HTTPException(status_code=404, detail="personagem não encontrado")
@app.post("/votar/{personagem}")
def upvote(personagem):
    voto=db.atualizar_voto(personagem)
    if voto==0:
        return "adicionado com sucesso"
    elif voto==1:
        raise HTTPException(status_code=404, detail="personagem não encontrado")
    else:
        raise HTTPException(status_code=400, detail="problema no banco de dados")
#uvicorn main:app --reload