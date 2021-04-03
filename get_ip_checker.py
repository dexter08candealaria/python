import boto3
import json
import pprint
import datetime
import logging
import sys

pp = pprint.pprint

#Set variables
region = 'us-east-1'
subnets = []
warn_percent = 25

#Set client
session = boto3.Session(profile_name='dexter-test')
ec2 = session.resource('ec2', region_name=region)
subnet_iterator = ec2.subnets.all()

# Message to log at end and optionally send to SNS
message = ''


# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')

# create console handler to write to console (stdout)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.WARNING)
logger.addHandler(ch)

def subnet_mapper(netmask):
    mapping = {
            '16': 65534,
            '17': 32766,
            '18': 16382,
            '19': 8190,
            '20': 4094,
            '21': 2046,
            '22': 1022,
            '23': 510,
            '24': 254,
            '25': 126,
            '26': 62,
            '27': 30,
            '28': 14,
            '29': 6,
            '30': 2,
        }
    
    return mapping.get(netmask, 224)

def get_subnets():
    try:
        global subnets
        subnets = []
        response = subnet_iterator
        for i in response:
            subnets.append(i)
    except Exception as e:
        logging.error(e)
        logger.error('There was a proble getting sunbet info')
        

def check_subnets():
    global subnets, warn_percent
    
    try:
        private_ips = []
        for subnet in subnets:
            netmask = str(subnet.cidr_block[-2:])
            available_hosts = subnet_mapper(netmask)
            network_interface = subnet.network_interfaces


            for network_interface in network_interface.iterator():
                for private_ip_address in network_interface.private_ip_addresses:
                    private_ips.append(private_ip_address['PrivateIpAddress'])

            ip_count = (len(private_ips))


            if (100 * float(ip_count)/float(available_hosts)) >= warn_percent:
                print('IP Addresses remaining for {} - {}'.format(subnet.id, available_hosts - ip_count))
                
    except Exception as e:
        logger.error(e)
        logger.error('There was a problem collecting IP info for Subnet: {}'.format(subnet.id))


start_message = 'Started IP check at {}s'.format(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
logger.info(start_message)


get_subnets()
check_subnets()