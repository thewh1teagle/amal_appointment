import requests
import urllib3
import schedule

# we have to use verify=False I don't care about integrity
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class watchdog:

    def __init__(self, branch, month, onAvailable) -> None:

        self.branch = branch
        self.month = month
        self.callback = onAvailable

        schedule.every(1).hours.do(self.execute)

        self.session = requests.session()

    # call this once upon creation
    def initialize(self):

        self.session.headers = {
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
        # https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests
        self.session.get(
            'https://www.amal-nehiga.org.il/amal_rishum/base/courses.php?type=1', verify=False)

    def execute(self):

        headers = {
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

        payload = {
            'loc': self.branch,  # 24
            'activity': '1',
            'month': self.month,  # 12
            'time': '',
        }

        response = self.session.post(
            'https://www.amal-nehiga.org.il/amal_rishum/base/get_all_courses.php',
            headers=headers,
            data=payload,
            verify=True
        )

        arrJson = response.json()

        available = len(arrJson) if isinstance(
            arrJson, list) and len(arrJson) > 0 else 0
        if (available > 0):
            self.callback(available, self.branch)
