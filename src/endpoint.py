#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Derek Wiseman
"""

import requests
import logging
from threading import Lock


HOSTNAME_KEY = "hostname"
LATLON_KEY = "loc"
ORG_KEY = "org"

LAT_INDEX = 0
LON_INDEX = 1

location_service = True
location_lock = Lock()


class Endpoint:
    def __init__(self, ip):
        self.__ip = ip
        self.__lat = '' # Not using artihmatic. Use str for better precision
        self.__lon = '' # Not using artihmatic. Use str for better precision
        self.__hostname = ''
        self.__org = ''
        self.__connections = set()

    def __eq__(self, right):
        return self.__ip == right.__ip
    
    def __key(self):
        return self.__ip
    
    def __hash__(self):
        return hash(self.__key())
    
    """Return the destination IP for the endpoint"""
    def get_ip(self):
        return self.__ip
    
    """The latitude for the endpoint. Default is 0"""
    def get_lat(self):
        return self.__lat
    
    """The longitude for the endpoint. Default is 0"""
    def get_lon(self):
        return self.__lon
    
    """
    Return a tuple containing lat, lon. For access the LAT_INDEX and LON_INDEX
    constants can be used.
    """
    def get_location(self):
        return self.__lat, self.__lon
    
    """Return the hostname correlated to the IP. Default is '' """
    def get_hostname(self):
        return self.__hostname
    
    """Return the organization name correlated to the IP. Default is '' """
    def get_org(self):
        return self.__org

    """
    Use https://ipinfo.io/ API to populate location, hostname, and
    organizational data. Also populates connection data. Checks on 
    private IPs not accounted for. 
    """    
    def get_data_by_ip(self):
        global location_service
        # Atomically check if the location service is enabled.
        # The 'with' statement ensures the lock is always released.
        with location_lock:
            if not location_service:
                # API limit was reached.
                return

        url = f"https://ipinfo.io/{self.__ip}/json"
        try:
            # Use a timeout to prevent threads from hanging indefinitely.
            response = requests.get(url, timeout=10)
            # Raise HTTPError for 4xx or 5xx responses
            response.raise_for_status()
            result = response.json()

        except requests.exceptions.HTTPError as ex:
            # Specifically check for the 429 "Too Many Requests" status code.
            if ex.response.status_code == 429:
                logging.warning("API Limit Exceeded. Disabling further lookups.")
                # Disable the loockup service.
                with location_lock:
                    location_service = False
            else:
                logging.error(f"HTTP Error for {self.__ip}: {ex}")
            return  # Stop processing 
        except requests.exceptions.RequestException as e:
            # Handle other network errors like timeouts or connection issues.
            logging.error(f"Request failed for {self.__ip}: {e}")
            return  # Stop processing

        # Parse the data.
        try:
            location_str = result.get(LATLON_KEY)
            if location_str:
                location = location_str.split(',')
                self.__lat = location[LAT_INDEX]
                self.__lon = location[LON_INDEX]
        except IndexError:
            logging.warning(f"Could not parse location data for {self.__ip}")

        self.__hostname = result.get(HOSTNAME_KEY, "Not Available")
        self.__org = result.get(ORG_KEY, "Not Available")

    """
    Check if value already exists in __connections
    @param value a connection to compare against existing objects in 
    __connections 
    """
    def contains(self, value):
        return value in self.__connections
        
    """
    Add connection to the __connection collection
    @param connection the connection oject to add to __connections
    """
    def add_connection(self, connection):
        self.__connections.add(connection)

if __name__ == '__main__':
    a = Endpoint('8.8.8.8')
    a.get_data_by_ip()
    
