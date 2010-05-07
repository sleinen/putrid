import sys, pexpect
from login import LoginMethod

class SshLoginMethod(LoginMethod):
    def __init__(self, device, conf):
        LoginMethod.__init__(self, device, conf)
        self.sshcmd = conf.sshcmd(device.name)
    def login(self, device):
        if self.sshcmd:
            cmd_args = self.sshcmd.split(" ")
            cmd = cmd_args[0]
            cmd_args = cmd_args[1:]
        else:
            cmd = 'ssh'
            cmd_args = []
        if self.username:
            cmd_args.extend(['-l', self.username])
        cmd_args.append(device.name)
        p = device.process = pexpect.spawn(cmd, cmd_args)
        if device.debug:
            p.logfile = sys.stderr
        p.expect("(Are you sure you want to continue connecting \(yes/no\)\? |password: )$")
        if p.after.endswith("password: "):
            pass
        else:
            p.sendline("yes")
            p.expect("password: $")
        p.sendline(self.password)
