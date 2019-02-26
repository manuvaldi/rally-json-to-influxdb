# rally-json-to-influxdb
Import Rally report json into Influxdb

## How to use ##
```
# python send_task_data_to_influx.py --help
usage: send_task_data_to_influx.py [-h] [-c CONFIGFILE] [-j JSONFILE]
                                   [-t TASK] [-m MEASUREMENT]

Rally Task Report JSON To Influx

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIGFILE, --configfile CONFIGFILE
                        file to read the config from
  -j JSONFILE, --jsonfile JSONFILE
                        Rally task JSON file report to import
  -t TASK, --task TASK  Rally task TAG to identify different task reports
  -m MEASUREMENT, --measurement MEASUREMENT
                        Measurement to import data

```

## Config file example ##

```
[InfluxDB]

influxdb_host=localhost
influxdb_port=8086

influxdb_db=mydata

influxdb_user=root
influxdb_pass=root
```

## Default values ##
```
CONFIGFILE = ./rallyjson2influx.config

JSONFILE = ./report.json

TASK = "default"

MEASUREMENT = "rally_task"
```
