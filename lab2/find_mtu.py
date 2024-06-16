import subprocess
import argparse
import platform


HEADER_SIZE = 28
MIN_MTU = 0
MAX_MTU = 10000


def check_availability(hostname: str) -> bool:
    if platform.system().lower() == 'windows':
        command = ["ping", "-n", "5", hostname]
    else:
        command = ["ping", "-c", "5", hostname]

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        return False


def ping_with_packet_size(hostname: str, packet_size: int) -> bool:
    if platform.system().lower() == "windows":
        command = ["ping", hostname, "-f", "-l", str(packet_size)]
    else:
        command = ["ping", hostname, "-c", "1", "-s", str(packet_size)]

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        return False


def find_min_mtu(hostname: str) -> int:
    low = MIN_MTU
    high = MAX_MTU - HEADER_SIZE

    while low + 1 < high:
        mid = (low + high) // 2
        if ping_with_packet_size(hostname, mid):
            low = mid
        else:
            high = mid

    return low


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True, help="hostname")
    args = parser.parse_args()

    hostname = args.host
    if not check_availability(hostname):
        print(f"Host with name {hostname} is not available :(")
        exit(1)

    print("Start finding of minimum MTU...")
    mtu = find_min_mtu(hostname)
    mtu += HEADER_SIZE
    print(f"Minimum MTU = {mtu}")
