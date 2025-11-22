import pyshark
import numpy as np
import matplotlib.pyplot as plt
import time

# TShark path
TSHARK_PATH = r"C:\Users\Acer\Wireshark\tshark.exe"

def capture_icmp_packets(interface='Wi-Fi', duration=60, max_packets=100):
    """
    Captures ICMP packets using pyshark for a specified duration or until max_packets is reached.
    """
    capture = pyshark.LiveCapture(interface=interface, tshark_path=TSHARK_PATH)
    capture.sniff(timeout=duration, packet_count=max_packets)
    print(f"Captured {len(capture)} packets")
    return capture

def calculate_latency(packets):
    """
    Calculates the latencies from ICMP packet capture timestamps.
    """
    latencies = []
    for packet in packets:
        if 'ICMP' in packet or 'ICMPv6' in packet:
            time_received = packet.sniff_time.timestamp()
            latencies.append(time_received)
    
    if not latencies:
        print("No ICMP packets found.")
        return np.array([])

    return np.diff(latencies) * 1000  # Convert to milliseconds

def calculate_throughput(packets, duration):
    """
    Calculates throughput (bits per second) based on the captured ICMP packets.
    """
    total_bytes = sum(int(packet.length) for packet in packets if 'ICMP' in packet or 'ICMPv6' in packet)
    return (total_bytes * 8) / duration  # Convert bytes to bits and divide by time in seconds

def calculate_packet_delivery_ratio(sent_packets, received_packets):
    """
    Calculates the Packet Delivery Ratio (PDR).
    """
    return (received_packets / sent_packets) * 100 if sent_packets > 0 else 0

def calculate_jitter(latencies):
    """
    Calculates jitter as the standard deviation of latencies.
    """
    return np.std(latencies) if latencies.size > 0 else 0

def plot_metrics(latencies, jitter, packet_loss, throughput, pdr):
    """
    Plots the calculated metrics: Latency, Jitter, Packet Loss, Throughput, and PDR.
    """
    plt.figure(figsize=(10, 8))

    if latencies.size > 0:
        plt.subplot(4, 1, 1)
        plt.plot(latencies, label='Latency (ms)')
        plt.ylabel('Latency (ms)')
        plt.legend()
    else:
        print("No latency data to plot.")

    plt.subplot(4, 1, 2)
    plt.bar([1], [jitter], label='Jitter (ms)', color='orange')
    plt.ylabel('Jitter (ms)')
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.bar([1], [packet_loss], label='Packet Loss (%)', color='red')
    plt.ylabel('Packet Loss (%)')
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.bar([1, 2], [throughput, pdr], tick_label=['Throughput (bps)', 'PDR (%)'], color=['blue', 'green'])
    plt.ylabel('Throughput / PDR')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sent_packets = 100  # Simulated count of ICMP packets sent
    duration = 60  # Duration of capture in seconds
    max_packets = 100  # Maximum number of packets to capture
    interface = 'Wi-Fi'  # Network interface

    packets = capture_icmp_packets(interface=interface, duration=duration, max_packets=max_packets)
    latencies = calculate_latency(packets)
    jitter = calculate_jitter(latencies)
    throughput = calculate_throughput(packets, duration)
    received_packets = len([packet for packet in packets if 'ICMP' in packet or 'ICMPv6' in packet])
    packet_loss = calculate_packet_delivery_ratio(sent_packets, received_packets)

    print(f"Latency (ms): {latencies}")
    print(f"Jitter (ms): {jitter}")
    print(f"Throughput (bps): {throughput}")
    print(f"Packet Delivery Ratio (%): {packet_loss}")

    plot_metrics(latencies, jitter, 100 - packet_loss, throughput, packet_loss)
