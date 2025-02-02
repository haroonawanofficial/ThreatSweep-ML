import nmap
import requests
from cve_detection_metasploit_modules import exploit_cves
from database import DatabaseManager
from machine_learning import MachineLearningModel

class NmapScanner:
    def __init__(self, target):
        self.target = target
        self.db = DatabaseManager()

    def scan(self):
        nm = nmap.PortScanner()
        nm.scan(self.target, arguments='-p- -sV -T4')  # Scan all 65,535 ports
        return nm.all_hosts(), nm[self.target]['tcp']

    def detect_cves(self, service_ports):
        for port, service_info in service_ports.items():
            if 'product' in service_info and 'version' in service_info:
                service_name = service_info['product']
                service_version = service_info['version']
                cve_list = self.detect_cves_for_service(service_name, service_version)

                if cve_list:
                    print(f"Service on port {port} ({service_name} {service_version}) is affected by CVEs: {', '.join(cve_list)}")
                    exploit_cves(self.target, service_name, service_version, port, cve_list)
                else:
                    print(f"No CVEs found for {service_name} {service_version} on port {port}")

    def detect_cves_for_service(self, service_name, service_version):
        cve_database_url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:2.3:a:{service_name}:{service_version}"
        try:
            response = requests.get(cve_database_url)
            response.raise_for_status()
            cve_data = response.json()
            cve_list = [entry['cve']['CVE_data_meta']['ID'] for entry in cve_data['result']['CVE_Items']]
            return cve_list
        except requests.exceptions.RequestException as e:
            print(f"Error querying NVD: {e}")
            return []

    def start_scan(self):
        scan_results = self.scan()
        for target, service_data in scan_results.items():
            for service_info in service_data:
                service_name = service_info['name']
                service_version = service_info['version']
                port = service_info['port']
                cve_list = service_info['cve_list']

                exploitation_result = exploit_cves(target, service_name, service_version, port, cve_list)

                self.db.store_exploitation_result(target, service_name, service_version, port, cve_list, exploitation_result)

if __name__ == '__main__':
    target = "127.0.0.1"
    scanner = NmapScanner(target)
    scanner.start_scan()
