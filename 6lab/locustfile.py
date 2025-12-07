from locust import HttpUser, task, between
from requests.auth import HTTPBasicAuth

class OpenBMCUser(HttpUser):
    wait_time = between(3, 6)
    host = "https://172.23.199.211:2443"
    username = "root"
    password = "0penBmc"

    @task
    def get_system_info(self):
        self.client.get(
            "/redfish/v1/Systems/system",
            name="OpenBMC: System Info",
            verify=False,
            auth=HTTPBasicAuth(self.username, self.password),
            headers={"Connection": "close"}
        )

    @task
    def get_power_state(self):
        self.client.get(
            "/redfish/v1/Systems/system",
            name="OpenBMC: PowerState",
            verify=False,
            auth=HTTPBasicAuth(self.username, self.password),
            headers={"Connection": "close"}
        )

class PublicAPIUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 2)

    @task
    def get_posts(self):
        self.client.get(
            "https://jsonplaceholder.typicode.com/posts",
            name='Public API: jsonplaceholder'
            )

    @task
    def get_delayed_json(self):
        self.client.get(
            "https://httpbin.org/json",
            name="Public API: Sample JSON"
        )