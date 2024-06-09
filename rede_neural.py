import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Carregar os dados do arquivo CSV
data = pd.read_csv("machine_failure_cleaned.csv")

# Separar os dados em features (X) e rótulos (y)
X = data.drop('Machine failure', axis=1).values
y = data['Machine failure'].values

# Obter os nomes das colunas
colunas = data.drop('Machine failure', axis=1).columns

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Construir o modelo
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(1)
])

# Compilar o modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Treinar o modelo
model.fit(X_train, y_train, epochs=10, batch_size=64, validation_split=0.2)

# Avaliar o modelo
loss = model.evaluate(X_test, y_test)
print("Loss:", loss)

# Função para fazer previsões a partir de entradas do usuário
def fazer_previsao_manual():
    entrada_usuario = []
    for i, coluna in enumerate(colunas):
        valor = float(input(f"Digite o valor para a coluna '{coluna}': "))
        entrada_usuario.append(valor)
    
    # Converter para array numpy e normalizar
    entrada_usuario = np.array(entrada_usuario).reshape(1, -1)
    entrada_usuario = scaler.transform(entrada_usuario)
    
    # Fazer a previsão
    previsao = model.predict(entrada_usuario)[0][0]

    # Avaliar a previsão
    if previsao > 1:
        resultado = "Falha de máquina"
    elif 0.95 <= previsao <= 1:
        resultado = "Grande chance de falhas"
    elif 0.85 <= previsao < 0.95:
        resultado = "Chances de falha"
    else:
        resultado = "Baixas chances de falha"
    
    print(f"Saída prevista para a entrada fornecida: {previsao:.2f}")
    print(f"Resultado: {resultado}")

# Solicitar ao usuário se deseja fazer uma previsão manual
while True:
    opcao = input("Você quer fazer uma previsão manual? (s/n): ").lower()
    if opcao == 's':
        fazer_previsao_manual()
    elif opcao == 'n':
        break
    else:
        print("Opção inválida. Por favor, digite 's' para sim ou 'n' para não.")
