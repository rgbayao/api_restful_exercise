# api_restful_exercise
Exercício de criação de api restful em python proposto no curso de Data Science da Lets Code.
## Banco de dados utilizado
pesquisa_foliao_carnaval_2018:
- Dados sobre o carnaval de Belo Horizonte em 2018;
- Fonte: https://dados.gov.br/dataset/pesquisa-com-foliao-carnaval-2018
- Download direto do arquivo <a href="https://ckan.pbh.gov.br/dataset/b7b0edda-2f3c-45bd-90d5-110216a47b76/resource/9b836e99-bf0a-4d3a-8934-59972097dade/download/dataset_carnaval_20181.csv">aqui</a>.
## Funcionamento da API
Ao rodar o arquivo api_restful.py abre-se um servidor local com os dados. Do servidor pode-se acessar os filtros para a coluna "morador" do csv, escrevendo-as no formato "/nome_do_filtro", as opções válidas são "Morador" e "Visitantes".  
O acesso aos filtros acima retornam o banco de dados filtrados em json e salva três arquivos na pasta de execução:
- Dois bancos de dados, um em json e outro em csv, dos dados agrupados por cortes de idade, relacionando esses índices com os gastos médios dos foliões.
- Um histograma de dois eixos mostrando a relação entre os gastos totais e dias de carnaval dos foliões.