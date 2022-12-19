import requests
import pathlib
import urllib3
# we have to use verify=False I don't care about integrity
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


locations = {
    'om_alfaham': '9', 
    'ofakim': '18', 
    'eilat': '20', 
    'ashdod': '15', 
    'ashkelon': '30', 
    'gat': '10', 
    'dimona': '19', 
    'haifa': '7', 
    'tiberias': '5', 
    'jerusalem_beit_hanina': '11', 
    'jerusalem_new_city': '24', 
    'karmiel': '3', 
    'naharia': '1', 
    'the_galilee': '28', 
    'afula': '8', 
    'kiryat_hayim': '6', 
    'kiryat_shmona': '2'
}


months = [
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '09',
    '10',
    '11',
    '12',
]

class AmalApi:

    def __init__(self) -> None:
        self.s = requests.session()
        self.bypass_incapsula()


    def bypass_incapsula(self):
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }
        # https://stackoverflow.com/questions/66683038/ubuntu-server-16-04-error-60-ssl-certificate-problem
        response = self.s.get('https://www.amal-nehiga.org.il/amal_rishum/base/courses.php?type=1', verify=False)

    def available_appointment(self, location, month) -> True:
        self.s.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.amal-nehiga.org.il',
            'Connection': 'keep-alive',
            'Referer': 'https://www.amal-nehiga.org.il/amal_rishum/base/courses.php?type=1',
            # 'Cookie': 'visid_incap_2221763=h4zj6ZZcQx2TzCm4QuQWbiKVn2MAAAAAQUIPAAAAAAC/z5U9GM6X/VuDUIA5yR+f; incap_ses_264_2221763=6Gc5K8w8GXRWv2QFE+upAyKVn2MAAAAAU5RIt370iFfC9A4ISUuhiQ==; incap_ses_1052_2221763=It5eNZzYnUSUG05ObXWZDmyXn2MAAAAAJAyUOYWJLV9vPOZZObFMiA==',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        data = {
            'loc': location, # 24
            'activity': '1',
            'month': month,
            'time': '',
        }

        response = self.s.post(
            'https://www.amal-nehiga.org.il/amal_rishum/base/get_all_courses.php',
            headers=headers,
            data=data,
            verify=True
        )
        data = response.json()
        return len(data) if isinstance(data, list) and len(data) > 0 else 0