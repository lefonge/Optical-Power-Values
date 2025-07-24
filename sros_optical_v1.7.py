import re
import csv

def parse_nokia_output(file_path):
    data = []
    vendor = "Nokia"
    hostname = "Unknown"
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    port = None
    lanes_section = False
    
    for i, line in enumerate(lines):
        # Identify hostname using System Name instead of Hostname
        match_hostname = re.search(r'System Name\s+:\s+(\S+)', line)
        if match_hostname:
            hostname = match_hostname.group(1)
        
        # Identify port/interface
        match_port = re.search(r'Interface\s+:\s+(\S+)', line)
        if match_port:
            port = match_port.group(1)
        
        # Identify start of lane section
        if "Lane ID" in line:
            lanes_section = True
            continue
        
        # Parse lane power values with proper indexing and error handling
        if lanes_section and re.match(r'\s*\d+', line):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    lane_id = parts[0]
                    tx_power = parts[-2]  # Second last column
                    rx_power = parts[-1]  # Last column
                    
                    # Ensure the extracted values are valid numbers
                    if re.match(r'[-\d\.]+', tx_power) and re.match(r'[-\d\.]+', rx_power):
                        data.append([vendor, hostname, f"{port}/Lane{lane_id}", tx_power, rx_power])
                    else:
                        print(f"Skipping invalid power values in line: {line.strip()}")
                except IndexError:
                    print(f"Skipping malformed line: {line.strip()}")
        
        # Identify port power values if no lanes are specified
        if "Tx Output Power (dBm)" in line:
            try:
                tx_match = re.search(r'Tx Output Power \(dBm\)\s+([-\d\.]+)', line)
                rx_match = re.search(r'Rx Optical Power \(avg dBm\)\s+([-\d\.]+)', lines[i+1])
                if tx_match and rx_match:
                    tx_power = tx_match.group(1)
                    rx_power = rx_match.group(1)
                    data.append([vendor, hostname, port, tx_power, rx_power])
            except IndexError:
                print(f"Skipping malformed power entry at line {i}")
    
    return data

def save_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Vendor", "Hostname", "Port", "Tx Power (dBm)", "Rx Power (dBm)"])
        writer.writerows(data)

if __name__ == "__main__":
    input_file = "nokia_output.txt"
    output_file = "nokia_optical_power.csv"
    parsed_data = parse_nokia_output(input_file)
    save_to_csv(parsed_data, output_file)
    print(f"Parsed data saved to {output_file}")
