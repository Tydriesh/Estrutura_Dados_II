# Analise Bovespa com Árvore de Decisão
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Carregar os dados
df = pd.read_csv("Bovespa.csv")  # <- Substitua se o arquivo tiver outro nome

# 2. Filtrar dados da Petrobras
df = df[df["Ticker"].isin(["PETR3", "PETR4"])].copy()

# 3. Conversão de dados numéricos
for col in ["Open", "High", "Low", "Close", "Volume"]:
    df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df = df.sort_values(by=["Ticker", "Date"])

# 4. Criar variáveis derivadas
df["Return"] = df.groupby("Ticker")["Close"].pct_change()
df["MM5"] = df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(5).mean())
df["Vol5"] = df.groupby("Ticker")["Return"].transform(lambda x: x.rolling(5).std())
df["Target"] = df.groupby("Ticker")["Close"].shift(-1)
df.dropna(inplace=True)

# 5. Preparar dados para modelo
features = ["Open", "High", "Low", "Close", "Volume", "MM5", "Vol5"]
X = df[features]
y = df["Target"]

# 6. Dividir treino e teste
split_idx = int(len(df) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# 7. Treinar modelo de Árvore de Decisão
model = DecisionTreeRegressor(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 8. Previsões e avaliação
df["Predicted"] = model.predict(X)
mae = mean_absolute_error(y_test, model.predict(X_test))
r2 = r2_score(y_test, model.predict(X_test))

print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")

# 9. Gráfico da estrutura da árvore
plt.figure(figsize=(20, 10))
plot_tree(model,
          feature_names=features,
          filled=True,
          rounded=True,
          fontsize=10)
plt.title("Estrutura da Árvore de Decisão - Previsão de Fechamento")
plt.savefig("arvore_decisao_bovespa.png", dpi=300)
plt.show()

# 10. Gráficos: comparação com variáveis de entrada
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 12))
axes = axes.flatten()

for idx, col in enumerate(features):
    sns.regplot(data=df, x=col, y="Predicted", ax=axes[idx],
                scatter_kws={"alpha": 0.5},
                line_kws={"color": "red"})
    axes[idx].set_title(f"Predição vs {col}")
    axes[idx].set_ylabel("Fechamento Previsto")
    axes[idx].set_xlabel(col)

for j in range(len(features), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.suptitle("Comparação entre Variáveis de Entrada e Previsões (Árvore de Decisão)", fontsize=16, y=1.02)
plt.show()
