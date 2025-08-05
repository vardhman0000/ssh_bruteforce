# SSH Bruteforce Tool

This project is a multithreaded SSH brute-force script written in Python. It attempts to find valid SSH credentials by trying combinations of usernames and passwords from provided wordlists.

## Features

- Multithreaded for faster brute-forcing
- Stops automatically when valid credentials are found
- Progress and results printed to the console
- Easy to use with customizable wordlists

## Requirements

- Python 3.x
- `paramiko` library  
  Install with:  
  ```
  pip install paramiko
  ```

## Usage

1. Prepare your wordlists:
   - `usernames.txt` — list of usernames (one per line)
   - `passwords.txt` — list of passwords (one per line)

2. Run the script:
   ```
   python3 sshBruteForce.py <target_ip>
   ```

   Example:
   ```
   python3 sshBruteForce.py 192.168.1.100
   ```

## Files

- `sshBruteForce.py` — main brute-force script
- `usernames.txt` — username wordlist (ignored by git)
- `passwords.txt` — password wordlist (ignored by git)

## Disclaimer

This tool is for educational and authorized penetration testing purposes only. Do not use it against systems without explicit permission.