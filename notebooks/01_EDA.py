#%%
import kagglehub

# Download latest version
path = kagglehub.dataset_download("mkechinov/ecommerce-behavior-data-from-multi-category-store")

print("Path to dataset files:", path)
# %%

import pandas as pd

# Carregando os dados
df = pd.read_csv(f"{path}/2019-Oct.csv")
#%%
# Exibindo as primeiras linhas do dataset
df.head()
# %%
# Exibindo informações sobre o dataset
df.info()
# %%[markdown]
# O dataset contém informações sobre o comportamento de compra dos clientes em uma loja de comércio eletrônico.
# As colunas incluem:
# - `event_time`: O horário do evento.
# - `event_type`: O tipo de evento (ex: view, addtocart, purchase).
# - `product_id`: O ID do produto.
# - `category_id`: O ID da categoria do produto.
# - `category_code`: O código da categoria do produto.
# - `brand`: A marca do produto.
# - `price`: O preço do produto.
# - `user_id`: O ID do usuário.
# - `user_session`: O ID da sessão do usuário.  
#%%[markdown]

# 'user_id' e 'user_session' são identificadores únicos para cada usuário e sessão, respectivamente. Eles podem ser usados para rastrear o comportamento de compra dos clientes ao longo do tempo e identificar padrões de consumo. O 'user_id' pode ser usado para agrupar os eventos por usuário, enquanto o 'user_session' pode ser usado para agrupar os eventos por sessão de compra. Essas informações são valiosas para entender o comportamento dos clientes e personalizar as estratégias de marketing e vendas.
# 'event_type' é uma coluna que indica o tipo de evento que ocorreu, como visualização do produto, adição ao carrinho ou compra. Essa informação é crucial para análise de compra dos clientes, pois permite identificar quais produtos são mais visualizados, quais são adicionados ao carrinho e quais são efetivamente comprados. Com base nessa coluna, é possível realizar análises de funil de vendas, identificar pontos de abandono no processo de compra e otimizar as estratégias de marketing para aumentar as conversões.
# A relação entre essas três colunas é fundamental para entender o comportamento de compra dos clientes. O 'user_id' e 'user_session' permitem rastrear as ações dos clientes ao longo do tempo, enquanto o 'event_type' fornece informações sobre as interações específicas que os clientes têm com os produtos. Analisando essas colunas em conjunto, é possível identificar padrões de consumo, segmentar os clientes com base em seu comportamento de compra e personalizar as estratégias de marketing para atender às necessidades e preferências dos clientes.  
# %%[markdown]
# <br>
# O dataset é bastante grande, contendo mais de 42 milhões de linhas. Ele pode ser utilizado para análises de comportamento do cliente, segmentação de mercado, análise de vendas, entre outras aplicações. 
#%%[markdown]
# Antes de prosseguir com a análise, é importante entender o que cada linha de dados representa. Cada linha do dataset representa um evento específico relacionado a um produto e a um usuário em um determinado momento. O tipo de evento pode ser uma visualização do produto, a adição do produto ao carrinho ou a compra do produto. Essas informações podem ser usadas para analisar o comportamento de compra dos clientes, identificar padrões de consumo e entender as preferências dos usuários em relação aos produtos e categorias disponíveis na loja de comércio eletrônico.
# %%[markdown]
# Vamos explorar um pouco mais os dados em busca de valores nulos e duplicados.
# %%
df.isnull().sum()
# %%
df.duplicated().sum()

# %%[markdown]
# O dataset possui uma quantidade significativa de valores nulos, especialmente nas colunas `category_code` e `brand`. Além disso, há uma quantidade considerável de linhas duplicadas. Esses fatores devem ser levados em consideração durante a análise dos dados, pois podem afetar os resultados e as conclusões que podemos tirar do dataset. Será necessário realizar um tratamento adequado para lidar com esses valores nulos e duplicados antes de prosseguir com a análise.
# Apesar disso, as colunas 'category_code' e 'brand' não são essenciais para a análise de comportamento de compra, e os valores nulos podem ser tratados como uma categoria separada ou simplesmente ignorados, dependendo do contexto da análise. Já as linhas duplicadas podem ser removidas para garantir que cada evento seja contado apenas uma vez, o que pode ajudar a obter resultados mais precisos e confiáveis.
# %%[markdown]
#Teremos também converter alguns tipos de dados, como a coluna `event_time`, que atualmente está em formato de string, para um formato de data e hora mais adequado para análise temporal. Isso permitirá que possamos realizar análises mais precisas e eficientes, como agrupar os eventos por dia, semana ou mês, e identificar tendências ao longo do tempo. Além disso, a conversão de tipos de dados pode ajudar a reduzir o uso de memória e melhorar o desempenho das operações de análise.
# %%
# Checando quais linhas possuem duplicados
df[df.duplicated()]
# %%[markdown]
# As linhas duplicadas parecem ser eventos idênticos, o que pode ocorrer devido a erros de registro ou processamento dos dados. Para garantir a integridade da análise, é recomendável remover essas linhas duplicadas, mantendo apenas uma ocorrência de cada evento. Isso pode ser feito utilizando o método `drop_duplicates()` do pandas, que irá eliminar as linhas duplicadas e manter apenas a primeira ocorrência de cada evento. Dessa forma, podemos garantir que cada evento seja contado apenas uma vez, o que é essencial para obter resultados precisos e confiáveis na análise do comportamento de compra dos clientes.
# %%[markdown]
# </br>
# Agora vamos checar se elas são 100% identicas, ou seja, se todas as colunas possuem os mesmos valores ou se são parcialmente iguais.
# %%
# Checando se as linhas duplicadas são 100% idênticas
df[df.duplicated(keep=False)].sort_values(by='event_time')
# %%[markdown]
# As linhas duplicadas parecem ser 100% idênticas, pois todas as colunas possuem os mesmos valores. Isso sugere que esses eventos foram registrados mais de uma vez, possivelmente devido a um erro de processamento ou registro dos dados.
# %%[markdown]
#Vamos agora verificar qual evento ocorre com mais frequência no dataset, para entender melhor o comportamento de compra dos clientes, para assim compreender como os clientes avançam no funil de conversão, desde a visualização do produto até a compra. Isso pode ajudar a identificar pontos de abandono no processo de compra e otimizar as estratégias de marketing para aumentar as conversões.
# %%
# Verificando a frequência de cada tipo de evento
event_counts = df['event_type'].value_counts()
print(event_counts)
# %%
# Visualizando a proporção de cada tipo de evento
event_proportions = df['event_type'].value_counts(normalize=True) * 100
print(event_proportions)
# %%[markdown]
# O evento mais frequente no dataset é o "view", que representa a visualização do produto pelos clientes. Isso indica que os clientes estão mais propensos a visualizar os produtos do que a adicioná-los ao carrinho ou comprá-los. A proporção de visualizações é significativamente maior do que as adições ao carrinho e as compras, o que sugere que muitos clientes estão apenas explorando os produtos sem necessariamente avançar para as etapas seguintes do funil de conversão.
# %%[markdown]
# Apenas 1.74% dos usuarios que visualizam chegam a finalizar a compra.
# %%
