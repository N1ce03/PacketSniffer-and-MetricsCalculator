from scapy.all import sendp, Ether, IP, UDP, Raw

def send_udp_packets_scapy(target_ip, target_port, packet_count):
    for i in range(packet_count):
        # Create Ethernet-level packet
        packet = Ether()/IP(dst=target_ip)/UDP(dport=target_port)/Raw(load="Test UDP Packet")
        sendp(packet, verbose=0)  # Send packet at Layer 2
        print(f"Sent packet {i+1} to {target_ip}:{target_port}")

# Replace "192.168.x.x" with your actual machine IP
send_udp_packets_scapy("192.168.1.100", 12345, 100)
