import pyshark
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

TSHARK_PATH = r"C:\Users\Acer\Wireshark\tshark.exe"   # Update if necessary


def capture_udp_packets(interface='Wi-Fi', max_packets=100):
    """
    Captures up to max_packets UDP packets on a specified network interface.
    """
    capture = pyshark.LiveCapture(interface=interface, tshark_path=TSHARK_PATH)
    capture.sniff(packet_count=max_packets)
    print(f"Captured {len(capture)} packets.")

    # Filter UDP packets
    udp_packets = [pkt for pkt in capture if 'UDP' in pkt]
    print(f"Filtered {len(udp_packets)} UDP packets.")

    return udp_packets

def calculate_udp_metrics(packets):
    """
    Calculates latency, jitter, packet loss, throughput, and PDR for UDP packets.
    """
    timestamps = [pkt.sniff_time.timestamp() for pkt in packets]
    packet_sizes = [int(pkt.length) for pkt in packets]

    if len(timestamps) < 2:
        print("Not enough UDP packets for latency/jitter/throughput calculations.")
        return np.array([]), 0, 100.0, 0, 0

    # Latency
    latencies = np.diff(timestamps) * 1000  # Convert to milliseconds

    # Jitter
    jitter = np.std(latencies)

    # Packet Loss
    packet_loss = (1 - len(latencies) / len(packets)) * 100  # Approximate packet loss

    # Throughput
    total_data = sum(packet_sizes)  # Total data in bytes
    total_time = timestamps[-1] - timestamps[0]  # Total time in seconds
    throughput = (total_data * 8) / total_time if total_time > 0 else 0  # Throughput in bits per second (bps)

    # Packet Delivery Ratio (PDR)
    sent_packets = len(packets)  # Assume all packets are sent for simplicity
    delivered_packets = len(packets) - int(packet_loss / 100 * len(packets))  # Approximation
    pdr = (delivered_packets / sent_packets) * 100 if sent_packets > 0 else 0

    return latencies, jitter, packet_loss, throughput, pdr

def plot_udp_metrics(latencies, jitter, packet_loss, throughput, pdr):
    """
    Plots UDP network metrics including latency, jitter, packet loss, throughput, and PDR.
    """
    plt.figure(figsize=(12, 8))

    # Latency Plot
    if len(latencies) > 0:
        plt.subplot(5, 1, 1)
        plt.plot(latencies, label='Latency')
        plt.ylabel('Latency (ms)')
        plt.legend()
    else:
        print("No latency data to plot.")

    # Jitter Plot
    plt.subplot(5, 1, 2)
    plt.plot([jitter] * max(1, len(latencies)), label='Jitter')
    plt.ylabel('Jitter (ms)')
    plt.legend()

    # Packet Loss Plot
    plt.subplot(5, 1, 3)
    plt.plot([packet_loss] * max(1, len(latencies)), label='Packet Loss')
    plt.ylabel('Packet Loss (%)')
    plt.legend()

    # Throughput Plot
    plt.subplot(5, 1, 4)
    plt.plot([throughput] * max(1, len(latencies)), label='Throughput')
    plt.ylabel('Throughput (bps)')
    plt.legend()

    # PDR Plot
    plt.subplot(5, 1, 5)
    plt.plot([pdr] * max(1, len(latencies)), label='PDR')
    plt.ylabel('PDR (%)')
    plt.legend()

    plt.xlabel('Packet Number')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Configuration
    interface = 'Wi-Fi'  # Change to your network interface
    max_packets = 100  # Maximum number of packets to capture

    # Capture UDP Packets
    packets = capture_udp_packets(interface=interface, max_packets=max_packets)

    # Calculate Metrics
    latencies, jitter, packet_loss, throughput, pdr = calculate_udp_metrics(packets)

    # Print Metrics
    print(f"Latency (ms): {latencies}")
    print(f"Jitter (ms): {jitter}")
    print(f"Packet Loss (%): {packet_loss}")
    print(f"Throughput (bps): {throughput}")
    print(f"Packet Delivery Ratio (%): {pdr}")

    # Plot Metrics
    plot_udp_metrics(latencies, jitter, packet_loss, throughput, pdr)
