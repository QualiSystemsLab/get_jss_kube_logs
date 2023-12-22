import argparse
import sys

from kube_helpers import get_kube_api, create_output_folder, get_kube_logs


def main(config_file, logs_reqiured, path, duration):
    api = get_kube_api(config_file)
    all_pods = api.list_pod_for_all_namespaces(watch=False)
    filepath = create_output_folder(path=path)
    print(f'Output folder: {filepath}')
    get_kube_logs(api, all_pods, logs_required, duration, filepath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python main.py', description='Kube Log collector',
                                     add_help=True)
    parser.add_argument('-d', '--duration', help='Duration in Hours', default="1", required=False)
    parser.add_argument('-e', '--environment', help='Environment Name, corresponding to the k8s config file name', default="local", required=False)
    parser.add_argument('-o', '--out_folder', help='Output folder', default=None, required=False)

    args = parser.parse_args()
    configuration = args.environment
    output_folder = args.out_folder
    duration = int(args.duration)

    config_file = f'c:/kubectl_configs/{configuration}'
    logs_required = (
        'robot-test-discovery-service-',
        'job-scheduling-portal-',
        'job-scheduling-service-',
        'sandbox-service-',
        'robot-test-execution-service-',
        'cloudshell-rabbitmq-'
    )
    main(config_file, logs_required, output_folder=output_folder, duration=duration)
