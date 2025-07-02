import sqlite3
import poemas
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pprint import pprint

try:
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt_tab')
    nltk.download('stopwords')

def executar():
    conexao = sqlite3.connect('poetroid.db')
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT p.id, p.poema, GROUP_CONCAT(pc.palavra, ', ') AS palavras_chave
    FROM poemas p
    LEFT JOIN palavras_chave pc ON p.id = pc.poema_id
    GROUP BY p.id;
    ''')

    resultados = cursor.fetchall()
    for row in resultados:
        print(f"ID: {row[0]}, Poema: {row[1]}, Palavras-Chave: {row[2]}")

    conexao.close() 
    
def inserir_poema_e_palavras(poema, palavras_chave, cursor, conexao):
    # Inserir o poema na tabela `poemas`
    cursor.execute('INSERT INTO poemas (poema) VALUES (?)', (poema,))
    poema_id = cursor.lastrowid  # Recupera o ID do poema recém-inserido
    for palavra in palavras_chave:
        cursor.execute('INSERT INTO palavras_chave (poema_id, palavra) VALUES (?, ?)', (poema_id, palavra))
    conexao.commit()
    
def db():
    conexao = sqlite3.connect('poetroid.db')
    cursor = conexao.cursor()
    for poema in poemas.template:
        inserir_poema_e_palavras(poema[0], poema[1], cursor, conexao)
    conexao.close()
    
def extrair_palavras_chave(descricao):
    stop_words = set(stopwords.words('portuguese'))  # Defina a linguagem desejada
    palavras = word_tokenize(descricao)
    palavras_chave = [palavra for palavra in palavras if palavra.isalpha() and palavra.lower() not in stop_words]
    return palavras_chave
    
def conectar():
    # Conectar ao banco de dados (ou criar um novo arquivo)
    conexao = sqlite3.connect('poetroid.db')
    cursor = conexao.cursor()
    # Criação da tabela para armazenar os poemas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS poemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único para cada poema
        poema TEXT NOT NULL,                   -- Coluna para armazenar o poema
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data e hora de criação do registro
    )
    ''')
    # Criação da tabela para armazenar as palavras-chave
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS palavras_chave (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único para cada palavra-chave
        poema_id INTEGER,                      -- Relaciona a palavra-chave ao poema
        palavra TEXT NOT NULL,                 -- A palavra-chave em si
        FOREIGN KEY (poema_id) REFERENCES poemas(id) -- Chave estrangeira ligando ao poema
    )
    ''')
    conexao.commit()
    conexao.close()
    
    
def encontrar_melhor_resultado(palavras_usuario):
    """
    Busca no banco de dados o poema que melhor corresponde à lista de palavras-chave fornecida.
    
    :param palavras_usuario: Lista de palavras-chave fornecida pelo usuário.
    :return: O poema com a maior correspondência e sua pontuação.
    """
    conexao = sqlite3.connect('poetroid.db')
    cursor = conexao.cursor()
    
    # Formatar os placeholders para a consulta SQL
    placeholders = ', '.join(['?'] * len(palavras_usuario))
    
    # Consulta para encontrar o poema com mais correspondências
    query = f'''
    SELECT 
        p.id,
        p.poema,
        COUNT(pc.palavra) AS pontuacao
    FROM 
        poemas p
    LEFT JOIN 
        palavras_chave pc 
    ON 
        p.id = pc.poema_id
    WHERE 
        pc.palavra IN ({placeholders})
    GROUP BY 
        p.id
    ORDER BY 
        pontuacao DESC
    LIMIT 1;
    '''
    
    # Executar a consulta com as palavras fornecidas
    cursor.execute(query, palavras_usuario)
    resultado = cursor.fetchone()
    
    conexao.close()
    
    # Verificar se houve resultado
    if resultado:
        return {
            "id": resultado[0],
            "poema": resultado[1],
            "pontuacao": resultado[2]
        }
    else:
        resultado = 'Nenhum poema foi encontrado no banco para:'
        for p in palavras_usuario:
            resultado += '\n'+ p
        return {'poema': resultado}

    
    
def verificar(caminho_arquivo):
    return os.path.isfile(caminho_arquivo)

def init ():
    if not verificar('poetroid.db'):
        conectar()
        db()
    executar()
         
init ()
