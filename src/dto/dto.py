from pydantic import BaseModel,Field
class ElencoDto(BaseModel):
    nome:str =Field(min_length=3)
    ator:str = Field(min_length=3)
    vivo:bool
    habilidades:list
    upvote:int

def serializar_lista(dados):
        lista = list()
        for c in dados:
            lista.append(
                ElencoDto(
                    nome=c.nome,
                    ator=c.ator,
                    vivo=c.vivo,
                    habilidades=c.habilidades,
                    upvote=c.upvote
                ).model_dump()
                )
        return lista
def serializar_dict(dados):
    dici = dict()
    for n,c in enumerate(dados):
        dici[f"{n+1}° lugar"]=(
            ElencoDto(
                    nome=c.nome,
                    ator=c.ator,
                    vivo=c.vivo,
                    habilidades=c.habilidades,
                    upvote=c.upvote
                ).model_dump()
                )
        
    return dici