from watchdog import watchdog
from pushApi import pushApi

import dotenv
import schedule
import time
import os


# this is a callback that gets called when there's an appointment available
def on_available(cnt, cname):
    push.send(
        "AMAL_APPOINTMENT",
        "New Appointment",
        f"Wow! There's new {cnt} in {cname} available!",
        "https://www.amal-nehiga.org.il/amal_rishum/base/courses.php?type=1"
    )


if __name__ == '__main__':
    dotenv.load_dotenv()

    branch = os.environ.get('branch')
    month = os.environ.get('month')

    watchdog = watchdog(branch, month, on_available)
    push = pushApi()

    print('Starting')

    watchdog.initialize()
    watchdog.execute()  # initial execution

    while True:
        schedule.run_pending()
        time.sleep(1)
