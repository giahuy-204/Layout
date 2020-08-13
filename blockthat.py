import time
from datetime import datetime as dt
import sqlite3

#use from database
def getWebsites():
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	cur.execute("SELECT url FROM db")
	rows = cur.fetchall()
	conn.close()
	return rows

#hosts file path [this is for windows]
hosts_temp = "hosts"
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
#ip
redirect = "127.0.0.1"

websites = []

for web in getWebsites():
	websites.append(web[0])


while True:
    if dt(dt.now().year, dt.now().month, dt.now().day,0) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day,23):
        print ("Starting...")
        with open(hosts_path,'r+') as file:
            content=file.read()
            for site in websites:
                if site in content:
                    pass
                else:
                    file.write(redirect+" "+site+"\n")
    else:
        with open(hostsPath,'r+') as file:
            content=file.readlines()
            file.seek(0)
            for line in content:
                if not any(site in line for site in websites):
                    file.write(line)
            file.truncate()
        print ("Fun hours...")
    time.sleep(5)
if __name__ == "__main__":
    main()
