import pprint
import subprocess


def map_wlan():
    '''
    info:
        -some of networks got 9 lines, some 10
    '''
    
    command = 'netsh wlan show networks mode=bssid'
    cmd_output = subprocess.Popen(command,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  encoding="cp852",
                                  universal_newlines=True)

    response = cmd_output.stdout.read()
    networks_str = [item for item in response.split('\n\n')[1:] if item.strip()]
    keywords = ['SSID', 'type', 'auth', 'cipher', 'BSSID', 'signal', 'radio', 'channel', 'basic_speed', 'other_speed']
    
    networks = []
    for item in networks_str:
        values = [(line.split(':', 1)[1]).strip() for line in item.splitlines()]
        network = dict(zip(keywords, values))
        networks.append(network)
        
    return networks
    
    
if __name__ == "__main__":
    networks = map_wlan()
    
    for network in networks:
        pprint.pprint(network)
        print()
