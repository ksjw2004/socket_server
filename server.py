import socket
import sys


def run_server(host="0.0.0.0", port=7777):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow immediate reuse of the port after stopping the server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind the socket to the port
        server_socket.bind((host, port))
        # Listen for incoming connections (allow up to 5 queued connections)
        server_socket.listen(5)
        print("=" * 60)
        print(" Socket Server started successfully!")
        print(f" Listening on: {host}:{port}")
        print(" Waiting for a connection from the host computer...")
        print("=" * 60)

        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            print(
                f"\n[+] Connection established from: {client_address[0]}:{client_address[1]}"
            )

            try:
                # Receive the data in small chunks and retransmit it
                data = client_socket.recv(1024)
                if data:
                    message = data.decode("utf-8")
                    print(f"[*] Received message: '{message}'")

                    # Respond back to the client
                    response = f"Hello Host! Connection to VM is successful. Received: '{message}'"
                    client_socket.sendall(response.encode("utf-8"))
                    print(f"[->] Sent response: '{response}'")
                else:
                    print("[-] No data received from client.")

            except Exception as e:
                print(f"[!] Error handling connection: {e}")
            finally:
                # Clean up the connection
                client_socket.close()
                print("[*] Connection closed. Waiting for new connection...")

    except KeyboardInterrupt:
        print("\n[!] Server is shutting down (KeyboardInterrupt)...")
    except Exception as e:
        print(f"[!] Server error: {e}")
    finally:
        server_socket.close()
        print("[*] Server socket closed. Goodbye!")


if __name__ == "__main__":
    # You can specify a custom port as a command line argument
    port = 7777
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 7777.")

    run_server(port=port)
