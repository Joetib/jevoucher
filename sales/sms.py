import json
from typing import List
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SmsApi:
    BASE_URL = "https://apps.mnotify.net/smsapi"
    API_KEY = settings.SMS_API_KEY

    def send(self, recipients: List[str], message: str, sender_id: str) -> bool:
        recipients = self.clean_recipients(recipients)
        recipients_string = ",".join(recipients)

        data = {
            "destination": recipients_string,
            "source": sender_id,
            "dlr": 0,
            "type": 0,
            "message": message,
        }
        data = {
            "key": self.API_KEY,
            "to": recipients_string,
            "msg": message,
            "sender_id": sender_id,
        }

        headers = {
            "Authorization": f"Bearer {self.API_KEY}",  # Replace 'API_KEY' with your actual API Key
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(
                self.BASE_URL, params=data, headers=headers, timeout=30
            )

            response.raise_for_status()
            print(response.json())
            return True
        except Exception as e:
            logger.error("An error occurred: %s", e)
            logger.error("Response content: %s", response.content)
            return False

    def clean_recipients(self, recipients: List[str]) -> List[str]:
        cleaned_list: List[str] = []
        for number in recipients:
            if len(number) < 10:
                cleaned_number = "".join(["233", number])
            elif len(number) == 10:
                cleaned_number = "".join(["233", number[1:]])
            else:
                cleaned_number = number
            cleaned_list.append(cleaned_number)
        return cleaned_list
