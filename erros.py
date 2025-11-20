
class ErroValorMinimo(Exception):
    def __init__(self,campo:str,minimo:int,recebido:int):
        
        super().__init__(f"o {campo} nao alcança o valor minimo de {minimo} caracteres")
    pass
class ValorVazio(Exception):
    def __init__(self):
        super().__init__("o Valor inserido e vazio")
class ErroNoBancoSql(Exception):
    def __init__(self,erro):
        super().__init__(f"aconteceu um erro no banco de dados {erro}")
class ErroNenhumResultado(Exception):
    def __init__(self,campo):
        super().__init__(f"Nenhum Resultado encontrado no campo {campo}")


