from fastapi import FastAPI
from fastapi import HTTPException
import json


app=FastAPI()
arquivo=open("dados/dados.json","r")
teste=json.load(arquivo)


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
    for n,c in enumerate(teste["elenco"]):
        if campo=="ator":
            if nome.upper().replace(" ","") in str(c["ator"]).upper().replace(" ",""):
                return {"Ator":c["ator"],"Personagem":c["nome"]}
            
                
        else:
            if nome.upper().replace(" ","") in str(c["nome"]).upper().replace(" ",""):
                return {"Ator":c["ator"],"Personagem":c["nome"]}
    return None
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
#uvicorn main:app --reload
arquivo.close()