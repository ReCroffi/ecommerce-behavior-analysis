#%%
import kagglehub

# Download latest version
path = kagglehub.dataset_download("mkechinov/ecommerce-behavior-data-from-multi-category-store")

print("Path to dataset files:", path)
# %%

import pandas as pd

# Carregando os dados
df = pd.read_csv(f"{path}/2019-Oct.csv", nrows=1000000)  # Carregando apenas os primeiros 1 milhão de linhas para análise inicial
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
# O dataset é bastante grande, contendo mais de 42 milhões de linhas, foi usado uma amostragem desse dataset para facilitar o EDA. Ele pode ser utilizado para análises de comportamento do cliente, segmentação de mercado, análise de vendas, entre outras aplicações. 
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
# Vamos começar agora a algumas metricas.
# A taxa de conversão é uma métrica importante para entender o comportamento de compra dos clientes. Ela representa a proporção de clientes que realizam uma ação desejada, como adicionar um produto ao carrinho ou finalizar uma compra, em relação ao número total de clientes que visualizaram o produto. A taxa de conversão pode ser calculada utilizando a fórmula: 
# Taxa de Conversão = (Número de Ações Desejadas / Número Total de Visualizações) * 100
# %%
# Calculando a taxa de conversão para adição ao carrinho
add_to_cart_conversion_rate = (df['event_type'].value_counts()['cart'] / df['event_type'].value_counts()['view']) * 100
print(f"Taxa de Conversão View -> Adição ao Carrinho: {add_to_cart_conversion_rate:.2f}%")
# Calculando a taxa de conversão para compra
purchase_conversion_rate = (df['event_type'].value_counts()['purchase'] / df['event_type'].value_counts()['view']) * 100
print(f"Taxa de Conversão View -> Compra: {purchase_conversion_rate:.2f}%")
#Calculando a taxa de conversao  Cart -> Compra (baseado em USUÁRIOS, não eventos)
users_with_cart = df[df['event_type'] == 'cart']['user_id'].nunique()
users_with_purchase = df[df['event_type'] == 'purchase']['user_id'].nunique()
users_cart_to_purchase = len(set(df[df['event_type'] == 'cart']['user_id'].unique()) & set(df[df['event_type'] == 'purchase']['user_id'].unique()))
cart_to_purchase_conversion_rate = (users_cart_to_purchase / users_with_cart) * 100
print(f"Taxa de Conversão Cart -> Compra (usuários): {cart_to_purchase_conversion_rate:.2f}%")


# %%[markdown]
# Essas taxas de conversão indicam que há uma queda significativa no número de clientes que avançam do estágio de visualização para a adição ao carrinho e, posteriormente, para a compra. Isso sugere que muitos clientes estão apenas explorando os produtos sem necessariamente avançar para as etapas seguintes do funil de conversão. A alta taxa de conversão do carrinho para a compra indica que, uma vez que os clientes adicionam um produto ao carrinho, eles estão mais propensos a finalizar a compra. No entanto, a baixa taxa de conversão da visualização para a adição ao carrinho sugere que pode haver oportunidades para otimizar a experiência do usuário e incentivar mais clientes a avançar no processo de compra.
# NOTA: Os valores exatos de conversão calculados acima substituem as estimativas anteriores.
#%%[markdown]

import seaborn as sns
import matplotlib.pyplot as plt

# Grafico de barras com numeros absolutos de views, adições ao carrinho e compras
# Configurando estilo e cores
sns.set_style('whitegrid')
plt.figure(figsize=(12, 6))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
ax = sns.countplot(x='event_type', data=df, order=['view', 'cart', 'purchase'], palette=colors)

# Adicionar valores nas barras
for container in ax.containers:
    ax.bar_label(container, fmt='%d', padding=3, fontsize=11, weight='bold')

