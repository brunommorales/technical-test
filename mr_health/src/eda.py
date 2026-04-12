from load_data import carregar_bases
from prepare_data import (
    tratar_item_pedido,
    unir_item_com_preco,
    calcular_total_item,
    calcular_total_pedido,
    montar_base_pedidos,
    montar_demanda_diaria_item,
)


def mostrar_base(df, nome):
    print(f"\n{nome}")
    print("shape:", df.shape)
    print("colunas:", list(df.columns))
    print(df.head())


def mostrar_qualidade(pedido, item_pedido, itens):
    print("\nNulos")

    print("\nPEDIDO")
    print(pedido.isna().sum())

    print("\nITEM_PEDIDO")
    print(item_pedido.isna().sum())

    print("\nITENS")
    print(itens.isna().sum())

    print("\nDuplicatas exatas")
    print("PEDIDO:", pedido.duplicated().sum())
    print("ITEM_PEDIDO:", item_pedido.duplicated().sum())
    print("ITENS:", itens.duplicated().sum())

    print("\nDuplicatas por chave")
    print("ID_PEDIDO em PEDIDO:", pedido.duplicated(subset=["ID_PEDIDO"]).sum())
    print("ID_ITEM em ITENS:", itens.duplicated(subset=["ID_ITEM"]).sum())
    print(
        "(ID_PEDIDO, ID_ITEM) em ITEM_PEDIDO:",
        item_pedido.duplicated(subset=["ID_PEDIDO", "ID_ITEM"]).sum()
    )

    pedidos_fora = item_pedido.loc[
        ~item_pedido["ID_PEDIDO"].isin(pedido["ID_PEDIDO"]),
        "ID_PEDIDO"
    ].nunique()

    itens_fora = item_pedido.loc[
        ~item_pedido["ID_ITEM"].isin(itens["ID_ITEM"]),
        "ID_ITEM"
    ].nunique()

    print("\nIntegridade")
    print("ID_PEDIDO sem correspondência em PEDIDO:", pedidos_fora)
    print("ID_ITEM sem correspondência em ITENS:", itens_fora)


def tratar_bases(pedido, item_pedido, itens):
    item_pedido = tratar_item_pedido(item_pedido)

    print(
        "\nVALOR_TOTAL nulo em PEDIDO:",
        pedido["VALOR_TOTAL"].isna().sum(),
        "de",
        len(pedido)
    )

    base_itens = unir_item_com_preco(item_pedido, itens)
    base_itens = calcular_total_item(base_itens)

    total_pedido = calcular_total_pedido(base_itens)
    base_pedidos = montar_base_pedidos(pedido, total_pedido)
    demanda_diaria_item = montar_demanda_diaria_item(base_itens, pedido)

    return base_itens, base_pedidos, demanda_diaria_item


def analise_descritiva(base_itens, base_pedidos, demanda_diaria_item):
    print("\nResumo geral")
    print("Pedidos:", base_pedidos["ID_PEDIDO"].nunique())
    print("Receita total:", round(base_pedidos["TOTAL_PEDIDO"].sum(), 2))
    print("Ticket médio:", round(base_pedidos["TOTAL_PEDIDO"].mean(), 2))

    vendas_por_dia = (
        base_pedidos.groupby("DATA", as_index=False)["TOTAL_PEDIDO"]
        .sum()
        .sort_values("DATA")
    )

    itens_mais_vendidos = (
        demanda_diaria_item.groupby("ID_ITEM", as_index=False)
        .agg(
            QUANTIDADE_TOTAL=("QUANTIDADE_TOTAL", "sum"),
            VALOR_TOTAL_ITEM=("VALOR_TOTAL_ITEM", "sum")
        )
        .sort_values("QUANTIDADE_TOTAL", ascending=False)
    )

    print("\nVendas por dia")
    print(vendas_por_dia.head(10))

    print("\nItens mais vendidos")
    print(itens_mais_vendidos)

    print("\nChecagem pós-merge")
    print("PRECO_UNITARIO nulo:", base_itens["PRECO_UNITARIO"].isna().sum())
    print("TOTAL_PEDIDO nulo:", base_pedidos["TOTAL_PEDIDO"].isna().sum())

    return vendas_por_dia, itens_mais_vendidos


def analisar_sazonalidade(vendas_por_dia):
    serie = vendas_por_dia.copy()
    serie = serie.set_index("DATA").asfreq("D", fill_value=0).reset_index()

    mapa = {
        0: "segunda",
        1: "terca",
        2: "quarta",
        3: "quinta",
        4: "sexta",
        5: "sabado",
        6: "domingo",
    }

    serie["dia_semana"] = serie["DATA"].dt.dayofweek.map(mapa)

    ordem = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]

    sazonalidade = (
        serie.groupby("dia_semana", as_index=False)["TOTAL_PEDIDO"]
        .mean()
        .rename(columns={"TOTAL_PEDIDO": "media_venda"})
    )

    sazonalidade["ordem"] = sazonalidade["dia_semana"].map(
        {dia: i for i, dia in enumerate(ordem)}
    )

    sazonalidade = sazonalidade.sort_values("ordem").drop(columns="ordem")

    print("\nDias sem venda:", (serie["TOTAL_PEDIDO"] == 0).sum())

    print("\nMédia de vendas por dia da semana")
    print(sazonalidade)

    return sazonalidade


if __name__ == "__main__":
    pedido, item_pedido, itens = carregar_bases()

    mostrar_base(pedido, "PEDIDO")
    mostrar_base(item_pedido, "ITEM_PEDIDO")
    mostrar_base(itens, "ITENS")

    mostrar_qualidade(pedido, item_pedido, itens)

    base_itens, base_pedidos, demanda_diaria_item = tratar_bases(
        pedido, item_pedido, itens
    )

    vendas_por_dia, itens_mais_vendidos = analise_descritiva(
        base_itens, base_pedidos, demanda_diaria_item
    )

    analisar_sazonalidade(vendas_por_dia)