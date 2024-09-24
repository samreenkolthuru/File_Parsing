import csv
from collections import defaultdict

# Here, we will create a function to load the lookup table from a CSV file
# and we will use the default dictionary to store the tags and port or protocol pairs
def lookuptable_loader(filename):
    lookup_table = defaultdict(list)  


    def file_processor(file_obj, delimiter=','):
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        
        required_headers = {'dstport', 'protocol'}
        headers = set(header.strip().lower() for header in reader.fieldnames)
        if not required_headers.issubset(headers):
            missing = required_headers - headers
            raise ValueError(f"Lookup table is missing required headers: {', '.join(missing)}")
        
        reader.fieldnames = [header.strip().lower() for header in reader.fieldnames]

        for row_number, row in enumerate(reader, start=2):  
            row = {key.strip().lower(): value.strip().lower() for key, value in row.items()}
            port = row.get('dstport')
            protocol = row.get('protocol')
            tag = row.get('tag', 'untagged')

            if not port or not protocol:
                print(f"Warning: Missing 'dstport' or 'protocol' in lookup table at line {row_number}. Skipping entry.")
                continue

            lookup_table[tag].append((port, protocol))

    try:
        with open(filename, 'r', encoding='utf-8') as file_obj:
            file_processor(file_obj)
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as file_obj:
            file_processor(file_obj)
    except FileNotFoundError:
        raise FileNotFoundError(f"The lookup file '{filename}' was not found.")

    return lookup_table


# Here, we will create a function to parse the flow logs and apply tags based on the lookup table
# and we will map the protocol numbers to protocol names
def log_flow_parse(flow_log_filename, lookup_table):
    count_tag = defaultdict(int)
    count_untag = 0
    count_port_protocol = defaultdict(int)

    map_protocol = {
        '6': 'tcp',    # TCP
        '17': 'udp',   # UDP
        '1': 'icmp'    # ICMP
    }

    try:
        with open(flow_log_filename, 'r') as file_obj:
            for line_number, line in enumerate(file_obj, start=1):
                parts = line.strip().split(',')
                if len(parts) < 8:
                    print(f"Warning: Incomplete line at {line_number} in flow logs. Skipping line.")
                    continue  

                try:
                    dst_port = parts[5].strip().lower()
                    protocol_number = parts[7].strip()
                except IndexError:
                    print(f"Warning: Unexpected format at line {line_number} in flow logs. Skipping line.")
                    continue

                protocol = map_protocol.get(protocol_number, 'other')

                if not dst_port or not protocol_number:
                    print(f"Warning: Missing 'dstport' or 'protocol' at line {line_number} in flow logs. Skipping line.")
                    continue

                successful_match = False

                for tag, port_protocol_list in lookup_table.items():
                    if (dst_port, protocol) in port_protocol_list:
                        count_tag[tag] += 1
                        count_port_protocol[(dst_port, protocol)] += 1
                        successful_match = True
                        break

                if not successful_match:
                    count_untag += 1
                    count_port_protocol[(dst_port, protocol)] += 1
    except FileNotFoundError:
        raise FileNotFoundError(f"The flow log file '{flow_log_filename}' was not found.")

    return count_tag, count_untag, count_port_protocol


# Here, we will write the function to write the results to an output CSV file
# In that we will include the number of tags and untags
#Additionally, we will also include the number of port/protocol combinations
def write_output(output_filename, count_tag, count_untag, count_port_protocol):
    try:
        with open(output_filename, 'w', newline='') as file_obj:
            writer = csv.writer(file_obj)

            writer.writerow(['Tag', 'Count'])
            for tag, count in count_tag.items():
                writer.writerow([tag, count])

            writer.writerow(['Untagged', count_untag])

            writer.writerow([])

            writer.writerow(['Port', 'Protocol', 'Count'])
            for (port, protocol), count in count_port_protocol.items():
                writer.writerow([port, protocol, count])
    except IOError:
        raise IOError(f"An error occurred while writing to the output file '{output_filename}'.")


# This is the Main function
def main():
    flow_log_file = 'flow_logs.txt'
    lookup_file = 'lookup_table.csv'
    output_file = 'output_file.csv'

    try:
        lookup_table = lookuptable_loader(lookup_file)
        tag_counts, untagged_count, port_protocol_counts = log_flow_parse(flow_log_file, lookup_table)
        write_output(output_file, tag_counts, untagged_count, port_protocol_counts)
        print(f"Processing complete. Results have been written to '{output_file}'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

