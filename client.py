import socket
import sys


def run_client(server_ip, port=7777):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout so we don't hang indefinitely if the IP is unreachable
    client_socket.settimeout(5.0)

    print("=" * 60)
    print(" Attempting to connect to VMware VM...")
    print(f" Target Server: {server_ip}:{port}")
    print("=" * 60)

    try:
        # Connect to the server
        client_socket.connect((server_ip, port))
        print(f"[+] Successfully connected to {server_ip}:{port}!")

        # Send data
        message = "Hello from local computer!"
        print(f"[->] Sending message: '{message}'")
        client_socket.sendall(message.encode("utf-8"))

        # Receive response
        data = client_socket.recv(1024)
        print(f"[<-] Received response from VM server:\n    '{data.decode('utf-8')}'")

        print("\n Connection verification completed successfully!")

    except socket.timeout:
        print("\n[!] Connection timed out. Please check:")
        print("  1. Is the server script running on the VM?")
        print("  2. Is the VM IP address correct?")
        print(
            "  3. Check VMware network settings (NAT/Bridged) and firewalls on both sides."
        )
    except ConnectionRefusedError:
        print(
            "\n[!] Connection refused. The VM is reachable, but the server script is not running or listening on this port."
        )
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
    finally:
        client_socket.close()
        print("[*] Connection closed.")


if __name__ == "__main__":
    # Get the server IP from command line argument, or prompt the user
    if len(sys.argv) > 1:
        server_ip = sys.argv[1]
    else:
        print("Enter the IP address of your VMware virtual machine:")
        server_ip = input("VM IP Address: ").strip()

    if not server_ip:
        print("Error: IP address cannot be empty.")
        sys.exit(1)

    port = 7777
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number. Using default port 7777.")

    run_client(server_ip, port)
