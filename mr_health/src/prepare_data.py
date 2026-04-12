import pandas as pd


def tratar_item_pedido(item_pedido):
    item_pedido = item_pedido.drop_duplicates().copy()

    item_pedido = (
        item_pedido.groupby(["ID_PEDIDO", "ID_ITEM"], as_index=False)["QUANTIDADE"]
        .sum()
    )

    return item_pedido


def unir_item_com_preco(item_pedido, itens):
    return item_pedido.merge(itens, on="ID_ITEM", how="left")


def calcular_total_item(base_itens):
    base_itens = base_itens.copy()
    base_itens["TOTAL_ITEM"] = base_itens["QUANTIDADE"] * base_itens["PRECO_UNITARIO"]
    return base_itens


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