plt.title('Distribuição de Eventos no Funil de Compra', fontsize=16, weight='bold', pad=20)
plt.xlabel('Tipo de Evento', fontsize=13, weight='bold')
plt.ylabel('Contagem de Eventos', fontsize=13, weight='bold')
plt.xticks(['view', 'cart', 'purchase'], ['📺 Visualização', '🛒 Carrinho', '✅ Compra'], fontsize=12)
plt.yticks(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/01_funil_de_compra.png', dpi=300, bbox_inches='tight')
plt.show()
#%%[markdown]
# Observa-se um volume extremamente alto de visualizações (~40M), porém uma queda abrupta para eventos de adição ao carrinho e compra, indicando que o principal gargalo do funil está na transição de visualização para intenção de compra.
# %%[markdown]
# Agora vamos analisar os usuarios, começando com o total de usuarios unicos.
# Verificando o total de usuários únicos
unique_users = df['user_id'].nunique()
print(f"Total de usuários únicos: {unique_users}")
# %%[markdown]
# O dataset contém um total de `unique_users` usuários únicos (valor mostrado acima), o que indica uma grande base de clientes para análise. Essa diversidade de usuários pode fornecer insights valiosos sobre o comportamento de compra, preferências e padrões de consumo dos clientes. Com uma quantidade tão significativa de usuários únicos, é possível realizar análises segmentadas para identificar diferentes grupos de clientes e personalizar as estratégias de marketing e vendas de acordo com as necessidades e preferências de cada segmento.
# %%[markdown]
#Seguindo para média de eventos por usuario, essa métrica pode fornecer insights sobre o nível de engajamento dos clientes com a plataforma de comércio eletrônico. Uma média mais alta de eventos por usuário pode indicar que os clientes estão mais ativos e envolvidos com os produtos, enquanto uma média mais baixa pode sugerir que os clientes estão apenas explorando a plataforma sem interagir muito.
# Calculando a média de eventos por usuário
#%%
average_events_per_user = df.groupby('user_id')['event_type'].count().mean()
print(f"Média de eventos por usuário: {average_events_per_user:.2f}")
# %%[markdown]
# A média de eventos por usuário é de aproximadamente `average_events_per_user` (valor mostrado acima), o que indica o nível médio de engajamento dos clientes com a plataforma de comércio eletrônico. Essa métrica sugere o nível de engajamento dos clientes.
# %%[markdown]
# Quantos usuarios realizaram pelo menos um compra?
#<br></br>
# Calculando o número de usuários que realizaram pelo menos uma compra
#%%
users_with_purchase = df[df['event_type'] == 'purchase']['user_id'].nunique()
print(f"Número de usuários que realizaram pelo menos uma compra: {users_with_purchase}")
# %%[markdown]
# O número de usuários que realizaram pelo menos uma compra é de `users_with_purchase` (mostrado acima), correspondendo a uma porcentagem dos usuários únicos. Isso indica o nível de conversão de usuários na plataforma. No entanto, também sugere que há espaço para melhorar a taxa de conversão e incentivar mais usuários a realizar compras.
# %%[markdown]
# Vamos ver agora a diferença de comportamento entre os usuarios que realizam compras e os que não compram.
# Calculando a média de eventos por usuário para os usuários que realizaram compras
# %%
users_with_purchases = df[df['event_type'] == 'purchase']['user_id'].unique()
df_users_with_purchase = df[df['user_id'].isin(users_with_purchases)]
average_events_per_user_with_purchase = df_users_with_purchase.groupby('user_id')['event_type'].count().mean()
print(f"Média de eventos por usuário que realizou compras: {average_events_per_user_with_purchase:.2f}")
# Calculando a média de eventos por usuário para os usuários que não realizaram compras
users_without_purchases = df[~df['user_id'].isin(users_with_purchases)]['user_id'].unique()
df_users_without_purchase = df[df['user_id'].isin(users_without_purchases)]
average_events_per_user_without_purchase = df_users_without_purchase.groupby('user_id')['event_type'].count().mean()
print(f"Média de eventos por usuário que não realizou compras: {average_events_per_user_without_purchase:.2f}")
# %%[markdown]
# Comparação entre usuários que compram e usuários que não compram (valores acima):
# - Média de eventos por usuário que realizou compras: `average_events_per_user_with_purchase`
# - Média de eventos por usuário que não realizou compras: `average_events_per_user_without_purchase`
# Esses números mostram uma diferença significativa, sugerindo que aumentar o engajamento dos usuários pode ser uma estratégia eficaz para incentivar mais compras na plataforma de comércio eletrônico.
#%%[markdown]
# Comparação dos clientes que compram vs os que não compram
# Criando uma nova coluna para indicar se o usuário realizou uma compra ou não
df['purchase_made'] = df['user_id'].isin(users_with_purchases)
# Criando um gráfico de barras para comparar número absoluto deeventos por usuarios
# Gráfico comparativo com estilo melhorado
sns.set_style('whitegrid')
plt.figure(figsize=(10, 6))
colors_comparison = ['#E74C3C', '#27AE60']
ax2 = sns.countplot(x='purchase_made', data=df, palette=colors_comparison)

# Adicionar valores nas barras
for container in ax2.containers:
    ax2.bar_label(container, fmt='%d', padding=3, fontsize=11, weight='bold')

plt.title('Comparação: Compradores vs Não Compradores', fontsize=16, weight='bold', pad=20)
plt.xlabel('Status de Compra', fontsize=13, weight='bold')
plt.ylabel('Contagem de Eventos', fontsize=13, weight='bold')
plt.xticks([0, 1], ['❌ Não Comprou', '✅ Comprou'], fontsize=12)
plt.yticks(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/02_compradores_vs_nao_compradores.png', dpi=300, bbox_inches='tight')
plt.show()
#%%[markdown]
# 
# %%[markdown]
# <br></br>
# Agora iremos analisar as sessões dos usuários, começando com a porcentagem de sessões que viram compras.
#%%
# Calculando a porcentagem de sessões que viram compras
sessions_with_purchase = df[df['event_type'] == 'purchase']['user_session'].nunique()
total_sessions = df['user_session'].nunique()
purchase_session_percentage = (sessions_with_purchase / total_sessions) * 100
print(f"Porcentagem de sessões que viram compras: {purchase_session_percentage:.2f}%")
# %%[markdown]
# O percentual de sessões que resultaram em compras foi calculado acima (veja `purchase_session_percentage`). Isso indica o nível de conversão de sessões na plataforma. O resultado mostra que a maioria das sessões não resulta em compra, sugerindo que há uma oportunidade significativa para melhorar a experiência do usuário, otimizar o processo de compra e implementar estratégias de marketing mais eficazes para incentivar os clientes a avançar no funil de conversão e realizar compras.


# %%[markdown]
#<br></br>
# Agora vamos analisar a média de eventos por sessão, totais, com compra e sem compra.
# Calculando a média de eventos por sessão para todas as sessões
average_events_per_session = df.groupby('user_session')['event_type'].count().mean()
print(f"Média de eventos por sessão: {average_events_per_session:.2f}")
# Calculando a média de eventos por sessão para sessões com compra
sessions_with_purchases = df[df['event_type'] == 'purchase']['user_session'].unique()
df_sessions_with_purchase = df[df['user_session'].isin(sessions_with_purchases)]        
average_events_per_session_with_purchase = df_sessions_with_purchase.groupby('user_session')['event_type'].count().mean()
print(f"Média de eventos por sessão com compra: {average_events_per_session_with_purchase:.2f}")
# Calculando a média de eventos por sessão para sessões sem compra
sessions_without_purchases = df[~df['user_session'].isin(sessions_with_purchases)]['user_session'].unique()
df_sessions_without_purchase = df[df['user_session'].isin(sessions_without_purchases)]
average_events_per_session_without_purchase = df_sessions_without_purchase.groupby('user_session')['event_type'].count().mean()
print(f"Média de eventos por sessão sem compra: {average_events_per_session_without_purchase:.2f}")
#%%[markdown]
#Veremos graficamente a comparação entre sessões com compra e sem compra.
# %%
# Gráfico comparativo: Média de eventos por sessão (com vs sem compra)
sns.set_style('whitegrid')
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Gráfico 1: Contagem de sessões
session_counts = ['Com Compra', 'Sem Compra']
session_values = [sessions_with_purchase, total_sessions - sessions_with_purchase]
colors1 = ['#27AE60', '#E74C3C']
bars1 = axes[0].bar(session_counts, session_values, color=colors1, edgecolor='black', linewidth=2)
for bar in bars1:
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontsize=12, weight='bold')
axes[0].set_title('Total de Sessões: Com vs Sem Compra', fontsize=14, weight='bold', pad=15)
axes[0].set_ylabel('Contagem de Sessões', fontsize=12, weight='bold')
axes[0].grid(axis='y', alpha=0.3)

# Gráfico 2: Média de eventos por sessão
session_types = ['Com Compra', 'Sem Compra']
session_avg = [average_events_per_session_with_purchase, average_events_per_session_without_purchase]
colors2 = ['#3498DB', '#F39C12']
bars2 = axes[1].bar(session_types, session_avg, color=colors2, edgecolor='black', linewidth=2)
for bar in bars2:
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=12, weight='bold')
axes[1].set_title('Média de Eventos por Sessão', fontsize=14, weight='bold', pad=15)
axes[1].set_ylabel('Média de Eventos', fontsize=12, weight='bold')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../reports/03_analise_sessoes.png', dpi=300, bbox_inches='tight')
plt.show()  
#%%[markdown]
# Vemos que a maioria das sessões não resultam em compra, mas as sessões que resultam em compra têm uma média significativamente maior de eventos, indicando um engajamento muito mais alto. Isso sugere que os clientes que estão mais engajados e interagindo mais com a plataforma têm uma probabilidade muito maior de realizar uma compra. Portanto, estratégias para aumentar o engajamento dos usuários podem ser eficazes para melhorar as taxas de conversão e incentivar mais compras na plataforma.
# %%
# Gerando relatório final com todos os valores calculados
final_report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               RELATÓRIO FINAL - ANÁLISE DE COMPORTAMENTO DE E-COMMERCE        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 MÉTRICAS DE CONVERSÃO:
  • Taxa de Conversão (View → Carrinho): {add_to_cart_conversion_rate:.2f}%
  • Taxa de Conversão (View → Compra): {purchase_conversion_rate:.2f}%
  • Taxa de Conversão (Carrinho → Compra): {cart_to_purchase_conversion_rate:.2f}%

