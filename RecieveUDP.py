import socket

def udp_listener(port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", port))
    print(f"Listening for UDP packets on port {port}")

    while True:
        data, addr = udp_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received packet from {addr}: {data}")

udp_listener(12345)  # Replace with the port you want to listen on
