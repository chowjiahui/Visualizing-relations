import time
import os
from json import JSONDecodeError
import codecs

import requests
from requests import Timeout
from urllib3.exceptions import ReadTimeoutError
from tika import parser


import codecs

class TritApi:
    def __init__(self, access_token, inputformat):
        self.calais_url = 'https://api.thomsonreuters.com/permid/calais'
        self.inputformat = inputformat
            
        self.headers = {'X-AG-Access-Token': access_token, 
                        'Content-Type':'text/raw',
                        'outputformat': 'application/json'  # 'xml/rdf'
                       }
        
    def readFiles(self, files):
        results = []
        print("Reading contents of folder...")        
        folder = os.listdir(files)
        
        for i, file_name in enumerate(folder):
            filepath = os.path.join(files, file_name)
            if os.path.isfile(filepath):
                if self.inputformat == 'pdf':
                    raw = parser.from_file(filepath)
                    content = raw['content']
                elif self.inputformat == 'text':
                    with codecs.open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()          
                result = self.classify(content)
                print("Sent " + str(i+1) + " file" + "s"*min(1,i) + " to TRIT")
                results.append(result)
        print("Finished retrieving results from TRIT.")
        return results

    def classify(self, text):
        # if len(text.split()) > 1000:
        #     print('Document seem to have more than 1000 words')

        text = text.encode('utf-8')
        while True:
            try:
                response = requests.post(self.calais_url, data=text, headers=self.headers, timeout=80)
                if response.status_code == 429:
                    print("Error status code: %d" % response.status_code)
                    print(str(response.content))
                    if "exceeded the concurrent request limit" in str(response.content):
                        print('Sleep 10 seconds!')
                        time.sleep(10)
                    else:
                        raise Exception(response.content)

                elif not response.ok:
                    print("Error status code: %d" % response.status_code)
                    raise Exception("Something wrong (code=%s): %s" % (response.status_code, response.content))

                else:
                    return response.json(encoding='utf-8')

            except (Timeout, ReadTimeoutError) as e:
                # print("call TRIT Api timeout", e)
                raise e

            except JSONDecodeError as e:
                # print('Decode TRIT Api response error', e)
                raise e

            except Exception as e:
                # print('Something errors', e)
                raise e