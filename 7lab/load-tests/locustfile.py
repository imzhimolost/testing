from locust import HttpUser, task, between

class BMCUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://localhost:2443"
    default_headers = {"Content-Type": "application/json"}

    def on_start(self):
        self.client.verify = False
        self.client.post(
            "/login",
            json={"username": "root", "password": "0penBmc"}
        )

    @task(3)
    def get_redfish_root(self):
        self.client.get("/redfish/v1")

    @task(2)
    def get_bmc_info(self):
        self.client.get("/redfish/v1/Managers/bmc")

    @task(1)
    def get_system_status(self):
        self.client.get("/redfish/v1/Systems/system")