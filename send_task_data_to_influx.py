#!/usr/bin/env python
"""Import Rally report JSON into Influxdb"""


import argparse
from datetime import datetime
import json
import ConfigParser
import os.path
from influxdb import InfluxDBClient


def parse_and_send_to_influx(config, jsonfile, measurement, task_tag):
    """Parse JSON and Send to InfluxDb function"""

    INFLUXDB_HOST = config.get('InfluxDB', 'influxdb_host')
    INFLUXDB_PORT = int(config.get('InfluxDB', 'influxdb_port'))
    INFLUXDB_DATABASE = config.get('InfluxDB', 'influxdb_db')
    INFLUXDB_USER = config.get('InfluxDB', 'influxdb_user')
    INFLUXDB_PWD = config.get('InfluxDB', 'influxdb_pass')

    json_output = None
    influx_objects = []

    # Check if config file exists
    if not os.path.isfile(jsonfile):
        print " * ERROR: JSON file file doesn't exist"
        parser.print_help()
        exit(1)
    else:
        try:
            json_output = json.load(open(jsonfile))
        except ValueError:
            print 'JSON syntax error'
            exit(1)

    if json_output:
        for task in json_output:

            for result in task["result"]:
                influx_object = dict()
                influx_object['measurement'] = measurement
                influx_object['tags'] = {
                    'task_id': task_tag,
                    'scenario': task['key']['name']
                }

                influx_object['time'] = \
                    datetime.strptime(task['created_at'], '%Y-%d-%mT%H:%M:%S')

                influx_object['fields'] = {
                    'load_duration': float(task['load_duration']),
                    'full_duration': float(task['full_duration']),
                    'success': int((result['error'].__len__()) > 0)
                }

                influx_objects.append(influx_object)

        influx_c = InfluxDBClient(INFLUXDB_HOST,
                                  INFLUXDB_PORT,
                                  INFLUXDB_USER,
                                  INFLUXDB_PWD,
                                  INFLUXDB_DATABASE)
        influx_c.write_points(influx_objects)

        return 'Results written'

    return 'No json data'


def main(args):
    """Main function"""

    config_parser = ConfigParser.RawConfigParser()

    # Check if config file exists
    if not os.path.isfile(args['configfile']):
        print " * ERROR: config file doesn't exist"
        parser.print_help()
        exit(1)

    # Read config
    config_parser.read(args['configfile'])
    json_file = args['jsonfile']
    measurement = args['measurement']
    task_tag = args['task']

    parse_and_send_to_influx(config_parser, json_file, measurement, task_tag)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Rally Task Report JSON To "
                                     " Influx")
    parser.add_argument('-c', '--configfile',
                        default="./rallyjson2influx.config",
                        help='file to read the config from')
    parser.add_argument('-j', '--jsonfile',
                        default="./report.json",
                        help='Rally task JSON file report to import')
    parser.add_argument('-t', '--task',
                        default="default",
                        help='Rally task TAG to identify different task '
                        'reports')
    parser.add_argument('-m', '--measurement',
                        default="rally_task",
                        help='Measurement to import data')

    arguments = vars(parser.parse_args())
    main(arguments)
