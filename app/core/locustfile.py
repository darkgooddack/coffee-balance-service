from locust import HttpUser, task, between

TOKEN = "..."

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

class BalanceUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def get_balance(self):
        self.client.get("/api/v1/balance/", headers=HEADERS)

    @task(1)
    def top_up(self):
        self.client.post(
            "/api/v1/balance/top-up",
            headers=HEADERS,
            json={"amount": 100}
        )

    @task(1)
    def pay(self):
        self.client.post(
            "/api/v1/balance/pay",
            headers=HEADERS,
            json={"amount": 50}
        )
