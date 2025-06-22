#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Derek Wiseman
"""


"""Class to represent a connection made between endpoints"""
class Connection:
    """
    A Constructor for a connection object.
    @param srcIP: a str containing the source IP address
    @param destIP: a str containing the destination IP address
    """
    def __init__(self, src_ip, dest_ip):
        self.__src_ip = src_ip
        self.__dest_ip = dest_ip

    def __key(self):
        return (self.__src_ip, self.__dest_ip)

    def __hash__(self):
        return hash(self.__key())
    
    """
    Check if right is equal to the src_ip
    @param right a string containing an IP address 
    """
    def __contains__(self, right):
        if isinstance(right, str):
            return right == self.__src_ip
        else:
            return False

    def __eq__(self, right):
        return (self.__src_ip == right.__src_ip) and (self.__dest_ip 
                                                      == right.__dest_ip)
    

if __name__ == '__main__':
    a = Connection('192.168.1.3', '8.8.8.8')
    b = Connection('8.8.8.8', '192.168.1.3')
    c = Connection('192.168.1.3', '8.8.8.8')

    d = set()
    d.add(a)
    d.add(b)
    d.add(c)

    for x in d:
        print(x)
