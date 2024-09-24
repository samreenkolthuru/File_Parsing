
Flow Log Tagging and Analysis and the Assumptions:

Using a lookup table from a CSV file, this Python script analyzes flow logs and assigns tags. 
After parsing logs and comparing destination ports and protocols with lookup table tags, the script 
creates a CSV summary report with counts of tagged, untagged, and port/protocol combinations.



Assumptions:
1. Log Format: The application only supports the comma-separated values (CSV) default log format, which has entries 
for the source IP address, destination IP address, source port, destination port, and protocol number. It is not 
supported to use custom log formats.

2. Supported Version: The log format is only compatible with version 2. If the logs are in different versions, 
they must follow version 2 format in order to be processed correctly.

3. File Encoding: By default, UTF-8 encoding is assumed for the lookup table and flow log. The script attempts 
to handle files using latin-1 encoding if UTF-8 fails.

4. Table Headers for Lookup: It is assumed that the lookup_table.csv file contains the following headers: 
protocol, tag, and dstport. An error will be raised by the script if any of these headers are missing.

5. Protocol Mapping: Only the protocol numbers 6, 17, and 1 for TCP, UDP, and ICMP are supported by the script. 
We will classify any additional protocol numbers as other.

6. Port/Protocol Matching: The lookup table's specified dstport and protocol values are the only criteria used for matching. 
The flow log entry is regarded as untagged if the lookup database contains no matching entries.

7. File Paths: Lookup_table.csv, flow_logs.txt, and output_file.csv are assumed to be in the same directory as the script 
by the script. Unless the code is changed, it cannot handle absolute file paths or folders.



What we did in the script:
1. imported a lookup table from a CSV file that has protocol pairings and destination ports in it.
2. Applied tags to flow log files by parsing them using the lookup table.
3. Tracked the number of times tagged and untagged flow entries occur.
4. Linked the names to protocol numbers (TCP, UDP, ICMP).
5. The analysis findings will be written to an output CSV file.



Requirements and Files we need to run the script:
1. Python 3.x
2. csv, collections - libraries. You can install them via -pip install collections
3. lookup_table.csv file consists of all the mappings of dstports (destination ports), protocols, and tags.It has columns named
dstport, protocol, tag.
4. flow_logs.txt file consists of log flows to be processed and they are seperated with commas.
5. output_file.csv consists of tag counts, untagged counts and port/protocol combinations.



Usage:
1. First, we should run lookup_gen.py which creates a lookup_table.csv and then we should run flow_logs_gen.py which creates a 
flow_logs.txt using the previous generated lookup_table.csv and then we should run parse_log_file.py which parses logs and compares 
with lookup table.

1. In order to generate a lookup table for our script, we are going to use a random lookup generator python script in which
the script produces the lookup table with a given number of rows (10,000 by default). It also assigns distinct destination port values
(dstport) at random. The dstport values are distinct and chosen at random from a range of 0 to 65535. This guarantees that the resulting 
CSV contains no duplicate dstport values. Additionally, it chooses a protocol at random from TCP, UDP, and ICMP. dc_tXXX, where 
XXX is a random number between 001 and 999, is the format in which random tag values are generated.

2. Now, In order to generate a flow log text file for our script, we are going to create and use a random flow log generator
python script in which the Python script creates a flow log text file (flow_logs.txt) by reading a lookup table from a CSV file 
(lookup_table.csv) which we created using lookup_gen.py. There are several fields in the flow log; some are generated dynamically, 
while others are taken from the lookup table. A network flow event is represented by each line in the output, which contains 
information about the protocol, ports, IP addresses, and statuses.This lookup_gen.py reads the destination port and protocol 
details from lookup_table.csv in order to create flow logs. ENI (Elastic Network Interface) IDs are generated dynamically. IP addresses
and others are at random.



How the script works:
1. Lookup Table Loading: The script loads destination ports and protocol mappings by reading the lookup_table.csv file 
and saving them in a dictionary with tags as keys.

2. Parsing Flow Logs: The script reads the file flow_logs.txt, compares protocol entries and destination port to the lookup 
table, and counts the number of tagged and untagged entries.

3. Output Report: The following outcomes are written to output_file.csv: counts for every tag, Number of entries without tags, and
Port and protocol combinations seen in the flow logs.



Error Handling:
1. The script records incomplete lines in the flow log and searches the lookup database for any missing necessary headers.
An error with the relevant message is raised if a necessary file cannot be located.

2. The flow log contains warnings for missing destination ports or protocols.




