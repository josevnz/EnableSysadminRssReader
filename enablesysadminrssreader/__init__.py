from typing import Dict, Any, List

import requests
from lxml.etree import fromstring, XMLParser

ENABLE_SYSADMIN_URL = "https://www.redhat.com/sysadmin/rss.xml"


def parse_rss(xml_data: str) -> List[Dict[str, Any]]:
    """
    Parse the Enable Sysadmin RSS feed
    :param xml_data: RAW XML as a string.
    :return: Dictionary with parsed items
    """
    parsed_rss = []
    parser = XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = fromstring(xml_data.encode('utf-8'), parser=parser)
    for first_level in root.getchildren():
        for elem in first_level.getchildren():
            if elem.tag == 'item':
                article = {
                    'title': None,
                    'link': None,
                    'description': None
                }
                for link_parts in elem.getchildren():
                    if link_parts.tag == 'title':
                        article['title'] = link_parts.text
                    elif link_parts.tag == 'link':
                        article['link'] = link_parts.text
                    elif link_parts.tag == 'description':
                        article['description'] = link_parts.text
                parsed_rss.append(article)
    return parsed_rss


def get_rss(url: str = ENABLE_SYSADMIN_URL) -> str:
    response = requests.get(
        headers={'UserAgent': 'EnableSysadminRssReader'},
        url=url
    )
    response.raise_for_status()
    return response.text
