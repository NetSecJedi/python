from prometheus_client import Gauge, start_http_server
import random
import time 
g = Gauge('python_test_guage', 'A test guage from Python code')
start_http_server(8000)

while True:
    g.set(random.random() * 15 - 5)
    time.sleep(5)