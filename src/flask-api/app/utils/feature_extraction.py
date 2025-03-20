"""
Utility functions for extracting network traffic features.
"""
import numpy as np
from datetime import datetime
from config import Config

def calculate_time_diff(time_list):
    """
    Calculate inter-arrival times between consecutive timestamps.

    Args:
        time_list: List of timestamps (datetime objects)

    Returns:
        List of inter-arrival times in microseconds
    """
    if len(time_list) <= 1:
        return []

    time_list.sort()  # Ensure timestamps are sorted
    time_diffs = []

    for i in range(1, len(time_list)):
        diff = (time_list[i] - time_list[i-1]).total_seconds() * 1000000  # Convert to microseconds
        time_diffs.append(diff)

    return time_diffs

def calculate_idle_times(time_list, threshold=Config.IDLE_THRESHOLD):
    """
    Calculate idle times in a flow based on a threshold.

    Args:
        time_list: List of timestamps (datetime objects)
        threshold: Time in microseconds to consider as idle

    Returns:
        List of idle times in microseconds
    """
    time_diffs = calculate_time_diff(time_list)
    idle_times = [diff for diff in time_diffs if diff > threshold]
    return idle_times

def extract_fwd_iat_std(forward_packet_times):
    """
    Calculate standard deviation of inter-arrival times in forward direction.

    Args:
        forward_packet_times: List of timestamps for forward packets

    Returns:
        Standard deviation of forward IATs (0 if insufficient packets)
    """
    fwd_iats = calculate_time_diff(forward_packet_times)
    if len(fwd_iats) < 2:  # Need at least 2 values for std
        return 0.0
    return float(np.std(fwd_iats))

def extract_bwd_iat_std(backward_packet_times):
    """
    Calculate standard deviation of inter-arrival times in backward direction.

    Args:
        backward_packet_times: List of timestamps for backward packets

    Returns:
        Standard deviation of backward IATs (0 if insufficient packets)
    """
    bwd_iats = calculate_time_diff(backward_packet_times)
    if len(bwd_iats) < 2:  # Need at least 2 values for std
        return 0.0
    return float(np.std(bwd_iats))

def extract_flow_iat_std(all_packet_times):
    """
    Calculate standard deviation of inter-arrival times for all packets.

    Args:
        all_packet_times: List of timestamps for all packets

    Returns:
        Standard deviation of flow IATs (0 if insufficient packets)
    """
    flow_iats = calculate_time_diff(all_packet_times)
    if len(flow_iats) < 2:  # Need at least 2 values for std
        return 0.0
    return float(np.std(flow_iats))

def extract_fwd_iat_max(forward_packet_times):
    """
    Calculate maximum inter-arrival time in forward direction.

    Args:
        forward_packet_times: List of timestamps for forward packets

    Returns:
        Maximum forward IAT (0 if insufficient packets)
    """
    fwd_iats = calculate_time_diff(forward_packet_times)
    if not fwd_iats:
        return 0.0
    return float(max(fwd_iats))

def extract_flow_iat_mean(all_packet_times):
    """
    Calculate mean inter-arrival time for all packets.

    Args:
        all_packet_times: List of timestamps for all packets

    Returns:
        Mean flow IAT (0 if insufficient packets)
    """
    flow_iats = calculate_time_diff(all_packet_times)
    if not flow_iats:
        return 0.0
    return float(np.mean(flow_iats))

def extract_flow_iat_max(all_packet_times):
    """
    Calculate maximum inter-arrival time for all packets.

    Args:
        all_packet_times: List of timestamps for all packets

    Returns:
        Maximum flow IAT (0 if insufficient packets)
    """
    flow_iats = calculate_time_diff(all_packet_times)
    if not flow_iats:
        return 0.0
    return float(max(flow_iats))

def extract_fwd_iat_mean(forward_packet_times):
    """
    Calculate mean inter-arrival time in forward direction.

    Args:
        forward_packet_times: List of timestamps for forward packets

    Returns:
        Mean forward IAT (0 if insufficient packets)
    """
    fwd_iats = calculate_time_diff(forward_packet_times)
    if not fwd_iats:
        return 0.0
    return float(np.mean(fwd_iats))

