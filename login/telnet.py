import sys, pexpect
from login import LoginMethod

class TelnetLoginMethod(LoginMethod):
    def login(self, device):
        cmd = 'telnet'
        cmd_args = []
        cmd_args.append(device.name)
        p = device.process = pexpect.spawn(cmd, cmd_args)
        if device.debug:
            p.logfile = sys.stderr
        p.expect("Username: $")
        p.sendline(self.username)
        p.expect("Password: $")
        p.sendline(self.password)
