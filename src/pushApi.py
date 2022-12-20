import requests
import json


class pushApi:

    def send(self, topic: str, title, text, click_url):

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
