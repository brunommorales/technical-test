import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


def montar_base_modelagem(demanda_diaria_item):
    base = demanda_diaria_item.copy()
    base["DATA"] = pd.to_datetime(base["DATA"])

    datas = pd.date_range(base["DATA"].min(), base["DATA"].max(), freq="D")
    itens = sorted(base["ID_ITEM"].unique())

    painel = pd.MultiIndex.from_product(
        [datas, itens],
        names=["DATA", "ID_ITEM"]
    ).to_frame(index=False)

    base = painel.merge(
        base[["DATA", "ID_ITEM", "QUANTIDADE_TOTAL"]],
        on=["DATA", "ID_ITEM"],
        how="left"
    )

    base["QUANTIDADE_TOTAL"] = base["QUANTIDADE_TOTAL"].fillna(0)
    base = base.sort_values(["ID_ITEM", "DATA"]).reset_index(drop=True)

    base["dia_semana"] = base["DATA"].dt.dayofweek
    base["lag_1"] = base.groupby("ID_ITEM")["QUANTIDADE_TOTAL"].shift(1)
    base["lag_7"] = base.groupby("ID_ITEM")["QUANTIDADE_TOTAL"].shift(7)

    base = base.dropna().reset_index(drop=True)
    return base


def separar_treino_teste(base_modelagem, dias_teste=14):
    data_corte = base_modelagem["DATA"].max() - pd.Timedelta(days=dias_teste - 1)

    treino = base_modelagem[base_modelagem["DATA"] < data_corte].copy()
    teste = base_modelagem[base_modelagem["DATA"] >= data_corte].copy()

    return treino, teste


def treinar_e_avaliar(treino, teste):
    features = ["ID_ITEM", "dia_semana", "lag_1", "lag_7"]
    target = "QUANTIDADE_TOTAL"

    X_train = pd.get_dummies(treino[features], columns=["ID_ITEM", "dia_semana"])
    X_test = pd.get_dummies(teste[features], columns=["ID_ITEM", "dia_semana"])

    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    y_train = treino[target]
    y_test = teste[target]

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    pred_modelo = modelo.predict(X_test)
    pred_modelo = np.clip(pred_modelo, 0, None)

    pred_baseline = teste["lag_7"].values
    pred_baseline = np.clip(pred_baseline, 0, None)

    mse_modelo = mean_squared_error(y_test, pred_modelo)
    mse_baseline = mean_squared_error(y_test, pred_baseline)

    metricas = pd.DataFrame([
        {
            "modelo": "regressao_linear",
            "MAE": round(mean_absolute_error(y_test, pred_modelo), 4),
            "MSE": round(mse_modelo, 4),
            "RMSE": round(np.sqrt(mse_modelo), 4),
        },
        {
            "modelo": "baseline_semana_anterior",
            "MAE": round(mean_absolute_error(y_test, pred_baseline), 4),
            "MSE": round(mse_baseline, 4),
            "RMSE": round(np.sqrt(mse_baseline), 4),
        }
    ])

    predicoes = teste[["DATA", "ID_ITEM", "QUANTIDADE_TOTAL"]].copy()
    predicoes["PREDICAO_MODELO"] = pred_modelo
    predicoes["PREDICAO_BASELINE"] = pred_baseline

    return modelo, predicoes, metricas