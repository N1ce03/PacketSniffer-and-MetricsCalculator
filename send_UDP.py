import socket
import time

def send_udp_packets(target_ip, target_port, packet_count, interval):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b"Test UDP Packet"  # Payload of the packet

    for i in range(packet_count):
        udp_socket.sendto(message, (target_ip, target_port))
        print(f"Sent packet {i+1} to {target_ip}:{target_port}")
        time.sleep(interval)  # Interval between packets

    udp_socket.close()
    print("UDP packets sent successfully.")

# Configuration
TARGET_IP = "127.0.0.1"  # Replace with the target IP
TARGET_PORT = 12345      # Replace with the target port
PACKET_COUNT = 100       # Number of packets to send
INTERVAL = 0.01          # Time interval between packets (in seconds)

send_udp_packets(TARGET_IP, TARGET_PORT, PACKET_COUNT, INTERVAL)
