import csv
import random
import string

# File names
lookup_table_file = 'lookup_table.csv'
output_file = 'flow_logs.txt'

# Read lookup_table.csv to get values for the 6th and 7th column
lookup_table = []
with open(lookup_table_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if present
    for row in reader:
        lookup_table.append(row[0:2])  # We only need the first two columns

# Function to generate eni-xxxxxxxx with random small letters and numbers
def generate_eni():
    return 'eni-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# Function to generate random IP address
def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

# Open file for writing the output
with open(output_file, mode='w') as file:
    for i in range(len(lookup_table)):
        # Constant values
        first_value = 2
        second_value = '123456789012'
        fourteenth_value = 'OK'
        
        # Changing values
        third_value = generate_eni()
        fourth_value = generate_ip()  # Source IP
        fifth_value = generate_ip()   # Destination IP
        sixth_value = lookup_table[i][0]  # Reading from CSV 1st column
        seventh_value = lookup_table[i][1]  # Reading from CSV 2nd column
        eighth_value = random.choice([1, 6, 17])
        ninth_value = random.randint(1, 25)
        tenth_value = random.randint(1, 25) * 1000
        eleventh_value = random.randint(1620140661, 1620140761)
        twelfth_value = random.randint(1620140721, 1620140821)
        thirteenth_value = random.choice(['ACCEPT', 'REJECT'])
        
        # Write formatted line to file
        file.write(f"{first_value}, {second_value},{third_value}, {fourth_value}, {fifth_value}, {sixth_value}, {seventh_value}, {eighth_value}, {ninth_value}, {tenth_value}, {eleventh_value}, {twelfth_value}, {thirteenth_value}, {fourteenth_value}\n")

print(f"Text file '{output_file}' generated successfully.")
