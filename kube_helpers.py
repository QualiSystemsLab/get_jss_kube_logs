import os
import time

from kubernetes import client, config


def get_all_pods(api, logs_required):
    all_pod_names = list()
    all_pods = api.list_pod_for_all_namespaces(watch=False)
    for i in all_pods.items:
        pod_name = i.metadata.name
        for pod in logs_required:
            if pod_name.startswith(pod):
                all_pod_names.append(pod_name)
    return all_pod_names


def get_logs(api, pod_name, duration=24):
    logs = api.read_namespaced_pod_log(name=pod_name, namespace='default', since_seconds=3600 * duration)
    return logs


def create_output_folder(filepath=None):
    curr_time = time.strftime('%y%m%d%H%M')
    if not filepath:
        filepath = f'c:/temp'
    if filepath.endswith('/'):
        filepath = filepath.rstrip('/')
    filepath = f'{filepath}/Logs_{curr_time}'
    print(f'Logs folder: {filepath}')
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    return filepath


def write_log_to_file(logs, filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))

    with open(filename, 'w') as f:
        print(logs, file=f)


def get_kube_api(config_file):
    config.load_kube_config(config_file=config_file)
    v1 = client.CoreV1Api()
    return v1


def get_kube_logs(v1, all_pods, logs_required, DURATION, filepath):
    for i in all_pods.items:
        pod_name = i.metadata.name
        for pod in logs_required:
            if pod_name.startswith(pod):
                curr_time = time.strftime('%y%m%d%H%M')
                logs = v1.read_namespaced_pod_log(
                    name=pod_name, namespace='default', since_seconds=3600 * DURATION
                )
                filename = ''.join([w[0] for w in pod_name.split('-')])
                filename = f'{filepath}/{filename}_{curr_time}.log'
                write_log_to_file(logs, filename)