def extract_fwd_iat_total(forward_packet_times):
    """
    Calculate sum of inter-arrival times in forward direction.

    Args:
        forward_packet_times: List of timestamps for forward packets

    Returns:
        Total sum of forward IATs (0 if insufficient packets)
    """
    fwd_iats = calculate_time_diff(forward_packet_times)
    if not fwd_iats:
        return 0.0
    return float(np.sum(fwd_iats))

def extract_flow_duration(all_packet_times):
    """
    Calculate total duration of the flow.

    Args:
        all_packet_times: List of timestamps for all packets

    Returns:
        Duration in microseconds (0 if insufficient packets)
    """
    if len(all_packet_times) < 2:
        return 0.0
    return float((max(all_packet_times) - min(all_packet_times)).total_seconds() * 1000000)

def extract_bwd_iat_max(backward_packet_times):
    """
    Calculate maximum inter-arrival time in backward direction.

    Args:
        backward_packet_times: List of timestamps for backward packets

    Returns:
        Maximum backward IAT (0 if insufficient packets)
    """
    bwd_iats = calculate_time_diff(backward_packet_times)
    if not bwd_iats:
        return 0.0
    return float(max(bwd_iats))

def extract_idle_max(all_packet_times, threshold=Config.IDLE_THRESHOLD):
    """
    Calculate maximum idle time.

    Args:
        all_packet_times: List of timestamps for all packets
        threshold: Time in microseconds to consider as idle

    Returns:
        Maximum idle time (0 if no idle periods)
    """
    idle_times = calculate_idle_times(all_packet_times, threshold)
    if not idle_times:
        return 0.0
    return float(max(idle_times))

def extract_idle_mean(all_packet_times, threshold=Config.IDLE_THRESHOLD):
    """
    Calculate mean idle time.

    Args:
        all_packet_times: List of timestamps for all packets
        threshold: Time in microseconds to consider as idle

    Returns:
        Mean idle time (0 if no idle periods)
    """
    idle_times = calculate_idle_times(all_packet_times, threshold)
    if not idle_times:
        return 0.0
    return float(np.mean(idle_times))

def parse_packet_data(packet_data):
    """
    Parse packet data and extract timestamps for forward and backward flows.

    Args:
        packet_data: JSON data containing packet information

    Returns:
        Tuple of (forward_packet_times, backward_packet_times, all_packet_times)
    """
    if not packet_data or len(packet_data) == 0:
        return [], [], []

    forward_packet_times = []
    backward_packet_times = []
    all_packet_times = []

    # First packet's source IP/port is considered the initiator
    first_src_ip = packet_data[0]['src_ip']
    first_src_port = packet_data[0]['src_port']

    for packet in packet_data:
        try:
            timestamp = datetime.fromisoformat(packet['timestamp'])
            all_packet_times.append(timestamp)

            # Determine direction based on the first packet's src_ip and src_port
            if packet['src_ip'] == first_src_ip and packet['src_port'] == first_src_port:
                forward_packet_times.append(timestamp)
            else:
                backward_packet_times.append(timestamp)

        except (KeyError, ValueError) as e:
            print(f"Error processing packet: {e}")
            continue

    return forward_packet_times, backward_packet_times, all_packet_times

def extract_all_features(packet_data):
    """
    Extract all 12 features from packet data.

    Args:
        packet_data: JSON data containing packet information

    Returns:
        Dictionary of extracted features
    """
    forward_times, backward_times, all_times = parse_packet_data(packet_data)

    features = {
        'Fwd IAT Std': extract_fwd_iat_std(forward_times),
        'Bwd IAT Std': extract_bwd_iat_std(backward_times),
        'Flow IAT Std': extract_flow_iat_std(all_times),
        'Fwd IAT Max': extract_fwd_iat_max(forward_times),
        'Flow IAT Mean': extract_flow_iat_mean(all_times),
        'Flow IAT Max': extract_flow_iat_max(all_times),
        'Fwd IAT Mean': extract_fwd_iat_mean(forward_times),
        'Fwd IAT Total': extract_fwd_iat_total(forward_times),
        'Flow Duration': extract_flow_duration(all_times),
        'Bwd IAT Max': extract_bwd_iat_max(backward_times),
        'Idle Max': extract_idle_max(all_times),
        'Idle Mean': extract_idle_mean(all_times)
    }

    return features