import pandas as pd
from config import PEDIDO_FILE, ITEM_PEDIDO_FILE, ITENS_FILE

def carregar_pedido():
    pedido = pd.read_excel(PEDIDO_FILE)
    pedido = pedido.drop(columns=["Unnamed: 0"], errors="ignore")
    pedido["DATA"] = pd.to_datetime(pedido["DATA"], errors="coerce")
    return pedido

def carregar_item_pedido():
    item_pedido = pd.read_excel(ITEM_PEDIDO_FILE)
    item_pedido = item_pedido.drop(columns=["Unnamed: 0"], errors="ignore")
    item_pedido["ID_ITEM"] = item_pedido["ID_ITEM"].str.strip()
    return item_pedido

def carregar_itens():
    itens = pd.read_excel(ITENS_FILE)
    itens = itens.rename(columns={"Unnamed: 0": "ID_ITEM", 0: "PRECO_UNITARIO"})
    itens["ID_ITEM"] = itens["ID_ITEM"].str.strip()
    return itens

def carregar_bases():
    pedido = carregar_pedido()
    item_pedido = carregar_item_pedido()
    itens = carregar_itens()
    return pedido, item_pedido, itens

if __name__ == "__main__":
    pedido, item_pedido, itens = carregar_bases()
    print("PEDIDO:")
    print(pedido.head())
    print("\nITEM_PEDIDO:")
    print(item_pedido.head())
    print("\nITENS:")
    print(itens.head())