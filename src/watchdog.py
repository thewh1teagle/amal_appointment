import requests
import urllib3
import schedule
from array import array
from typing import Callable

# we have to use verify=False I don't care about integrity
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class watchdog:

    def __init__(self, branches: array, months: array, on_available: Callable) -> None:

        # data from outer class
        self.branches = branches
        self.months = months
        self.callback = on_available

        # internal use
        self.branch_index = 0
        self.branches_len = len(branches)
        self.month_index = 0
        self.months_len = len(months)

        schedule.every(6).seconds.do(self.execute)

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

        branch = self.branches[self.branch_index]
        month = self.months[self.month_index]

        # print(f'month {month} branch {branch}')

        payload = {
            'loc': branch,
            'activity': '1',
            'month': month,
            'time': '',
        }

        response = self.session.post(
            'https://www.amal-nehiga.org.il/amal_rishum/base/get_all_courses.php',
            headers=headers,
            data=payload,
            verify=True
        )

        arr_json = response.json()

        available = len(arr_json) if isinstance(
            arr_json, list) and len(arr_json) > 0 else 0

        # print(available)

        if (available):
            self.callback(available, self.branch)
        #   return  # remove this if you want to iterate to next month/branch when a date is found

        if (self.months_len > 1):

            if (self.month_index == self.months_len - 1):
                self.month_index = 0  # if we reached the max amount of months, we reset the index

                # when we checked all months for current branch, we iterate to next branch
                if (self.branches_len > 1):

                    if (self.branch_index == self.branches_len - 1):
                        # we reset back to the first branch
                        self.branch_index = 0
                        return

                    self.branch_index += 1

                return

            # we iterate to next month in the array
            self.month_index += 1
