import pexpect
import device.generic

class ManagedDevice(device.generic.ManagedDevice):
    """Cisco IOS Devices
    """

    ## Be liberal in what you accept... this should match the enable
    ## password prompt on both Cisco and Brocade/Foundry:
    ##
    enable_password_prompt_re = ".*[Pp]assword: ?$"

    def __init__(self, name, conf):
        device.generic.ManagedDevice.__init__(self, name, conf)
        self.width = 80
        self.length = 0
        self.enabled = False
    def enable(self):
        p = self.process
        p.sendline("enable")
        p.expect(self.enable_password_prompt_re)
        p.sendline(self.enablepw)
        self.fullprompt = self.hostname + "#$"
        p.expect(self.fullprompt)
        self.enabled = True
    def login(self):
        device.generic.ManagedDevice.login(self)
        self.set_length_width(self.length, self.width)
    def set_length_width(self, length, width):
        p = self.process
        p.sendline("terminal length "+str(self.length))
        p.expect(self.fullprompt)
        p.sendline("terminal width "+str(self.width))
        p.expect(self.fullprompt)
    def parse_initial_prompt(self):
        self.process.expect(">$")
        self.hostname = self.process.before.rpartition("\n")[2]
        if "@" in self.hostname:
            ## On Foundry/Brocade devices, the hostname is sometimes
            ## prefixed with e.g. "telnet@" or "SSH@".  We strip this.
            ##
            ## This isn't necessary on Cisco IOS devices, but doesn't
            ## hurt either.
            ##
            self.hostname = self.hostname.rpartition("@")[2]
    def pp_show_version(self, string):
        print self.pseudocomment(string)
    def commands(self):
        return [{"show version": self.pp_show_version}]
        ## return ["show version",
        ##         "show idprom backplane"]
    def disable(self):
        self.process.sendline("disable")
        self.enabled = False
    def logout(self):
        if self.enabled:
            self.disable()
        self.process.sendline("quit")
        self.process.expect(pexpect.EOF)
        device.generic.ManagedDevice.logout(self)
