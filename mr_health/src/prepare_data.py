import pandas as pd
from load_data import carregar_bases

def unir_item_com_preco(item_pedido, itens):
    return item_pedido.merge(itens, on="ID_ITEM", how="left")

def calcular_total_item(base_itens):
    base = base_itens.copy()
    base["TOTAL_ITEM"] = base["QUANTIDADE"] * base["PRECO_UNITARIO"]
    return base

def calcular_total_pedido(base_itens):
    total_pedido = (
        base_itens.groupby("ID_PEDIDO", as_index=False)["TOTAL_ITEM"]
        .sum()
        .rename(columns={"TOTAL_ITEM": "TOTAL_PEDIDO"})
    )
    return total_pedido

def montar_base_pedidos(pedido, total_pedido):
    return pedido.merge(total_pedido, on="ID_PEDIDO", how="left")

def montar_demanda_diaria_item(base_itens, pedido):
    base = base_itens.merge(
        pedido[["ID_PEDIDO", "DATA"]],
        on="ID_PEDIDO",
        how="left"
    )

    demanda = (
        base.groupby(["DATA", "ID_ITEM"], as_index=False)
        .agg(
            QUANTIDADE_TOTAL=("QUANTIDADE", "sum"),
            VALOR_TOTAL_ITEM=("TOTAL_ITEM", "sum")
        )
    )
    return demanda

if __name__ == "__main__":
    pedido, item_pedido, itens = carregar_bases()

    base_itens = unir_item_com_preco(item_pedido, itens)
    base_itens = calcular_total_item(base_itens)
    total_pedido = calcular_total_pedido(base_itens)

    base_pedidos = montar_base_pedidos(pedido, total_pedido)
    demanda_diaria_item = montar_demanda_diaria_item(base_itens, pedido)

    print("\n=== BASE_ITENS ===")
    print(base_itens.head())

    print("\n=== BASE_PEDIDOS ===")
    print(base_pedidos.head())

    print("\n=== DEMANDA_DIARIA_ITEM ===")
    print(demanda_diaria_item.head())

    print("\n=== CHECAGEM DE NULOS EM PRECO_UNITARIO ===")
    print(base_itens["PRECO_UNITARIO"].isna().sum())