#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Derek Wiseman
"""


import argparse
import logging
import sys
from simpleGui import GUI
from interactiveMap import InteractiveMap
from pcapParser import PcapParser
from scapy.error import Scapy_Exception



if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(prog='netmap',
                                     description='Network Data Visualizer')
    parser.add_argument('filename', type=str,
                         help='pcap file for %(prog)s')
    args = parser.parse_args()

    gui = GUI()
    geo_map = InteractiveMap()

    pcap_parser = PcapParser(args.filename)
    try:
        endpoints = pcap_parser.parse()
        if not endpoints:
            logging.info("No valid IP endpoints found in the pcap file. Exiting.")
            sys.exit(0)
    except (FileNotFoundError, IsADirectoryError, Scapy_Exception) as ex:
        logging.critical(f"Could not parse pcap file: {ex}")
        sys.exit(1)

    geo_map.plot_markers(endpoints)
    gui.display_map(geo_map.get_map())
