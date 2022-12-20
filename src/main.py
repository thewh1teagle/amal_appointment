from watchdog import watchdog
from pushApi import pushApi

import dotenv
import schedule
import time


# this is a callback that gets called when there's an appointment available
def onAvailable(cnt, cname):
    pushApi.send(
        "AMAL_APPOINTMENT",
        "New Appointment",
        f"Wow! There's new {cnt} in {cname} available!",
        "https://www.amal-nehiga.org.il/amal_rishum/base/courses.php?type=1"
    )


if __name__ == '__main__':
    dotenv.load_dotenv()

    branch = dotenv.get_key('branch')
    month = dotenv.get_key('month')

    watchdog = watchdog(branch, month, onAvailable)
    pushApi = pushApi()

    print('Starting')

    watchdog.initialize()
    watchdog.execute()  # initial execution

    while True:
        schedule.run_pending()
        time.sleep(1)
