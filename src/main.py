from AmalApi import AmalApi, locations, months
from Push import Push
import schedule
import time
import settings
import datetime

api = AmalApi()
push = Push()

def job():
    try:
        print('Job run', datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        for city in settings.CITIES:
            appointmens = api.available_appointment(city, months[-1])
            if appointmens > 0:
                push.send(settings.TOPIC ,"New Appointment", f"Wow! There's new {appointmens} in {city.name} available!", "https://www.amal-nehiga.org.il/amal_rishum/base/courses.php?type=1")
                print('Push...\nhanging for 30 minutes...')
                time.sleep(60*30) # 30 minutes
    except Exception as e:
        print(f'We got error :( {e}')
        push.send(settings.TOPIC, "Error", e, "")

if __name__ == '__main__':  
    print('Starting')
    job()
    schedule.every(settings.SCHEDULE_INTEVAL).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)