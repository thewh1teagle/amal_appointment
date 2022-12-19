from AmalApi import locations, Location
from typing import List

SCHEDULE_INTEVAL = 1 # every 1 hour
TOPIC = "AMAL_APPOINTMENT"
CITIES: List[Location] = [
    next(l for l in locations if l.name == 'jerusalem_beit_hanina'), # jerusalem_beit_hanina
    next(l for l in locations if l.name == 'jerusalem_new_city') # jerusalem_nayot
]