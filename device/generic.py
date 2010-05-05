import pexpect
from login.ssh import SshLoginMethod
from login.telnet import TelnetLoginMethod

class ManagedDevice:
    ""
    def __init__(self, name, conf):
        self.name = name
        self.enablepw = conf.enable_password(name)
        self.width = 80
        self.length = 0
        self.child = None
        self.process = None
        self.debug = False
        method = conf.login_method(name)
        if method == 'ssh':
            self.login_method = SshLoginMethod(self, conf)
        elif method == 'telnet':
            self.login_method = TelnetLoginMethod(self, conf)
    def ssh_login(self):
        self.login_method.login(self)
    def enable(self):
        p = self.process
        p.sendline("enable")
        p.expect("password: $")
        p.sendline(self.enablepw)
        p.expect(self.fullprompt)
    def login(self):
        self.ssh_login()
        self.enable()
        p = self.process
        p.sendline("terminal length "+str(self.length))
        p.expect(self.fullprompt)
        p.sendline("terminal width "+str(self.width))
        p.expect(self.fullprompt)
    def command_results(self, command):
        self.process.sendline(command)
        self.process.expect(self.fullprompt)
        return self.process.before
    def commands(self):
        return ["show version"]
        ## return ["show version",
        ##         "show idprom backplane"]
    def logout(self):
        self.process.sendline("quit")
        self.process.expect(pexpect.EOF)
