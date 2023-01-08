from __future__ import annotations

import prometheus_client as pc
import time
import socket

from .metrics import * 

from bagbag import *

class PushGateway():
    def __init__(self, address:str, job:str, pushinterval:int=15, instance:str=None):
        self.job = job 
        self.instance = instance if instance != None else socket.gethostname()
        self.address = address 
        self.registry = pc.CollectorRegistry()
        self.pushinterval = pushinterval

        if not self.address.startswith("http://") or not self.address.startswith("https://"):
            self.address = 'https://' + self.address 
        
        self.address = self.address + f"/metrics/job/{self.job}/instance/{self.instance}"
        
        Thread(self.run)
    
    def run(self):
        rl = Tools.RateLimit(str(int(3600/self.pushinterval)) + "/h")
        while True:
            rl.Take()
            data = pc.generate_latest(self.registry)
            while True:
                try:
                    Http.PutRaw(self.address, data, TimeoutRetryTimes=9999)
                    break 
                except:
                    pass 
        
    def NewCounter(self, name:str, help:str) -> PrometheusCounter:
        return PrometheusCounter(name, help, self.registry)
    
    def NewCounterWithLabel(self, name:str, labels:list[str], help:str) -> PrometheusCounterVec:
        return PrometheusCounterVec(name, labels, help, self.registry)
    
    def NewGauge(self, name:str, help:str) -> PrometheusGauge:
        return PrometheusGauge(name, help, self.registry)
    
    def NewGaugeWithLabel(self, name:str, labels:list[str], help:str) -> PrometheusGaugeVec:
        return PrometheusGaugeVec(name, labels, help, self.registry)

if __name__ == "__main__":
    import time
    import random

    p = PushGateway("pushgateway.example.com", "test_job")
    c = p.NewCounterWithLabel(
        "test_counter", 
        ["label1", "label2"], # Two labels, will display with this order
        "test counter metric"
    )
    g = p.NewGaugeWithLabel(
        "test_gauge", 
        ["label1", "label2"], # Two labels, will display with this order
        "test gauge metric"
    )
    while True:
        c.Add({"label2": "value2", "label1": "value1"}) # Order is not matter
        c.Add(["l3", "l4"])
        c.Add(["l5"]) # Will be "l5" and ""
        c.Add(["l6", "l7", "l8"]) # Will be "l7" and "l8"
        g.Set(["l6", "l7", "l8"], random.randint(0, 100))
        time.sleep(1)