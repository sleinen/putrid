class LoginMethod:
    def __init__(self, device, conf):
        self.device = device
        self.conf = conf
        self.username = conf.username(device.name)
        self.password = conf.password(device.name)

import login.telnet
import login.ssh
