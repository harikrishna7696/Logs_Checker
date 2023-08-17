import ast
import gzip
import argparse
from colorama import Fore
import os
from datetime import datetime


def get_logs_from_gz(path, usecase, camera_ip, start_time, end_time):
    with gzip.open(path, 'r') as log:
        log_file = log.read()
        logs = log_file.decode('utf-8')
    for i in logs.split('\n')[1:]:
        eve = i.split(":")
        # print(eve)
        if path.startswith('event_consumer'):
            if len(eve) > 5:
                if eve[5].strip() == 'Received event json is':
                    d = i.split('Received event json is')[1][2:].strip()
                    data_dict = ast.literal_eval(d)
                    dt_time = data_dict['datetime'].split('.')[0]
                    camera = data_dict['camera']
                    inf = data_dict['inf_op']
                    current_usecase = data_dict['current_usecase']
                    res = camera_ip == camera and usecase == current_usecase
                    if res:
                        format_str = "%Y-%m-%d %H:%M:%S"
                        time_fmt = "%H:%M:%S"
                        converted_log_datetime = datetime.strptime(dt_time, format_str)
                        converted_start_time = datetime.strptime(start_time, time_fmt)
                        converted_end_time = datetime.strptime(end_time, time_fmt)
                        log_time = converted_log_datetime.time()
                        s_time = converted_start_time.time()
                        e_time = converted_end_time.time()

                        if s_time <= log_time <= e_time:
                            print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase, Fore.BLUE,
                                  inf)
                        else:
                            print(Fore.GREEN,
                                  "******************************** Fetching Done ***********************************")
                            exit()
        # BRU_BRU_C168_LC0012
        else:
            if len(eve) > 7:
                if eve[5].strip() == f'[{camera_ip}] Received data json is':
                    d = i.split(f'[{camera_ip}] Received data json is')[1][2:].strip()
                    data_dict = ast.literal_eval(d)
                    dt_time = data_dict['datetime'].split('.')[0]
                    inf = data_dict['inf_op']
                    current_usecase = data_dict['current_usecase']
                    format_str = "%Y-%m-%d %H:%M:%S"
                    time_fmt = "%H:%M:%S"
                    converted_log_datetime = datetime.strptime(dt_time, format_str)
                    converted_start_time = datetime.strptime(start_time, time_fmt)
                    converted_end_time = datetime.strptime(end_time, time_fmt)
                    log_time = converted_log_datetime.time()
                    s_time = converted_start_time.time()
                    e_time = converted_end_time.time()

                    if s_time <= log_time <= e_time:
                        print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase, Fore.BLUE,
                              inf)
                    else:
                        print(Fore.GREEN, "******************************** Fetching Done ***********************************")
                        exit()


def get_logs_from_log(path, usecase, camera_ip, start_time, end_time):
    print(path)
    with open(path, 'r') as log:
        log_file = log.readlines()
    for i in log_file:
        eve = i.split(":")
        if path.startswith('event_consumer'):
            if len(eve) > 5:
                if eve[5].strip() == 'Received event json is':
                    d = i.split('Received event json is')[1][2:].strip()
                    data_dict = ast.literal_eval(d)
                    dt_time = data_dict['datetime'].split('.')[0]
                    camera = data_dict['camera']
                    inf = data_dict['inf_op']
                    current_usecase = data_dict['current_usecase']
                    res = camera_ip == camera and usecase == current_usecase
                    if res:
                        format_str = "%Y-%m-%d %H:%M:%S"
                        time_fmt = "%H:%M:%S"
                        converted_log_datetime = datetime.strptime(dt_time, format_str)
                        converted_start_time = datetime.strptime(start_time, time_fmt)
                        converted_end_time = datetime.strptime(end_time, time_fmt)
                        log_time = converted_log_datetime.time()
                        s_time = converted_start_time.time()
                        e_time = converted_end_time.time()

                        if s_time <= log_time <= e_time:
                            print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase, Fore.BLUE,
                                  inf)
                        else:
                            print(Fore.GREEN,
                                  "******************************** Fetching Done ***********************************")
                            exit()
        else:
            if len(eve) > 7:
                if eve[5].strip() == f'[{camera_ip}] Received data json is':
                    d = i.split(f'[{camera_ip}] Received data json is')[1][2:].strip()
                    data_dict = ast.literal_eval(d)
                    dt_time = data_dict['datetime'].split('.')[0]
                    format_str = "%Y-%m-%d %H:%M:%S"
                    time_fmt = "%H:%M:%S"
                    inf = data_dict['inf_op']
                    converted_log_datetime = datetime.strptime(dt_time, format_str)
                    converted_start_time = datetime.strptime(start_time, time_fmt)
                    converted_end_time = datetime.strptime(end_time, time_fmt)
                    log_time = converted_log_datetime.time()
                    s_time = converted_start_time.time()
                    e_time = converted_end_time.time()
                    current_usecase = data_dict['current_usecase']
                    if s_time <= log_time <= e_time:
                        print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase, Fore.BLUE,
                              inf)
                    else:
                        print(Fore.GREEN,
                              "******************************** Fetching Done ***********************************")
                        exit()


args = argparse.ArgumentParser()
args.add_argument('-path', '-p', type=str, required=True, help='Path to .gz log file')
args.add_argument('-event', '-e', type=str, required=True,
                  help='Give the event name ex: On_Block, Note: Give event which is in config file')
args.add_argument('-cam_ip', '-ip', type=str, required=True, help='camera ip [BRU_BRU_*]')
args.add_argument('-start_time', type=str, default='07:00:00', help='Start time')
args.add_argument('-end_time', type=str, default='10:00:00', help='End time')

opt = args.parse_args()
path = opt.path
if os.path.exists(path):
    print(Fore.GREEN, 'File found at {}.'.format(path))
    print(Fore.BLUE, "Log file -> {}".format(path))
    confirmation = input('   Continue checking with above log file: (y/n): ')
    if confirmation == 'y' or confirmation == 'yes':
        print(Fore.GREEN, "***************************************************************************")
        print(Fore.GREEN, "***************************************************************************")
        print(Fore.YELLOW, "***********************This Script will Check the logs*********************")
        print(Fore.GREEN, "***************************************************************************")
        print(Fore.GREEN, "***************************************************************************")
        if path.endswith('.log'):
            get_logs_from_log(path, opt.event, opt.cam_ip, opt.start_time, opt.end_time)
        elif path.endswith('.gz'):
            get_logs_from_gz(path, opt.event, opt.cam_ip, opt.start_time, opt.end_time)
else:
    print(Fore.RED, 'File not found at {}, Please check the path.'.format(path))
