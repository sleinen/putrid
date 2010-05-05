import re, fnmatch

class CloginConfiguration:
    known_attributes = [
         'autoenable', 'ciphertype',
         'enableprompt', 'enauser',
         'identity', 'method', 'noenable',
         'passphrase', 'passprompt', 'password',
         'sshcmd',
         'user', 'userpassword', 'userprompt']
    def __init__(self):
        self.attributes = {}
        for attr in self.known_attributes:
            self.attributes[attr] = []
    def attr_for_device(self, attr, devicename):
        for glob, value in self.attributes[attr]:
            if fnmatch.fnmatch(devicename, glob):
                return value
        return None
    def passwords(self, devicename):
        return self.attr_for_device('password', devicename).split(" ")
    def password(self, devicename):
        return self.passwords(devicename)[0]
    def enable_password(self, devicename):
        return self.passwords(devicename)[1]
    def login_method(self, devicename):
        return self.attr_for_device('method', devicename)
    def username(self, devicename):
        return self.attr_for_device('user', devicename)
    def sshcmd(self, devicename):
        return self.attr_for_device('sshcmd', devicename)
    def read_cloginrc(self, filename):

        class CloginParseError(Exception):
            def __init__(self, message):
                self.message = message
            def __str__(self):
                return self.message

        class CloginUnknownAttributeError(CloginParseError):
            def __init__(self, attr):
                self.attr = attr
            def __str__(self):
                return "Unknown attribute " + self.attr

        class CloginUnparseableLine(CloginParseError):
            def __init__(self, line):
                self.attr = line
            def __str__(self):
                return "Cannot parse line " + self.line

        f = open(filename)
        for line in f:
            if line.startswith("#") or re.search("^\s*$", line):
                pass
            else:
                m = re.search("^\s*add\s+(\S+)\s+(\S+)\s+(.*)$", line)
                if m:
                    attr, device, value = m.group(1), m.group(2), m.group(3)
                    if attr in self.known_attributes:
                        self.attributes[attr].append([device, value])
                    else:
                        raise CloginUnknownAttributeError(attr)
                else:
                    m = re.search("^\s*include\s+(\S+)\s*$", line)
                    if m:
                        self.read_cloginrc(m.group(1))
                    else:
                        raise CloginUnparseableLine(line)
        f.close()
