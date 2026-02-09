import nmap
import socket

class JokerEngine:
    def __init__(self):
        self.nm = nmap.PortScanner()

    def run_deep_scan(self, target):
        
        flags = "-sV -T4 -Pn --script=vuln"
        self.nm.scan(target, arguments=flags)
        return self.nm

    def resolve_target(self, target):
        try:
            return socket.gethostbyname(target)
        except:
            return target

    def get_service_risk(self, port, version):
        
        if "23" in str(port) or "telnet" in version.lower():
            return "CRITICAL"
        return "STABLE"
