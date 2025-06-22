#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Derek Wiseman
"""


import folium
from endpoint import Endpoint
from concurrent.futures import ThreadPoolExecutor
import logging

""" Class wrapped around folium """
class InteractiveMap:
    """
    Constructor fcontaining predefined values for the follium. Wrapper to the
    folium.Map() method
    """
    def __init__(self):
        self.__geo_map = folium.Map(width=1024, height=768,
                                     location=[40, -90], zoom_start=3,
                                     tiles=folium.TileLayer(no_wrap=True))

    """Return the folium map object"""
    def get_map(self):
        return self.__geo_map
    
    """Create a marker for each endpoint object in the collection"""
    def plot_markers(self, endpoints):

        # Use a thread pool to populate data for all endpoints concurrently.
        with ThreadPoolExecutor() as pool:
            pool.map(lambda ep: ep.get_data_by_ip(), endpoints)

        plotted_count = 0
        for endpoint in endpoints:
            lat, lon = endpoint.get_location()

            # Skip endpoints where location lookup failed (lat/lon are default 0)
            if not lat or not lon:
                continue
            
            logging.debug(f"Plotting marker for {endpoint.get_ip()} at ({lat}, {lon})")
            html=f"""
            <p>Hostname: {endpoint.get_hostname()}</p>
            <p>Org: {endpoint.get_org()}</p>
            <p>IP: {endpoint.get_ip()}</p>
            """
            iframe = folium.IFrame(html=html, width=200, height=200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=[lat, lon],
                popup=popup,
            ).add_to(self.__geo_map)
            plotted_count += 1
        logging.info(f'Plotted {plotted_count} markers.')
