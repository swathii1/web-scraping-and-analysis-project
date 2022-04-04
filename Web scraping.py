#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#PART 1
from bs4 import BeautifulSoup
import requests
import time
from urllib.request import Request, urlopen


def main():
    try:
        session_requests = requests.session()
        site = "https://www.planespotters.net/user/login"
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        page1 = session_requests.get(site, headers = hdr)
        doc1 = BeautifulSoup(page1.content, 'html.parser')
        
        #Look at the unmodified source.
        #              
        print(doc1)
        
        # Here we extract the token required to login
        input1 = doc1.select("div.planespotters-form input[name=csrf]")[0]
        input2 = doc1.select("div.planespotters-form input[name=rid]")[0]
        #cookie_key = data-cookiefirst-key
        token1 = input1.get("value")
        token2 = input2.get("value")
        token = [token1,token2]
        cookies1 = session_requests.cookies.get_dict()
        print("The token is ", token)
         
        #Always pause between two requests.
                      
        time.sleep(5) # 3s


        #An open session carries the cookies and allows you to make post requests
        #session_requests = requests.session()

        res = session_requests.post(site, 
                                data = {# "referer" : "https://www.planespotters.net/user/login",
                                      # "mode" : "login",
                                      "username" : "swathii", # your username here
                                      "password" : "abc123", # your password here
                                      "csrf" : token1,
                                      "rid" : token2},
                                headers = hdr,
                                cookies = cookies1,
                                timeout = 15)
        #
        # This will get us the Cookies.
        # 
        cookies2 = session_requests.cookies.get_dict()
                     
        print(" The cookies are {} {}".format(cookies1, cookies2))

        #
        # And this is the easiest way to remain in session.
        #
        URL = "https://www.planespotters.net/member/profile"
        page2 = session_requests.get(URL, headers = hdr, cookies= {**cookies1, **cookies2})
        
        doc2 = BeautifulSoup(page2.content, 'html.parser')
        

        print(doc2);
        print();
        print(cookies2)
        print(bool(doc2.findAll(text = "swathii"))) # your username here
        print(bool(doc2.findAll(text = "Profile")))
    
    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    main()

