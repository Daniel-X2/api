from fastapi import FastAPI
from fastapi import HTTPException
import json


app=FastAPI()
try:
    with open("dados/dados.json","r") as arquivo:
        teste=json.load(arquivo)
except:
    raise RuntimeError
    teste=[]


@app.get("/")
def home():
    return "ola mano"
    
@app.get("/elenco")
def elenco():
    lista=[]
    for c in range(0,len(teste["elenco"])):
        lista.insert(c,{"Personagem":teste["elenco"][c]["nome"],"ator":teste["elenco"][c]["ator"]})
        
    return lista
def buscar_no_elenco(nome,campo="ator"):
    lista=[]
    for n,c in enumerate(teste["elenco"]):
        if campo=="ator":
            if nome.upper().replace(" ","") in str(c["ator"]).upper().replace(" ",""):
                lista.append({"Ator":c["ator"],"Personagem":c["nome"]})
        else:
            if nome.upper().replace(" ","") in str(c["nome"]).upper().replace(" ",""):
                lista.append({"Ator":c["ator"],"Personagem":c["nome"]})
    return lista
@app.get("/elenco/{nome}")
def busca_ator(nome:str):
    ator=buscar_no_elenco(nome)
    if ator:
        return ator
    raise HTTPException(status_code=404, detail="Ator não encontrado")
@app.get("/personagem/{nome}")
def buscar_personagem(nome:str):
    personagem=buscar_no_elenco(nome,"personagem")
    if personagem:
        return personagem
    raise HTTPException(status_code=404, detail="personagem não encontrado")
@app.post("/votar/{personagem}")
def upvote(personagem):
    for n,c in enumerate(teste["elenco"]):
        if personagem.upper().replace(" ","") in str(c["nome"]).upper().replace(" ",""):
            c["upvote"]+=1
            return "deu bom"
    return "deu ruim"
#uvicorn main:app --reload
