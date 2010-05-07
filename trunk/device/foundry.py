import pexpect
from device.generic import ManagedDevice
import device.cisco

class ManagedDevice(device.cisco.ManagedDevice):
    """Brocade/Foundry devices are very similar to Cisco IOS devices.
    We override a few methods where the two differ.
    """
    def content_type(self):
        return "foundry"
    def set_length_width(self, length, width):
        ## Foundry/Brocade devices don't seem to have "terminal width"
        p = self.process
        p.sendline("terminal length "+str(self.length))
        p.expect(self.fullprompt)
    def commands(self):
        return ["show version"]
    def disable(self):
        self.process.sendline("quit")
        self.enabled = False
    def logout(self):
        if self.enabled:
            self.disable()
        self.process.sendline("exit")
        self.process.expect(pexpect.EOF)
        device.generic.ManagedDevice.logout(self)
