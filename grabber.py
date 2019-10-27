#!/usr/bin/python3

'''

Litres grabbing utility 

MinHinProm, 2019

'''

import requests, time


LOGIN_URL = 'https://www.litres.ru/pages/login/'
HEADERS = { #Requests headers
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

def timestamp(): #Timestamp in Litres format function
    return str(int(time.time() * 1000))

s = requests.Session() #Create new session
csrf = ""

print("       _____ _______  ______ _______ _______	")
print("|        |      |    |_____/ |______ |______	")
print("|_____ __|__    |    |    \_ |______ ______|	")
print("                                            	")
print(" ______  ______ _______ ______  ______  _____ __   _  ______	")
print("|  ____ |_____/ |_____| |_____] |_____]   |   | \  | |  ____	")
print("|_____| |    \_ |     | |_____] |_____] __|__ |  \_| |_____|	")
print("                                                            	")
print("_______  _____   _____        	")
print("   |    |     | |     | |     	")
print("   |    |_____| |_____| |_____	")
print("                              	")
print("Coded by: Vladislav Kalugin  	\n")


login = input("Login: ")
password = input("Password: ")
print("Getting CSRF...")

loginData = {
    'csrf': '',
    'login': login,
    'pre_action': 'login',
    'pwd': password,
    'ref_url': '/',
    'showpwd': 'on',
    'timestamp': timestamp(),
    'utc_offset_min': '180',
}

payload = s.post(LOGIN_URL, data=loginData, headers=HEADERS, allow_redirects=False).text #Request CSRF data

# "csrf" : "443851:1572108634:8c204a17f1d8ffaa5611df4f3a2515816e619dab41455f699f42cd9515a94fc4"

for i in range(0, len(payload)):
    if(payload.find("\"csrf\"", i, i + 6) != -1):
        csrfStart = payload.find("\"", i + 7) + 1
        csrfEnd = payload.find("\"", csrfStart + 1)
        csrf = payload[csrfStart:csrfEnd]
        print("CSRF: " + csrf)
        break

if(csrf == ""): exit("CSRF not found!")

print("Logging in...")

loginData = {
    'csrf': csrf,
    'login': login,
    'pre_action': 'login',
    'pwd': password,
    'ref_url': '/',
    'showpwd': 'on',
    'timestamp': timestamp(),
    'utc_offset_min': '180',
}

payload = s.post(LOGIN_URL, data=loginData, headers=HEADERS, allow_redirects=False).text #Login request

if (payload == ""): print("Logged in!")
else: exit(payload + "\n Login error!")

while True:
    download_dir = input("Enter download dir: ")

    print('Page url format: https://www.litres.ru/pages/get_pdf_page/?file={file_id}&page={page}&rt={rt}&ft={file_format}')
    print('Page url format: https://www.litres.ru/pages/get_pdf_page/?file={file_id}&page=  -- start url')
    print('Page url format: &rt={rt}&ft=  --  end url')

    start_url = input("Enter start url: ")
    end_url = input("Enter end url: ")

    start_page = int(input("Enter start page: "))
    end_page = int(input("Enter end page: "))

    delay = int(input("Enter delay between requests: "))

    for i in range(start_page, end_page + 1):
        print("Downloading page " + str(i))

        code_stat = False
        
        while True: 
            ext = ""

            if (not code_stat):
                url = start_url + str(i) + end_url + "jpg"
                code_stat = True
                ext = "jpg"
            elif (code_stat):
                url = start_url + str(i) + end_url + "gif"
                ext = "gif"
                code_stat = False

            print("URL: " + url)

            time.sleep(delay) #Delay between requests
            
            response = s.get(url, headers=HEADERS)

            if(response.status_code == 200): 
                if(response.headers.get("Content-Type") == "image/jpeg, image/jpeg" or response.headers.get("Content-Type") == "image/gif, image/gif"):
                    f = open(download_dir + "page_" + str(i) + "." + ext, "wb")
                    f.write(response.content)
                    f.close()
                    print("Downloaded!")
                    break
                print("Server returned wrong Content-Type: " + response.headers.get("Content-Type"))

            elif (response.status_code == 500):
                print("Server returned 500 status code! Waiting for one minute...")
                time.sleep(60)
            else:
                print("Got error code: " +  str(response.status_code))


    print("Download complete!")
    agreement = input("Do you want to download another book? (y/n): ")
    if(agreement != "y"): break
