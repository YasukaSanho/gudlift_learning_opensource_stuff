from locust import HttpUser, task

class ProjetPerfTest(HttpUser):

    @task
    def login(self):
        self.client.post("/showSummary", data={"email":"john@simplylift.co"})

    @task
    def clubs(self):
        self.client.get('/clubsDetails')