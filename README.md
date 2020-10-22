# obd2-exporter-py
OBD2 exporter for Prometheus

# Installation

```
$ pip install obd
$ pip install prometheus_client
```

After setup ELM327 device to car.
check ELM327 bluetooth address.

```
$ sudo bluetoothctl
$ scan on
```

bind rfcomm

```
$ sudo rfcomm bind rfcomm0 xx:xx:xx:xx:xx:xx
```

start program

```
$ sudo python3 exporter.py
```

check expoter

```
$ curl localhost:8000
```
