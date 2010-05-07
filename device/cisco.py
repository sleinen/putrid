import pexpect
from device.generic import ManagedDevice

class CiscoDevice(ManagedDevice):
    ""

    def __init__(self, name, conf):
        ManagedDevice.__init__(self, name, conf)
        self.width = 80
        self.length = 0
    def enable(self):
        p = self.process
        p.sendline("enable")
        p.expect("password: $")
        p.sendline(self.enablepw)
        self.fullprompt = self.hostname + "#$"
        p.expect(self.fullprompt)
    def login(self):
        ManagedDevice.login(self)
        p = self.process
        p.sendline("terminal length "+str(self.length))
        p.expect(self.fullprompt)
        p.sendline("terminal width "+str(self.width))
        p.expect(self.fullprompt)
    def parse_initial_prompt(self):
        self.process.expect(">$")
        self.hostname = self.process.before.rpartition("\n")[2]
    def commands(self):
        return ["show version"]
        ## return ["show version",
        ##         "show idprom backplane"]
    def logout(self):
        self.process.sendline("quit")
        self.process.expect(pexpect.EOF)
        ManagedDevice.logout(self)
