from prometheus_client import Guage, start_http_server
import random

g = Guage('python_test_guage', 'A test guage from Python code')
start_http_server(8000)
g.Set(random.random() * 15 - 5)