from locust import HttpUser, task, between
import json


class PerformanceTests(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    @task(1)
    def test_index(self):
        res = self.client.get(f"/")
        print("response", res.json())
