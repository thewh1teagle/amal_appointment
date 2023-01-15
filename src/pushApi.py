import requests
import json
from typing import Callable


class pushApi:

    def send(self, topic: str, title: str, text: str, click_url: Callable):

        formData = {
            "topic": topic,
            "message": text,
            "title": title,
            # "tags": ["warning","cd"],
            "priority": 0,
            # "attach": "https://filesrv.lan/space.jpg",
            # "filename": "diskspace.jpg",
            "click": click_url,
            "actions": [{"action": "view", "label": "Admin panel", "url": "https://filesrv.lan/admin"}]
        }

        requests.post("https://ntfy.sh/", data=json.dumps(formData))
