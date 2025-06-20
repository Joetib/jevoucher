import requests
from django.conf import settings


class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"

    def verify_payment(self, ref, amount: int):
        path = "/transaction/verify/{}".format(ref)

        headers = {
            "Authorization": "Bearer {}".format(self.PAYSTACK_SECRET_KEY),
            "Content-Type": "application/json",
        }
        url = "{}{}".format(self.base_url, path)

        response = requests.get(url, headers=headers)

        print(
            "Paystack response: \n--------\n",
            response.json(),
            "\n----------",
        )
        if response.status_code == 200:
            response_data = response.json()
            if not response_data["status"]:
                return False, response_data["message"]
            data: dict = response_data["data"]
            return data["status"] == "success", data
        return False, "Payment verification failed"
