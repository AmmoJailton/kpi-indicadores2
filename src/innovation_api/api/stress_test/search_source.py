import random

from locust import HttpUser, between, task

searches = [
    {"query": "O que é regularidade do sono?", "k": 100},
    {"query": "Eficiência do sono", "k": 100},
    {"query": "Latencia do sono", "k": 100},
    {"query": "Insônia", "k": 100},
    {"query": "Viajei e dormi mal o que fazer?", "k": 100},
    {"query": "Como dormir melhor?", "k": 100},
    {"query": "Quais são as sindromes do sono?", "k": 100},
]


class AppUser(HttpUser):
    wait_time = between(2, 5)

    @task
    def search(self):
        body = random.choice(searches)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.client.post("/search/source/", json=body, headers=headers)
