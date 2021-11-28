from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)
api = Api(app)

bh_carnival = df = pd.read_csv(
    'https://ckan.pbh.gov.br/dataset/b7b0edda-2f3c-45bd-90d5-110216a47b76/resource/9b836e99-bf0a-4d3a-8934'
    '-59972097dade/download/dataset_carnaval_20181.csv'
)

money_columns = ['T_Hospedagem', 'Alimentacao', 'T_Atrativos_passeios',
                 'Transporte_interno', 'Compras', 'Ingressos', 'Outros', 'Total']


def _groupby_age_cut(data) -> pd.DataFrame:
    money_data = data.fillna(0)
    money_data = _convert_all_to_numerical_column(money_data)
    money_data = money_data.groupby(pd.cut(money_data['Idade'], bins=range(16, 77, 10))).mean().round(2)
    return money_data


def _convert_all_to_numerical_column(data):
    for i in data:
        if data[i].dtype == 'object':
            data[i] = _convert_to_numerical_column(data[i])
        return data


def _convert_to_numerical_column(data_series: pd.Series):
    data_series = data_series.fillna("0")
    data_series = data_series.apply(lambda x: x.replace(",", "."))
    data_series = data_series.astype("float")
    return data_series


def _persistence_data(data, filtered_by):
    data.to_csv(f'{filtered_by}_spend_values.csv')
    data.to_json(f'{filtered_by}_spend_values.json')


def _generate_money_spend_data(data, filtered_by):
    filter_cols = money_columns.copy()
    filter_cols.append("Idade")
    money_data = _groupby_age_cut(data.loc[:, filter_cols])
    _persistence_data(money_data, filtered_by)


def _generate_money_spend_chart(data, filtered_by):
    data = data.loc[:, ['Dias_carnaval', 'Total']]
    data = data.loc[~data['Dias_carnaval'].isna()]
    if data['Total'].dtype == 'object':
        data['Total'] = _convert_to_numerical_column(data['Total'])
    sns.set(rc={'figure.figsize': (20, 9)})
    sns.histplot(data, x='Total', y='Dias_carnaval', discrete=(False, True))
    plt.ylabel('Days in BH Carnival', fontsize=14)
    plt.xlabel('Total Spend amount', fontsize=14)
    plt.title(f'{filtered_by}: Total spend vs Days in BH Carnival histogram')
    plt.savefig(f'{filtered_by}_spend_chart.png')


class CarnivalData(Resource):
    def get(self, morador):
        data_filter = bh_carnival['morador'] == morador
        bh_carnival_filtered = bh_carnival[data_filter]
        if len(bh_carnival_filtered) > 0:
            _generate_money_spend_data(bh_carnival_filtered, morador)
            _generate_money_spend_chart(bh_carnival_filtered, morador)
        return bh_carnival_filtered.to_json()


api.add_resource(CarnivalData, '/<string:morador>')

if __name__ == '__main__':
    app.run(debug=True)
