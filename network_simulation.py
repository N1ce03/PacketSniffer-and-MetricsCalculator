from scapy.all import IP, ICMP, send
import time

def generate_traffic(destination_ip, packet_count=100, interval=0.1):
    print(f"Sending {packet_count} ICMP packets to {destination_ip} using IPv4...")
    for i in range(packet_count):
        packet = IP(dst=destination_ip)/ICMP()  # Ensure we're using IP() for IPv4
        send(packet, verbose=1)  # Set verbose to see each packet sent
        time.sleep(interval)

if __name__ == "__main__":
    destination_ip = "8.8.8.8"  # Replace with any IPv4-compatible IP address
    generate_traffic(destination_ip, packet_count=100, interval=0.1)
