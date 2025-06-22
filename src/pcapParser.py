#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Derek Wiseman
"""


from scapy.all import PcapReader, IP
from scapy.error import Scapy_Exception
from connection import Connection
from endpoint import Endpoint
import logging

# exception for file doesnt exist or IsADirectoryError
# add Logging

"""Class to Parse pcap files along with the data needed for plotting"""
class PcapParser():
    """
    Constructor for PcapParser
    @param filename the pcap file to parse. Error checking not done until acessed.
    """
    def __init__(self, filename):
        self._filename = filename

    """
    Parse Useful information from the packet capture and create connection objects
    @return a set of Endpoints 
    """
    def parse(self):
        # Use a dictionary to map destination IPs to Endpoint objects.
        endpoints = {}
        try:
            for packet in PcapReader(self._filename):
                try:
                    if IP not in packet:
                        continue

                    # Parse relevant data from the packet
                    src_ip = packet[IP].src
                    dest_ip = packet[IP].dst

                    # Get or create the destination endpoint
                    endpoint = endpoints.get(dest_ip)
                    if not endpoint:
                        endpoint = Endpoint(dest_ip)
                        endpoints[dest_ip] = endpoint

                    # Add the connection to the endpoint.
                    # Internal set will handle duplicates automatically.
                    conn = Connection(src_ip, dest_ip)
                    endpoint.add_connection(conn)

                except Exception:
                    logging.exception("An unexpected error occurred while parsing a packet:")
                    packet.show()
                    #traceback.print_exc()

        # Handle Exceptions from opening and reading the file
        except (FileNotFoundError, IsADirectoryError, Scapy_Exception) as e:
            # Re-raise file-related or Scapy errors
            logging.error(f"Failed to read pcap file '{self._filename}': {e}")
            raise

        # Return a set of the unique Endpoint objects.
        return set(endpoints.values())


if __name__ == '__main__':
    parser = PcapParser('./cap2.pcap')
    x = parser.parse()
    
