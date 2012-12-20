# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import posixpath
import socket
import tempfile
import traceback
from mozdevice import DeviceManagerSUT, DMError
from mozpool import config

logger = logging.getLogger('sut.cli')

def sut_verify(device_fqdn):
    logger.info('Verifying that SUT agent is running.')
    try:
        DeviceManagerSUT(device_fqdn)
    except DMError:
        logger.error('Exception initiating DeviceManager!')
        logger.error(traceback.format_exc())
        return False
    logger.info('Successfully connected to SUT agent.')
    return True

def check_sdcard(device_fqdn):
    logger.info('Checking SD card.')
    success = True
    try:
        dm = DeviceManagerSUT(device_fqdn)
        dev_root = dm.getDeviceRoot()
        if dev_root:
            d = posixpath.join(dev_root, 'autophonetest')
            dm.removeDir(d)
            dm.mkDir(d)
            if dm.dirExists(d):
                with tempfile.NamedTemporaryFile() as tmp:
                    tmp.write('autophone test\n')
                    tmp.flush()
                    dm.pushFile(tmp.name, posixpath.join(d, 'sdcard_check'))
                    dm.removeDir(d)
                logger.info('Successfully wrote test file to SD card.')
            else:
                logger.error('Failed to create directory under device '
                              'root!')
                success = False
        else:
            logger.error('Invalid device root.')
            success = False
    except DMError:
        logger.error('Exception while checking SD card!')
        logger.error(traceback.format_exc())
        success = False
    return success

def reboot(device_fqdn):
    logger.info('Rebooting device via SUT agent.')
    addr = socket.gethostbyname(config.get('server', 'fqdn').split(':')[0])
    port_manager = PortManager(addr)
    port = int(port_manager.reserve())
    dm = DeviceManagerSUT(device_fqdn)
    try:
        print 'reboot callback server on %s:%d' % (addr, port)
        dm.reboot(addr, port_manager.use(port))
    except DMError:
        logger.error('Reboot failed: %s' % traceback.format_exc())
        return False
    logger.info('Received callback; device is back up.')
    return True


class PortManager(object):
    '''
    Obtain a free port on ip address

    usage:
           port_manager = PortManager(ipaddress)
           port = port_manager.reserve()
           port_manager.use(port)

    See
    http://docs.python.org/library/socket.html
    http://code.activestate.com/recipes/531822-pick-unused-port/

    Chapter 4: Elementary Sockets
    UNIX Network Programming
    Networking APIs: Sockets and XTI
    Volume 1, Second Edition
    W. Richard Stevens
    '''

    def __init__(self, ipaddr):
        self.ipaddr = ipaddr
        self.reserved_ports = {}

    def reserve(self):
        '''
        Reserve a port for later use by creating a socket
        with a random port. The socket is left open to
        prevent others from using the port.
        '''
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.ipaddr, 0))
            port = sock.getsockname()[1]
            self.reserved_ports[port] = sock
            return port

    def use(self, port):
        '''
        Prepare a reserved port for use by closing its socket and
        returning the port.
        '''
        sock = self.reserved_ports[port]
        sock.close()
        return port
