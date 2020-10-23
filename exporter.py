#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge, Counter
import random
import time
import obd
import sys

# Create a metric
ENGINE_LOAD         = Gauge('engine_load', 'Calculated engine load')
COOLANT_TEMP        = Gauge('coolant_temp', 'Engine coolant temperature')
SHORT_FUEL_TRIM_1   = Gauge('short_fuel_trim_1', 'Short term fuel trim Bank 1')
RPM                 = Gauge('rpm', 'Engine speed')
SPEED               = Gauge('speed', 'Vehicle speed')
RUN_TIME            = Counter('run_time', 'Run time since engine start')

commands = {
    obd.commands.ENGINE_LOAD: ENGINE_LOAD,
    obd.commands.COOLANT_TEMP: COOLANT_TEMP,
    obd.commands.SHORT_FUEL_TRIM_1: SHORT_FUEL_TRIM_1 ,
    obd.commands.RPM: RPM,
    obd.commands.SPEED: SPEED,
    obd.commands.RUN_TIME: RUN_TIME
}

def get_obd(connection):

    for cmd, prom in commands.items():
        if cmd.name.lower() == prom._name:
            response = connection.query(cmd)
            prom.set(response.value.magnitude)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    print("start server...")

    connection = obd.OBD("/dev/rfcomm1")
    if connection.status() != obd.OBDStatus.CAR_CONNECTED:
        print("ELM327 is not connected!!")
        sys.exit(1)
    else:
        print("start reading OBD2 info and export to prometheus...")

    # Generate some requests.
    while True:
        get_obd(connection)
        time.sleep(1)
