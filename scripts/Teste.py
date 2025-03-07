import pandas as pd
import google.generativeai as genai
import os

# Caminho para o arquivo Excel
caminho_arquivo = os.path.join("data", "processed_data", "Meganium_Sales_data.xlsx")

try:
    # Carrega o arquivo Excel usando pandas
    df = pd.read_excel(caminho_arquivo)

    # Faça o que você precisa com o DataFrame (df)
    print(df.head())  # Exibe as primeiras linhas do DataFrame

except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

# Substitua 'SUA_CHAVE_DE_API' pela sua chave de API do Gemini
genai.configure(api_key="AIzaSyCsJmOGr4njLyx3W3lAooTI1uowHte1roA")

# Carrega o modelo Gemini Pro
model = genai.GenerativeModel('gemini-1.5-flash-8b')

def carregar_dados(nome_arquivo):
    """Carrega os dados de um arquivo .xlsx em um DataFrame do pandas."""
    try:
        df = pd.read_excel(nome_arquivo)
        return df
    except FileNotFoundError:
        return None

def analisar_dados(df):
    """Realiza análises básicas nos dados de compra."""
    if df is None:
        return "Arquivo não encontrado."

    produtos_vendidos = df['Produto'].value_counts()
    precos_quantidades = df.groupby('Produto')[['Preço', 'Quantidade']].sum()
    sites = df['Site'].unique()
    paises = df['País'].value_counts(normalize=True) * 100

    return {
        "produtos_vendidos": produtos_vendidos,
        "precos_quantidades": precos_quantidades,
        "sites": sites,
        "paises": paises
    }

def remover_compra(df, indice):
    """Remove uma compra do DataFrame com base no índice."""
    if df is None:
        return "Arquivo não encontrado."
    try:
        df.drop(indice, inplace=True)
        return "Compra removida com sucesso."
    except KeyError:
        return "Índice inválido."

def adicionar_compra(df, nova_compra):
    """Adiciona uma nova compra ao DataFrame."""
    if df is None:
        return "Arquivo não encontrado."
    try:
        df.loc[len(df)] = nova_compra
        return "Compra adicionada com sucesso."
    except Exception as e:
        return f"Erro ao adicionar compra: {e}"

def editar_compra(df, indice, nova_compra):
    """Edita uma compra existente no DataFrame."""
    if df is None:
        return "Arquivo não encontrado."
    try:
        df.loc[indice] = nova_compra
        return "Compra editada com sucesso."
    except KeyError:
        return "Índice inválido."
    
def interagir_com_usuario(df):
    """Interage com o usuário, processa a entrada e utiliza a API do Gemini."""
    while True:
        pergunta = input("Usuário: ")
        if pergunta.lower() == "sair":
            break

        # Utiliza a API do Gemini para gerar uma resposta
        resposta_gemini = model.generate_content(pergunta)
        resposta = resposta_gemini.text

        # Lógica para processar a pergunta e manipular os dados
        if "remover compra" in pergunta.lower():
            try:
                indice = int(input("Índice da compra a remover: "))
                resposta = remover_compra(df, indice)
            except ValueError:
                resposta = "Índice inválido."
        elif "adicionar compra" in pergunta.lower():
            nova_compra = input("Dados da nova compra (separados por vírgula): ").split(",")
            resposta = adicionar_compra(df, nova_compra)
        elif "editar compra" in pergunta.lower():
            try:
                indice = int(input("Índice da compra a editar: "))
                nova_compra = input("Novos dados da compra (separados por vírgula): ").split(",")
                resposta = editar_compra(df, indice, nova_compra)
            except ValueError:
                resposta = "Índice inválido."
        elif "país que mais vendeu" in pergunta.lower():
            analise = analisar_dados(df)
            pais_mais_vendeu = analise["paises"].idxmax()
            porcentagem = analise["paises"].max()
            resposta = f"O país que mais vendeu foi {pais_mais_vendeu} com {porcentagem:.2f}%."
        # Adicione mais lógica para outras perguntas e análises

        print("IA:", resposta)

if __name__ == "__main__":
    nome_arquivo = "Meganium_Sales_data.xlsx"  # Substitua pelo nome do seu arquivo
    df = carregar_dados(nome_arquivo)
    interagir_com_usuario(df)