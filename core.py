import nmap
import os
import socket
from datetime import datetime
from fpdf import FPDF

class JokerSigmaCore:
    def __init__(self):
        self.scanner = nmap.PortScanner()
        self.sig = "CREATED BY JOKER | SIGMA-V99"

    def execute_elite_audit(self, target):
        
        elite_flags = "-sS -sV -sC -O -T4 --version-all --script=vuln,banner,realvnc-auth-bypass"
        try:
            self.scanner.scan(target, arguments=elite_flags)
            return self._structure_intel(target)
        except Exception as e:
            return {"status": "CRITICAL_ERROR", "msg": str(e)}

    def _structure_intel(self, target):
        intel = {
            "target": target,
            "ip": socket.gethostbyname(target),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "author": "JOKER",
            "nodes": []
        }
        for host in self.scanner.all_hosts():
            node = {
                "address": host,
                "os": self.scanner[host].get('osmatch', [{'name': 'Stealth/Unknown'}])[0]['name'],
                "status": self.scanner[host].state(),
                "vectors": []
            }
            for proto in self.scanner[host].all_protocols():
                for port in self.scanner[host][proto].keys():
                    v = self.scanner[host][proto][port]
                    node["vectors"].append({
                        "port": port,
                        "service": v['name'],
                        "product": v.get('product', 'N/A'),
                        "version": v.get('version', 'N/A'),
                        "vulns": v.get('script', {})
                    })
            intel["nodes"].append(node)
        return intel

    def build_sigma_report(self, data):
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(0, 0, 210, 60, 'F')
        
        pdf.set_font("Courier", 'B', 32)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(190, 20, "JOKER SIGMA INTEL", ln=True, align='C')
        
        pdf.set_font("Courier", 'B', 12)
        pdf.set_text_color(0, 255, 0)
        pdf.cell(190, 10, "CYBER RECONNAISSANCE FRAMEWORK", ln=True, align='C')
        
        pdf.set_font("Courier", 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(190, 10, f"STRICTLY CONFIDENTIAL | AUTH: {data['author']}", ln=True, align='C')
        
        pdf.ln(30)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Courier", 'B', 11)
        pdf.cell(0, 10, f"VECTOR: {data['target']} ({data['ip']}) | TIME: {data['timestamp']}", ln=True)
        pdf.line(10, 85, 200, 85)
        
        for node in data['nodes']:
            pdf.ln(10)
            pdf.set_fill_color(15, 15, 15)
            pdf.set_text_color(0, 255, 0)
            pdf.set_font("Courier", 'B', 14)
            pdf.cell(190, 12, f"HOST: {node['address']} [{node['os']}]", ln=True, fill=True)
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Courier", 'B', 9)
            pdf.cell(20, 8, "PORT", 1, 0, 'C')
            pdf.cell(40, 8, "SERVICE", 1, 0, 'C')
            pdf.cell(130, 8, "VULNERABILITY & VERSION DATA", 1, 1, 'C')
            
            pdf.set_font("Courier", size=8)
            for v in node['vectors']:
                pdf.cell(20, 8, str(v['port']), 1)
                pdf.cell(40, 8, v['service'], 1)
                info = f"{v['product']} {v['version']}"
                pdf.cell(130, 8, info[:75], 1, 1)
                
                if v['vulns']:
                    pdf.set_text_color(255, 0, 0)
                    pdf.multi_cell(190, 5, f"CRITICAL: {str(v['vulns'])}", border=1)
                    pdf.set_text_color(0, 0, 0)

        path = f"JOKER_SIGMA_{data['target'].replace('.', '_')}.pdf"
        pdf.output(path)
        return path
