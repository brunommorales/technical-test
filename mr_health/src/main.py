from config import OUTPUT_DIR
from load_data import carregar_bases
from prepare_data import (
    tratar_item_pedido,
    unir_item_com_preco,
    calcular_total_item,
    montar_demanda_diaria_item,
)
from model import (
    montar_base_modelagem,
    separar_treino_teste,
    treinar_e_avaliar,
)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pedido, item_pedido, itens = carregar_bases()

    item_pedido = tratar_item_pedido(item_pedido)

    base_itens = unir_item_com_preco(item_pedido, itens)
    base_itens = calcular_total_item(base_itens)

    demanda_diaria_item = montar_demanda_diaria_item(base_itens, pedido)

    base_modelagem = montar_base_modelagem(demanda_diaria_item)
    treino, teste = separar_treino_teste(base_modelagem, dias_teste=14)

    modelo, predicoes, metricas = treinar_e_avaliar(treino, teste)

    predicoes.to_csv(OUTPUT_DIR / "predicoes_teste.csv", index=False)
    metricas.to_csv(OUTPUT_DIR / "metricas_modelo.csv", index=False)

    print("\nModelo finalizado.")
    print(metricas.to_string(index=False))
    print(f"\nArquivos salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()