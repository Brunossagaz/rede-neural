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

# Fazer previsões
predictions = model.predict(X_test)

# Exibir algumas previsões
for i in range(5):
    print("Entrada:", X_test[i])
    print("Saída real:", y_test[i])
    print("Saída prevista:", predictions[i])
    print()
