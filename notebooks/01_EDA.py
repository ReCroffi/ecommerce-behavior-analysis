#%%
import kagglehub
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Download latest version
path = kagglehub.dataset_download("mkechinov/ecommerce-behavior-data-from-multi-category-store")
print("Path to dataset files:", path)
# %%

# Carregando os dados
df = pd.read_csv(f"{path}/2019-Oct.csv", nrows=1_000_000)
sns.set_style('whitegrid')

# %%
def compute_conversion_rates(df, event_counts, purchase_user_ids):
    cart_user_ids = df[df['event_type'] == 'cart']['user_id'].unique()
    add_to_cart = event_counts['cart'] / event_counts['view'] * 100
    view_to_purchase = event_counts['purchase'] / event_counts['view'] * 100
    cart_to_purchase = len(set(cart_user_ids) & set(purchase_user_ids)) / len(cart_user_ids) * 100
    return add_to_cart, view_to_purchase, cart_to_purchase


def compare_engagement(df, group_col, group_ids):
    counts = df.groupby(group_col)['event_type'].count()
    avg_overall = counts.mean()
    avg_with = counts[counts.index.isin(group_ids)].mean()
    avg_without = counts[~counts.index.isin(group_ids)].mean()
    return avg_overall, avg_with, avg_without


def plot_funnel(df, save_path='../reports/01_funil_de_compra.png'):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='event_type', data=df, order=['view', 'cart', 'purchase'],
                  palette=['#FF6B6B', '#4ECDC4', '#45B7D1'], ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', padding=3, fontsize=11, weight='bold')
    ax.set_title('Distribuição de Eventos no Funil de Compra', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Tipo de Evento', fontsize=13, weight='bold')
    ax.set_ylabel('Contagem de Eventos', fontsize=13, weight='bold')
    ax.set_xticklabels(['📺 Visualização', '🛒 Carrinho', '✅ Compra'], fontsize=12)
    ax.tick_params(axis='y', labelsize=11)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_buyers_comparison(df, purchase_user_ids, save_path='../reports/02_compradores_vs_nao_compradores.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    purchase_made = df['user_id'].isin(purchase_user_ids)
    sns.countplot(x=purchase_made, order=[False, True], palette=['#E74C3C', '#27AE60'], ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', padding=3, fontsize=11, weight='bold')
    ax.set_title('Comparação: Compradores vs Não Compradores', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Status de Compra', fontsize=13, weight='bold')
    ax.set_ylabel('Contagem de Eventos', fontsize=13, weight='bold')
    ax.set_xticklabels(['❌ Não Comprou', '✅ Comprou'], fontsize=12)
    ax.tick_params(axis='y', labelsize=11)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_sessions_analysis(sessions_with_purchase, total_sessions, avg_with, avg_without,
                           save_path='../reports/03_analise_sessoes.png'):
    _, axes = plt.subplots(1, 2, figsize=(14, 6))
    labels = ['Com Compra', 'Sem Compra']

    # Gráfico 1: Contagem de sessões
    bars1 = axes[0].bar(labels, [sessions_with_purchase, total_sessions - sessions_with_purchase],
                        color=['#27AE60', '#E74C3C'], edgecolor='black', linewidth=2)
    for bar in bars1:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2., height,
                     f'{int(height):,}', ha='center', va='bottom', fontsize=12, weight='bold')
    axes[0].set_title('Total de Sessões: Com vs Sem Compra', fontsize=14, weight='bold', pad=15)
    axes[0].set_ylabel('Contagem de Sessões', fontsize=12, weight='bold')
    axes[0].grid(axis='y', alpha=0.3)

    # Gráfico 2: Média de eventos por sessão
    bars2 = axes[1].bar(labels, [avg_with, avg_without],
                        color=['#3498DB', '#F39C12'], edgecolor='black', linewidth=2)
    for bar in bars2:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.2f}', ha='center', va='bottom', fontsize=12, weight='bold')
    axes[1].set_title('Média de Eventos por Sessão', fontsize=14, weight='bold', pad=15)
    axes[1].set_ylabel('Média de Eventos', fontsize=12, weight='bold')
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def print_final_report(add_to_cart_rate, view_to_purchase_rate, cart_to_purchase_rate,
                       unique_users, users_with_purchase,
                       avg_events_user, avg_events_buyer, avg_events_non_buyer,
                       total_sessions, sessions_with_purchase, purchase_session_pct,
                       avg_events_session, avg_events_session_with, avg_events_session_without):
    ratio = avg_events_buyer / avg_events_non_buyer
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               RELATÓRIO FINAL - ANÁLISE DE COMPORTAMENTO DE E-COMMERCE        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 MÉTRICAS DE CONVERSÃO:
  • Taxa de Conversão (View → Carrinho): {add_to_cart_rate:.2f}%
  • Taxa de Conversão (View → Compra): {view_to_purchase_rate:.2f}%
  • Taxa de Conversão (Carrinho → Compra): {cart_to_purchase_rate:.2f}%

👥 ANÁLISE DE USUÁRIOS:
  • Total de usuários únicos: {unique_users:,}
  • Usuários que realizaram compra: {users_with_purchase:,}
  • Percentual de compradores: {users_with_purchase / unique_users * 100:.2f}%
  • Média de eventos por usuário (geral): {avg_events_user:.2f}
  • Média de eventos por usuário (com compra): {avg_events_buyer:.2f}
  • Média de eventos por usuário (sem compra): {avg_events_non_buyer:.2f}
  • Ratio de engajamento (com/sem compra): {ratio:.2f}x

📱 ANÁLISE DE SESSÕES:
  • Total de sessões: {total_sessions:,}
  • Sessões com compra: {sessions_with_purchase:,}
  • Percentual de sessões com compra: {purchase_session_pct:.2f}%
  • Média de eventos por sessão (geral): {avg_events_session:.2f}
  • Média de eventos por sessão (com compra): {avg_events_session_with:.2f}
  • Média de eventos por sessão (sem compra): {avg_events_session_without:.2f}

╔══════════════════════════════════════════════════════════════════════════════╗
║                         CONCLUSÕES PRINCIPAIS                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

1️⃣  FUNIL DE CONVERSÃO: Há uma queda significativa de visualizações para
    adições ao carrinho ({add_to_cart_rate:.2f}%), indicando um gargalo crítico.

2️⃣  ENGAJAMENTO: Usuários que realizam compras têm {ratio:.2f}x mais
    interações do que não-compradores.

3️⃣  TAXA FINAL: Apenas {view_to_purchase_rate:.2f}% dos usuários que visualizam
    produtos chegam a comprar.

4️⃣  CARRINHO: Taxa de conversão de {cart_to_purchase_rate:.2f}% (carrinho → compra) mostra que
    o desafio maior é levar usuários a adicionar produtos ao carrinho.
""")

#%%
df.head()
# %%
df.info()
# %%[markdown]
# O dataset contém informações sobre o comportamento de compra dos clientes em uma loja de e-commerce multi-categoria.
# As colunas incluem:
# - `event_time`: Data e hora do evento.
# - `event_type`: Tipo de evento — `view`, `cart` ou `purchase`.
# - `product_id`: Identificador do produto.
# - `category_id`: Identificador da categoria do produto.
# - `category_code`: Código legível da categoria (ex: `electronics.smartphone`).
# - `brand`: Marca do produto.
# - `price`: Preço do produto em USD.
# - `user_id`: Identificador único do usuário.
# - `user_session`: Identificador da sessão de navegação.
#%%[markdown]
# Cada linha representa um evento de interação entre um usuário e um produto: visualização (`view`), adição ao carrinho (`cart`) ou compra (`purchase`).
# Combinando `user_id`, `user_session` e `event_type`, é possível reconstruir a jornada de compra de cada cliente e analisar o funil de conversão.
# %%[markdown]
# O dataset completo contém mais de 42 milhões de linhas. Para este EDA, carregamos 1 milhão de linhas — suficiente para identificar padrões representativos sem sobrecarregar a memória.
# %%[markdown]
# Vamos verificar a qualidade dos dados: valores nulos e linhas duplicadas.
# %%
df.isnull().sum()
# %%
df.duplicated().sum()
# %%[markdown]
# As colunas com maior presença de nulos são `category_code` e `brand` — campos descritivos que não são essenciais para a análise do funil de conversão. Os nulos nessas colunas podem ser ignorados ou tratados como categoria "desconhecida" conforme o contexto da análise.
# As linhas duplicadas serão investigadas a seguir para decidir como tratá-las.
# %%
df[df.duplicated()]
# %%[markdown]
# Agora vamos confirmar se as duplicatas são 100% idênticas em todas as colunas, ou apenas parcialmente coincidentes.
# %%
df[df.duplicated(keep=False)].sort_values(by='event_time')
# %%[markdown]
# As duplicatas são registros completamente idênticos — mesmo usuário, produto, preço, sessão e timestamp. Isso indica erros de ingestão de dados, não eventos reais distintos. O ideal é removê-las com `drop_duplicates()` antes de análises quantitativas.
# %%[markdown]
# Vamos agora verificar a distribuição dos tipos de evento para entender como os usuários se comportam ao longo do funil de compra.
# %%
event_counts = df['event_type'].value_counts()
print(event_counts)
# %%
event_proportions = event_counts / event_counts.sum() * 100
print(event_proportions)
# %%[markdown]
# Como esperado, `view` domina o volume de eventos. A proporção de `cart` e `purchase` é consideravelmente menor, sinalizando um funil com alto nível de abandono antes da conversão.
# %%[markdown]
# ## Taxas de Conversão
# Calculamos três métricas de conversão para mapear os gargalos do funil:
# - **View → Carrinho**: proporção de visualizações que resultam em adição ao carrinho (baseada em eventos)
# - **View → Compra**: proporção de visualizações que resultam em compra (baseada em eventos)
# - **Carrinho → Compra**: proporção de usuários que adicionaram ao carrinho e também realizaram ao menos uma compra
# %%
purchase_user_ids = df[df['event_type'] == 'purchase']['user_id'].unique()

add_to_cart_conversion_rate, purchase_conversion_rate, cart_to_purchase_conversion_rate = \
    compute_conversion_rates(df, event_counts, purchase_user_ids)

print(f"Taxa de Conversão View -> Adição ao Carrinho: {add_to_cart_conversion_rate:.2f}%")
print(f"Taxa de Conversão View -> Compra: {purchase_conversion_rate:.2f}%")
print(f"Taxa de Conversão Cart -> Compra (usuários): {cart_to_purchase_conversion_rate:.2f}%")

# %%[markdown]
# O funil revela dois gargalos distintos:
# 1. A conversão de visualização para carrinho é baixa — a maioria dos usuários não demonstra intenção de compra após ver o produto.
# 2. A conversão de carrinho para compra é substancialmente mais alta — usuários que chegam ao carrinho têm alta probabilidade de concluir a compra.
#
# Isso indica que o principal desafio da plataforma é engajar o usuário o suficiente para levá-lo a considerar a compra, não necessariamente fechar a venda após essa decisão.
#%%

# Grafico de barras com numeros absolutos de views, adições ao carrinho e compras
plot_funnel(df)
#%%[markdown]
# O gráfico evidencia a queda abrupta entre visualizações e os demais eventos. O gargalo principal está na transição de `view` para `cart` — onde a grande maioria dos usuários abandona o funil.
# %%[markdown]
# ## Análise de Usuários
# %%
unique_users = df['user_id'].nunique()
print(f"Total de usuários únicos: {unique_users}")
# %%[markdown]
# A amostra contém uma base diversa de usuários, o que permite análises segmentadas com boa representatividade estatística.
# %%[markdown]
# A média de eventos por usuário indica o nível geral de engajamento com a plataforma. Valores baixos sugerem navegação superficial; valores mais altos indicam usuários que exploram ativamente o catálogo.
#%%
users_with_purchase = len(purchase_user_ids)
print(f"Usuários que realizaram pelo menos uma compra: {users_with_purchase} ({users_with_purchase/unique_users*100:.1f}% do total)")
# %%[markdown]
# Agora separamos os usuários entre compradores e não-compradores para comparar seus padrões de engajamento.
# %%
average_events_per_user, average_events_per_user_with_purchase, average_events_per_user_without_purchase = \
    compare_engagement(df, 'user_id', purchase_user_ids)

print(f"Média de eventos por usuário: {average_events_per_user:.2f}")
print(f"Média de eventos — compradores:     {average_events_per_user_with_purchase:.2f}")
print(f"Média de eventos — não-compradores: {average_events_per_user_without_purchase:.2f}")
# %%[markdown]
# Compradores geram significativamente mais eventos do que não-compradores. Isso confirma que engajamento e conversão estão correlacionados: usuários que interagem mais com a plataforma têm maior probabilidade de comprar. Estratégias que aumentem o número de interações por sessão podem impactar positivamente as taxas de conversão.
#%%[markdown]
# O gráfico abaixo mostra a proporção de eventos gerados por cada grupo.
# %%
plot_buyers_comparison(df, purchase_user_ids)
# %%[markdown]
# ## Análise de Sessões
# Agora analisamos as sessões de navegação para entender em que proporção elas resultam em compra e como o comportamento difere entre sessões com e sem compra.
#%%
purchase_session_ids = df[df['event_type'] == 'purchase']['user_session'].unique()
sessions_with_purchase = len(purchase_session_ids)
total_sessions = df['user_session'].nunique()
purchase_session_percentage = sessions_with_purchase / total_sessions * 100
print(f"Sessões com compra: {sessions_with_purchase:,} de {total_sessions:,} ({purchase_session_percentage:.2f}%)")
# %%[markdown]
# A grande maioria das sessões não resulta em compra. No entanto, isso é esperado em e-commerce — o comportamento de navegação sem intenção imediata de compra é comum. O dado relevante é o que diferencia as sessões que convertem das que não convertem.
# %%
average_events_per_session, average_events_per_session_with_purchase, average_events_per_session_without_purchase = \
    compare_engagement(df, 'user_session', purchase_session_ids)

print(f"Média de eventos por sessão (geral):       {average_events_per_session:.2f}")
print(f"Média de eventos por sessão (com compra):  {average_events_per_session_with_purchase:.2f}")
print(f"Média de eventos por sessão (sem compra):  {average_events_per_session_without_purchase:.2f}")
#%%[markdown]
# Sessões que resultam em compra têm uma média de eventos muito superior às que não convertem. Isso reforça a correlação entre engajamento e conversão observada na análise de usuários: quanto mais o cliente interage dentro de uma sessão, maior a probabilidade de compra.
# %%
plot_sessions_analysis(sessions_with_purchase, total_sessions,
                       average_events_per_session_with_purchase,
                       average_events_per_session_without_purchase)
# %%
# Gerando relatório final com todos os valores calculados
print_final_report(
    add_to_cart_conversion_rate, purchase_conversion_rate, cart_to_purchase_conversion_rate,
    unique_users, users_with_purchase,
    average_events_per_user, average_events_per_user_with_purchase, average_events_per_user_without_purchase,
    total_sessions, sessions_with_purchase, purchase_session_percentage,
    average_events_per_session, average_events_per_session_with_purchase, average_events_per_session_without_purchase,
)
