import pexpect
from login.ssh import SshLoginMethod
from login.telnet import TelnetLoginMethod

class ManagedDevice:
    ""
    def __init__(self, name, conf):
        self.name = name
        self.enablepw = conf.enable_password(name)
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
        self.parse_initial_prompt()
    def login(self):
        self.ssh_login()
        self.enable()
    def command_results(self, command):
        self.process.sendline(command)
        self.process.expect(command+"$") # echo
        self.process.expect(self.fullprompt)
        return self.process.before.rstrip("\n")
    def logout(self):
        pass
    def pseudocomment(self, string):
        return "\n".join(map(lambda x: "! " + x, string.split("\n")))
