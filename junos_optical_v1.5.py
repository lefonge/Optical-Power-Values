import re
import csv
from collections import defaultdict

# Input and output file paths
input_filename = "juniper_output.txt"  # Replace with actual path if needed
output_filename = "juniper_optical_power.csv"  # Updated CSV file name

# Patterns to match different cases
patterns = {
    "tx_power": re.compile(r"Laser output power\s+:\s+\S+\s+mW\s+/\s+(-?\d+\.\d+|\d+) dBm"),
    "rx_power_avg": re.compile(r"Receiver signal average optical power\s+:\s+(-?\d+\.\d+|\d+)"),  # Includes 0.0000
    "rx_power_laser": re.compile(r"Laser rx power\s+:\s+\S+\s+mW\s+/\s+(-?\d+\.\d+|\d+) dBm"),
    "rx_power_lane": re.compile(r"Laser receiver power\s+:\s+\S+\s+mW\s+/\s+(-?\d+\.\d+|\d+) dBm"),
    "interface": re.compile(r"Physical interface:\s+(\S+)"),
    "lane": re.compile(r"Lane (\d+)"),
}

# Dictionary to store parsed data
data = defaultdict(lambda: {"Vendor": "Juniper", "Tx Power (dBm)": None, "Rx Power (dBm)": None})
current_interface = None
current_lane = None

# Read and parse the file
with open(input_filename, "r") as file:
    for line in file:
        line = line.strip()

        # Check for interface
        match = patterns["interface"].match(line)
        if match:
            current_interface = match.group(1)
            current_lane = None  # Reset lane tracking
            continue

        # Check for lanes
        match = patterns["lane"].match(line)
        if match:
            current_lane = match.group(1)
            continue

        # Determine the port name (Interface or Interface + Lane)
        port_name = f"{current_interface}-lane{current_lane}" if current_lane is not None else current_interface

        # Check for Tx Power (General and Lane cases)
        match = patterns["tx_power"].search(line)
        if match:
            data[port_name]["Tx Power (dBm)"] = match.group(1)

        # Check for Rx Power (Average Optical Power case, including 0.0000)
        match = patterns["rx_power_avg"].search(line)
        if match:
            data[port_name]["Rx Power (dBm)"] = match.group(1)

        # Check for Rx Power (Laser Rx Power case)
        match = patterns["rx_power_laser"].search(line)
        if match:
            data[port_name]["Rx Power (dBm)"] = match.group(1)

        # Check for Rx Power (Lane case)
        match = patterns["rx_power_lane"].search(line)
        if match:
            data[port_name]["Rx Power (dBm)"] = match.group(1)

# Convert the dictionary to a list of rows, filtering out empty lane entries
csv_data = [["Vendor", "Port", "Tx Power (dBm)", "Rx Power (dBm)"]]
for port, values in data.items():
    tx_power = values["Tx Power (dBm)"]
    rx_power = values["Rx Power (dBm)"]

    # Ensure at least one power value exists before adding to output
    if tx_power is not None or rx_power is not None:
        csv_data.append([values["Vendor"], port, tx_power if tx_power else "", rx_power if rx_power else ""])

# Write the extracted data to a CSV file
with open(output_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)

print(f"Data successfully written to {output_filename}")
