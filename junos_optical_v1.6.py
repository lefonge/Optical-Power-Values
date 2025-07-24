import re
import csv

input_file = "juniper_output.txt"
output_file = "juniper_optical_power.csv"

def extract_dbm_value(line):
    match = re.search(r'([-+]?[0-9]*\.?[0-9]+)\s*dBm', line)
    if match:
        return match.group(1)
    return None

with open(input_file, 'r') as file:
    lines = file.readlines()

data = []
hostname = "unknown"
interface = None
lane = None
tx_power = None
rx_power = None

for i, line in enumerate(lines):
    line = line.strip()

    if line.startswith("Hostname:"):
        hostname = line.split(":", 1)[1].strip()

    elif line.startswith("Physical interface:"):
        interface = line.split(":")[1].strip()
        lane = None  # reset lane for new interface
        tx_power = None
        rx_power = None

    elif re.match(r'^Lane \d+', line):
        lane = re.search(r'Lane (\d+)', line).group(1)
        tx_power = None
        rx_power = None

    elif "Laser output power" in line and "dBm" in line:
        value = extract_dbm_value(line)
        if value != "-Inf":
            tx_power = value

    elif "Laser receiver power" in line and "dBm" in line:
        value = extract_dbm_value(line)
        if value != "-Inf":
            rx_power = value

        # If both values are now ready and valid, write the record
        if interface and lane is not None and (tx_power or rx_power):
            port = f"{interface}-lane{lane}"
            data.append(["Juniper", hostname, port, tx_power if tx_power else "", rx_power if rx_power else ""])
            tx_power, rx_power = None, None  # reset after use

# Write to CSV
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Vendor", "Hostname", "Port", "Tx Power (dBm)", "Rx Power (dBm)"])
    for row in data:
        writer.writerow(row)

print(f"Data successfully written to {output_file}")
