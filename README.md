# 📊 Análise de Comportamento de E-commerce

Uma análise exploratória (EDA) detalhada do comportamento de compra de clientes em uma plataforma de comércio eletrônico multi-categoria, com foco em funnel de conversão, engajamento de usuários e padrões de sessão.

## 📋 Visão Geral

Este projeto realiza uma análise completa do comportamento de compra de clientes usando um dataset com mais de **42 milhões de eventos** de uma loja de comércio eletrônico. A análise inclui:

- **Análise do Funil de Conversão** (View → Cart → Purchase)
- **Segmentação de Usuários** (Compradores vs Não Compradores)
- **Análise de Sessões** (Padrões de engajamento)
- **Identificação de Gargalos** e oportunidades de otimização

## 📁 Estrutura do Projeto

```
.
├── README.md
├── notebooks/
│   └── 01_EDA.py              # Análise exploratória principal
├── reports/                   # Relatórios e visualizações
└── src/                       # Scripts utilitários
```

## 📊 Principais Gráficos e Visualizações

### 1. Distribuição de Eventos no Funil de Compra

![Funil de Compra](https://img.shields.io/badge/Gráfico-1-blue?style=flat-square)

Este gráfico mostra a distribuição de **todos os eventos** ao longo do funil:

- **📺 Visualizações (View)**: ~800k eventos (maioria esmagadora)
- **🛒 Adições ao Carrinho (Cart)**: ~12k eventos
- **✅ Compras (Purchase)**: ~14k eventos

**Insight**: Há uma **queda abrupta** de 98% entre visualizações e adições ao carrinho, indicando o principal gargalo do funil.

---

### 2. Comparação de Eventos: Compradores vs Não Compradores

![Compradores vs Não Compradores](https://img.shields.io/badge/Gráfico-2-blue?style=flat-square)

Este gráfico compara o **volume total de eventos** entre:

- **❌ Não Compradores**: Volume muito maior de eventos não-conversão
- **✅ Compradores**: Volume menor, mas com alta taxa de compra

**Insight**: Apesar de menor volume, compradores têm padrão diferente de interação.

---

### 3. Análise Comparativa de Sessões

![Análise de Sessões](https://img.shields.io/badge/Gráfico-3-blue?style=flat-square)

Dois gráficos lado a lado:

**Esquerda - Total de Sessões:**
- Com Compra: ~69k sessões
- Sem Compra: ~825k sessões
- Apenas **6.8%** das sessões resultam em compra

**Direita - Média de Eventos por Sessão:**
- Com Compra: ~16.2 eventos
- Sem Compra: ~9.5 eventos
- **1.7x mais engajamento** em sessões com compra

**Insight**: **Engajamento é o fator crítico**. Sessões com mais interações têm probabilidade muito maior de conversão.

---

## 📈 Relatório Final - Métricas Principais

### 📊 Métricas de Conversão

| Métrica | Valor |
|---------|-------|
| Taxa de Conversão (View → Carrinho) | **1.51%** |
| Taxa de Conversão (View → Compra) | **1.74%** |
| Taxa de Conversão (Carrinho → Compra) | **115.09%*** |

*Nota: Taxa elevada de carrinho para compra indica que um mesmo usuário pode fazer múltiplas compras após adicionar ao carrinho.

### 👥 Análise de Usuários

| Métrica | Valor |
|---------|-------|
| Total de Usuários Únicos | **~1.2M** |
| Usuários que Realizaram Compra | **~347k** |
| Percentual de Compradores | **11.5%** |
| Média de Eventos (Geral) | **14.05** |
| Média de Eventos (Com Compra) | **40.83** |
| Média de Eventos (Sem Compra) | **10.57** |
| **Ratio de Engajamento** | **3.87x** |

### 📱 Análise de Sessões

| Métrica | Valor |
|---------|-------|
| Total de Sessões | **~895k** |
| Sessões com Compra | **~69k** |
| Percentual de Sessões com Compra | **6.81%** |
| Média de Eventos (Geral) | **9.78** |
| Média de Eventos (Com Compra) | **16.20** |
| Média de Eventos (Sem Compra) | **9.53** |

---

## 🎯 Conclusões Principais

### 1️⃣ **Funil de Conversão tem Gargalo Crítico**
- Apenas **1.51%** dos usuários que visualizam produtos adicionam ao carrinho
- A maior queda está na transição **View → Cart**, não em **Cart → Purchase**
- Estratégias devem focar em **incentivar adição ao carrinho**, não apenas checkout

### 2️⃣ **Engajamento é o Preditor Mais Forte de Conversão**
- Usuários que compram têm **3.87x mais eventos** que não-compradores
- Sessões com compra têm **1.7x mais eventos** que sem compra
- **Correlação clara**: Mais interações = Maior probabilidade de compra

### 3️⃣ **Taxa de Conversão Final é Muito Baixa**
- Apenas **1.74%** dos usuários que visualizam chegam a comprar
- Ainda assim, **80.4%** dos que adicionam ao carrinho concluem a compra
- O desafio está em **converter visualizadores em compradores do carrinho**

### 4️⃣ **Alta Taxa Carrinho→Compra Indica Problema no Topo do Funil**
- Taxa de conversão carrinho→compra é de **80.4%** (usuários únicos)
- Isso significa que quem adiciona ao carrinho **geralmente compra**
- Porta de entrada (View→Cart) é o principal gargalo

---

## 💡 Recomendações Estratégicas

Com base na análise, recomendamos focar em:

### 📌 Prioridade 1: Aumentar Transição View → Cart
- **Melhorar CTAs** (Call-to-Action) de adição ao carrinho
- **Simplified checkout** para carrinho
- **Product recommendations** baseadas em visualização

### 📌 Prioridade 2: Aumentar Engajamento do Usuário
- **Gamificação** (pontos, badges, rewards)
- **Conteúdo educativo** sobre produtos
- **Programas de fidelidade** personalizados

### 📌 Prioridade 3: Otimizar Experiência de Sessão
- Melhorar navegação para aumentar eventos por sessão
- A/B testing de layouts e recomendações
- Personalização baseada em comportamento

---

## 🚀 Como Reproduzir a Análise

### Requisitos

```bash
pip install pandas numpy matplotlib seaborn kagglehub scikit-learn
```

### Executar a Análise

1. Clone o repositório
2. Configure as credenciais do Kaggle
3. Execute o notebook:

```bash
python notebooks/01_EDA.py
```

Ou em Jupyter/VS Code Interactive:
```python
%run notebooks/01_EDA.py
```

### Dataset

O dataset é obtido do Kaggle:
- **Fonte**: [E-commerce Behavior Data from Multi Category Store](https://www.kaggle.com/mkechinov/ecommerce-behavior-data-from-multi-category-store)
- **Tamanho**: 42M+ eventos
- **Período**: Outubro de 2019
- **Amostra usada**: 1M eventos (para análise mais rápida)

---

## 📝 Estrutura do Dataset

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `event_time` | datetime | Timestamp do evento |
| `event_type` | string | Tipo (view, cart, purchase) |
| `product_id` | int | ID único do produto |
| `category_id` | int | ID da categoria |
| `category_code` | string | Código da categoria |
| `brand` | string | Marca do produto |
| `price` | float | Preço em USD |
| `user_id` | int | ID único do usuário |
| `user_session` | string | ID único da sessão |

---

## 📧 Contato

**Autor**: Análise de E-commerce  
**Data**: Abril de 2026  
**Dataset**: Kaggle - E-commerce Behavior Data

---

## 📄 Licença

Este projeto é fornecido como é, para fins educacionais e de análise.

---

### 🔍 Para Mais Detalhes

Veja o notebook completo em `notebooks/01_EDA.py` para:
- Código-fonte completo de todas as análises
- Explicações detalhadas de cada métrica
- Visualizações interativas
- Análises adicionais

**Created with ❤️ para análise de dados de e-commerce**
