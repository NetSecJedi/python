from prometheus_client import Gauge, start_http_server
import random

g = Gauge('python_test_guage', 'A test guage from Python code')
start_http_server(8000)
g.set(random.random() * 15 - 5)