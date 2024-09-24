import csv
import random

# Number of rows to generate
num_rows = 10000

# File name for the CSV
file_name = 'lookup_table.csv'

# Generate unique dstport values ranging from 0 to 65535
dstport_values = random.sample(range(65535), num_rows)

# List of protocols
protocols = ['tcp', 'udp', 'icmp']

# Function to generate random tag values like 'dc_tx' where x is between 001 to 999
def generate_tag():
    return f'dc_t{random.randint(1, 999):03}'

# Writing to CSV
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing header
    writer.writerow(['dstport', 'protocol', 'tag'])
    
    # Writing the rows
    for dstport in dstport_values:
        protocol = random.choice(protocols)
        tag = generate_tag()
        writer.writerow([dstport, protocol, tag])

print(f"CSV file '{file_name}' generated successfully.")
