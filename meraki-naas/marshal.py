READ_ME = '''
=== PREREQUISITES ===
Run in Python 3

Install requests and Meraki Dashboard API Python modules:
pip[3] install requests [--upgrade]
pip[3] install meraki [--upgrade]

=== DESCRIPTION ===
This script finds all MR access points in an organization, and then iterates
through all networks to obtain the Air Marshall information of the APs.

For questions, contact Jeffry at jehandal@cisco.com.

=== USAGE ===
python3 marshal.py {login parameters file}
'''


import configparser
import csv
from datetime import datetime
import getopt
import logging
from meraki import meraki
import requests
import sys


# Prints READ_ME help message for user to read
def print_help():
    lines = READ_ME.split('\n')
    for line in lines:
        print('# {0}'.format(line))

logger = logging.getLogger(__name__)

def configure_logging():
    logging.basicConfig(
        filename='{}_log_{:%Y%m%d_%H%M%S}.txt'.format(sys.argv[0].split('.')[0], datetime.now()),
        level=logging.DEBUG,
        format='%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def read_config(file):
    cp = configparser.ConfigParser()
    try:
        cp.read(file)
        api_key = cp.get('access', 'key')
        org_id = cp.get('access', 'org')
    except:
        print_help()
        sys.exit(2)
    return api_key, org_id


def data_value(dictionary, key):
    try:
        return dictionary[key]
    except:
        return ''


def main(api_key, org_id):
    # Get the org's inventory
    inventory = meraki.getorginventory(api_key, org_id)

    # Filter for only MR devices
    aps = [device for device in inventory if device['model'][:2] in ('MR') and device['networkId'] is not None]

    # Create array to save all the rogue APs accros the organization
    rogues = []
    for ap in aps:
        roguedata = meraki.badssid(api_key, ap['networkId'], 10800, suppressprint=True)

    # Extract all rogue SSIDs single line
    #rogues.append([rogue['ssid'] for rogue in roguedata if 'ssid' in rogue])

    # Extract all rogue SSIDs to a file
    logger.info(f'Preparing the output file. Check your local directory.')
    timenow = '{:%Y%m%d_%H%M%S}'.format(datetime.now())
    filename = 'rogues_{0}.csv'.format(timenow)
    output_file = open(filename, mode='w', newline='\n')
    field_names = ['Rogue SSIDs', 'Channels']
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(field_names)
    for rogue in roguedata:
        if 'ssid' in rogue: #skip if no data
            csv_row = [data_value(rogue, 'ssid'), data_value(rogue, 'channels')]
            csv_writer.writerow(csv_row)

    output_file.close()
    m = MultipartEncoder({'roomId': 'Y2lzY2.....',
                          'text': 'Rogue APs File',
                          'files': (filename, open(filename, 'rb'),
                          'image/png')})

    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                      headers={'Authorization': 'Bearer ACCESS_TOKEN',
                      'Content-Type': m.content_type})

    print r.text



if __name__ == '__main__':
    # Configure logging to stdout
    configure_logging()
    # Define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # Set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # Tell the handler to use this format
    console.setFormatter(formatter)
    # Add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # Output to logfile/console starting inputs
    start_time = datetime.now()
    logger.info('Started script at {0}'.format(start_time))

    inputs = sys.argv[1:]
    print(len(inputs))
    if len(inputs) == 0:
        print_help()
        sys.exit(2)

    config_file = inputs[0]


    #parse input file.
    api_key, org_id = read_config(config_file)

    #Execute the program
    main(api_key, org_id)


    # Finish output to logfile/console
    end_time = datetime.now()
    logger.info('Ended script at {0}'.format(end_time))
    logger.info(f'Total run time = {end_time - start_time}')
