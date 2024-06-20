import tkinter as tk
from tkinter import messagebox, scrolledtext
from customtkinter import * 
from PIL import Image
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
def fazer_previsao_manual(valores_usuario):
    entrada_usuario = np.array(valores_usuario).reshape(1, -1)
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
    
    return previsao, resultado

# Lista de textos personalizados para as labels
labels_personalizadas = [
    "RPM (Rotações por Minuto) (0-5000)",
    "Torque (0.0-70.0)",
    "Desgaste (0-240)",
    "TWF (0-1)",
    "HDF (0-1)",
    "PWF (0-1)",
    "OSF (0-1)"
]

# Criação da interface gráfica com Tkinter
def criar_interface():

    # Função para processar a previsão quando o botão for clicado
    def processar_previsao():
        try:
            valores_usuario = [float(entry.get()) for entry in entradas]
            previsao, resultado = fazer_previsao_manual(valores_usuario)
            messagebox.showinfo("Resultado da Previsão", f"Saída prevista: {previsao:.2f}\nResultado: {resultado}")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores válidos para todas as colunas.")

    # Função para abrir a janela de ajuda
    def abrir_janela_ajuda():
        #help_window = tk.Toplevel(root)
        help_window = CTkToplevel(root)
        help_window.title("Ajuda - Previsão de Falhas de Máquina")
        help_window.geometry("400x300")
        
        # Texto de ajuda
        try:
            with open('ajuda.txt', 'r', encoding='utf-8') as file:
                help_text = file.read()
        except FileNotFoundError:
            help_text = "Arquivo de ajuda não encontrado."
        
        # Caixa de texto com barra de rolagem para exibir o texto de ajuda
        text_area = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=40, height=10)
        text_area.insert(tk.END, help_text)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Botão para fechar a janela de ajuda
        #close_button = tk.Button(help_window, text="Fechar", command=help_window.destroy)
        close_button = CTkButton(help_window, text="Fechar", corner_radius=26, fg_color="#1B2CC1", hover_color="#3D518C" ,command=help_window.destroy)
        close_button.pack(pady=10)
        
    set_appearance_mode("dark")

    # Criar a janela principal
    #root = tk.Tk()
    root=CTk()
    root.title("Previsão de Falhas de Máquina")
    root.geometry("500x600")
    set_appearance_mode("dark")

    # Obter a largura e a altura da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    
    # Calcular a posição para centralizar a janela
    posicao_x = int(largura_tela / 2 - 500 / 2)  # 500 é a largura da janela principal
    posicao_y = int(altura_tela / 2 - 600 / 2)   # 600 é a altura da janela principal
    
    # Definir a posição da janela
    root.geometry(f"500x600+{posicao_x}+{posicao_y}")

    # Criar um comando de validação
    vcmd = (root.register(validar_entrada), '%P')

    # Criar labels e entradas para cada coluna
    # entradas = []
    # for texto_label in labels_personalizadas:
    #     label = tk.Label(root, text=texto_label)
    #     label.pack()
    #     entry = tk.Entry(root, validate='key', validatecommand=vcmd)
    #     entry.pack()
    #     entradas.append(entry)

    entradas = []
    for texto_label in labels_personalizadas:
        label = CTkLabel(root, text=texto_label)
        label.pack()
        entry = CTkEntry(root, validate='key', validatecommand=vcmd)
        entry.pack()
        entradas.append(entry)

    # Criar botão para fazer a previsão
    #button = tk.Button(root, text="Fazer Previsão", command=processar_previsao)
    #button.pack(pady=20)

    #NOVO Botão Previsão
    botao = CTkButton(master=root, text="Fazer previsão", corner_radius=26, fg_color="#1B2CC1", hover_color="#3D518C" , command=processar_previsao)
    botao.pack(pady=20)

    # Botão para abrir a janela de ajuda
    help_button = CTkButton(master=root, text="Ajuda", corner_radius=26, fg_color="#1B2CC1", hover_color="#3D518C" , command=abrir_janela_ajuda)
    help_button.pack(pady=10)

    # Iniciar o loop principal da interface
    root.mainloop()

# Função de callback para validar entrada numérica
def validar_entrada(P):
    if P == "" or P.replace('.', '', 1).isdigit():
        return True
    return False

# Chamar a função para criar a interface
criar_interface()

