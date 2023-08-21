import ast
import gzip
import argparse
from colorama import Fore
import os
from datetime import datetime


def get_logs_from_gz(path, usecase, camera_ip, start_time, end_time, cl_name, check_cl):
    """
    describe function
    :param path:
    :param usecase:
    :param camera_ip:
    :param start_time:
    :param end_time:
    :return:
    """
    global counter
    counter = False

    try:
        with gzip.open(path, 'r') as log:
            log_file = log.read()
            logs = log_file.decode('utf-8')
        for i in logs.split('\n')[1:]:
            eve = i.split(":")
            if path.startswith('event_consumer'):
                if len(eve) > 5:
                    if eve[5].strip() == f'[{camera_ip}] [{usecase}] Received event json is':
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
                                print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase,
                                      Fore.WHITE,
                                      inf)
                            if log_time > e_time:
                                print(Fore.GREEN,
                                      "******************************** Fetching Done ***********************************")
                                exit()
            # BRU_BRU_C168_LC0012
            else:
                if len(eve) > 6:
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
                        if check_cl:
                            li = [cl[0] for cl in inf]
                        if s_time <= log_time <= e_time:
                            if check_cl and cl_name in li:
                                print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase,
                                      Fore.WHITE,
                                      inf, end=' ')
                                counter = True
                            elif not check_cl:
                                print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase,
                                      Fore.WHITE,
                                      inf)

                        if log_time > e_time:
                            print(Fore.GREEN,
                                  "******************************** Fetching Done ***********************************")
                            exit()
                    elif counter and eve[5].strip() == 'Counter':
                        print(Fore.RED, 'Counter: ', eve[-1])
                        print()
                        counter = False

        print(Fore.GREEN, "******************************** Fetching Done ***********************************")
    except Exception as e:
        print(e)


def get_logs_from_log(path, usecase, camera_ip, start_time, end_time, cl_name, check_cl):
    global counter
    counter = False
    try:
        with open(path, 'r') as log:
            log_file = log.readlines()
        for i in log_file:
            eve = i.split(":")
            if path.startswith('event_consumer'):
                if len(eve) > 5:
                    if eve[5].strip() == f'[{camera_ip}] [{usecase}] Received event json is':
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
                                print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase,
                                      Fore.WHITE,
                                      inf)
                            elif log_time > e_time:
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
                        if check_cl:
                            li = [cl[0] for cl in inf]
                        if s_time <= log_time <= e_time:
                            if check_cl and cl_name in li:
                                print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase,
                                      Fore.WHITE,
                                      inf)
                                counter = True
                            elif not check_cl:
                                print(Fore.RED, dt_time, Fore.GREEN, camera_ip, Fore.YELLOW, current_usecase,
                                      Fore.WHITE,
                                      inf)
                                counter = True
                        if log_time > e_time:
                            print(Fore.GREEN,
                                  "******************************** Fetching Done ***********************************")
                            exit()
                    elif counter and eve[5].strip() == 'Counter':
                        print(Fore.RED, 'Counter: ', eve[-1])
                        counter = False

        print(Fore.GREEN, "******************************** Fetching Done ***********************************")
        exit()
    except Exception as e:
        print(e)


args = argparse.ArgumentParser()
args.add_argument('-path', '-p', type=str, required=True, help='Path to .gz log file')
args.add_argument('-event', '-eve', type=str, default='On_Block',
                  help='Give the event name ex: On_Block, Note: Give event which is in config file')
args.add_argument('-cam_ip', '-ip', type=str, required=True, help='camera ip [BRU_BRU_*]')
args.add_argument('-start_time', '-s', type=str, default='00:00:00', help='Start time')
args.add_argument('-end_time', '-e', type=str, default='23:00:00', help='End time')
args.add_argument('-class_name', '-c', type=str, default='', help='Give class to fetch the inference')
args.add_argument('-check_cl', '-cl', default=False, type=str)
args.add_argument('-counter', default=True, type=bool)

opt = args.parse_args()
log_path = opt.path
if os.path.exists(log_path):
    print(Fore.GREEN, 'File found at {}.'.format(log_path))
    print(Fore.WHITE, "Log file -> {}".format(log_path))
    confirmation = input('   Continue checking with above log file: (y/n): ')
    if confirmation == 'y' or confirmation == 'yes':
        print(Fore.GREEN, "***************************************************************************")
        print(Fore.GREEN, "***************************************************************************")
        print(Fore.YELLOW, "***********************This Script will Check the logs*********************")
        print(Fore.GREEN, "***************************************************************************")
        print(Fore.GREEN, "***************************************************************************")
        if log_path.endswith('.log'):
            get_logs_from_log(log_path, opt.event, opt.cam_ip, opt.start_time, opt.end_time, opt.class_name,
                              opt.check_cl)
        elif log_path.endswith('.gz'):
            get_logs_from_gz(log_path, opt.event, opt.cam_ip, opt.start_time, opt.end_time, opt.class_name,
                             opt.check_cl)
else:
    print(Fore.RED, 'File not found at {}, Please check the path.'.format(log_path))
