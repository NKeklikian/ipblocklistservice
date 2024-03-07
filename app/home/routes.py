from app.home import home_blueprint
from app.home.ip_blocklist_service import IpBlocklistService
import socket
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# Exception handling should be handled in
# API middleware if more endpoints are added to the API
@home_blueprint.route('/api/ips/<string:ipv4>', methods=["GET"])
def is_in_blocklist(ipv4):
    error_dict = {'message': None, 'trace': None}
    logging.info('Received IP: ' + ipv4)
    try:
        socket.inet_aton(ipv4)
    except OSError:
        error_dict['message'] = 'Invalid IP address'
        return error_dict, 422
    try:
        return {'is_in_blocklist': IpBlocklistService.is_blocklisted(ipv4)}
    except Exception as e:
        error_dict['message'] = 'Redis failed'
        error_dict['trace'] = str(e)
        return error_dict, 424  # Failed dependency