👥 ANÁLISE DE USUÁRIOS:
  • Total de usuários únicos: {unique_users:,}
  • Usuários que realizaram compra: {users_with_purchase:,}
  • Percentual de compradores: {(users_with_purchase/unique_users)*100:.2f}%
  • Média de eventos por usuário (geral): {average_events_per_user:.2f}
  • Média de eventos por usuário (com compra): {average_events_per_user_with_purchase:.2f}
  • Média de eventos por usuário (sem compra): {average_events_per_user_without_purchase:.2f}
  • Ratio de engajamento (com/sem compra): {average_events_per_user_with_purchase/average_events_per_user_without_purchase:.2f}x

📱 ANÁLISE DE SESSÕES:
  • Total de sessões: {total_sessions:,}
  • Sessões com compra: {sessions_with_purchase:,}
  • Percentual de sessões com compra: {purchase_session_percentage:.2f}%
  • Média de eventos por sessão (geral): {average_events_per_session:.2f}
  • Média de eventos por sessão (com compra): {average_events_per_session_with_purchase:.2f}
  • Média de eventos por sessão (sem compra): {average_events_per_session_without_purchase:.2f}

╔══════════════════════════════════════════════════════════════════════════════╗
║                         CONCLUSÕES PRINCIPAIS                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

1️⃣  FUNIL DE CONVERSÃO: Há uma queda significativa de visualizações para 
    adições ao carrinho ({add_to_cart_conversion_rate:.2f}%), indicando um gargalo crítico.

2️⃣  ENGAJAMENTO: Usuários que realizam compras têm {average_events_per_user_with_purchase/average_events_per_user_without_purchase:.2f}x mais 
    interações do que não-compradores.

3️⃣  TAXA FINAL: Apenas {purchase_conversion_rate:.2f}% dos usuários que visualizam
    produtos chegam a comprar.

4️⃣  CARRINHO: Taxa de conversão de {cart_to_purchase_conversion_rate:.2f}% (carrinho → compra) mostra que
    o desafio maior é levar usuários a adicionar produtos ao carrinho.
"""
print(final_report)
