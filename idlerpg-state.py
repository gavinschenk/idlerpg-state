#!/usr/bin/env python3
#description     : Get propertys of your idlerpg character
#author          : Gavin Schenk <g.schenk@gmx.de>
#copyright       : gsc(2021)
#licence         : Apache License 2.0

import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlencode, quote_plus

__version__='0.9'


def process_idlerpg_query( args ):

    payload = {'player':args.character }
    payload_encoded = urlencode(payload, quote_via=quote_plus)
    url = f'https://idlerpg.lolhosting.net/xml.php?{payload_encoded}'
    response = urllib.request.urlopen(url).read()
    tree = ET.fromstring(response)

    if args.showxml:
        print(ET.tostring(tree, encoding='utf8').decode('utf8'))
        return 0

    for res in tree.findall(args.property):
        if res.text is not None:
            print(res.text)
            return 0

    for child in tree:
        for res in child.findall(args.property):
            if res.text is not None:
                print(res.text)
                return 0

    return 1

def parse_arguments():
    parser = argparse.ArgumentParser(description='Get properties of your idlerpg char.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-x', '--showxml', action='store_true', help="Print out full xml and exit")
    parser.add_argument('character', type=str, help="Your characters name")
    parser.add_argument('-p', '--property', type=str, default='online', help="Property you want")
    return parser.parse_args()

def main():
    args = parse_arguments()
    result =  process_idlerpg_query( args )
    sys.exit(result)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()

