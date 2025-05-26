from typing import List
import requests
from django.conf import settings
import logging

logging.basicConfig(
    filename="sms_api.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class SmsApi:
    BASE_URL = "https://sms.textcus.com/api/send"
    API_KEY = settings.SMS_API_KEY

    def send(self, recipients: List[str], message: str, sender_id: str) -> bool:
        recipients = self.clean_recipients(recipients)
        recipients_string = ",".join(recipients)
        params = {
            "apikey": self.API_KEY,
            "destination": recipients_string,
            "message": message,
            "source": sender_id,
            "dlr": 0,
            "type": 0,
        }
        url = "https://sms.textcus.com/api/send"
        try:
            response = requests.get(url, params=params)
            response_data = response.json()
            print(response_data)
            return response_data["status"] == "0000"
        except Exception as e:
            logging.error("An error occurred: %s", e)
            logging.error("Response content: %s", response.content)
            raise e

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
