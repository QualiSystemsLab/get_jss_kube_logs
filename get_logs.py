from kubernetes.client.rest import ApiException
from kubernetes import client, config

env_name = 'lab'
config.load_kube_config(rf'c:/kubectl_configs/{env_name}')
pod_name = 'cloudshell-rabbitmq-0'

try:
    api_instance = client.CoreV1Api()
    api_response = api_instance.read_namespaced_pod_log(name=pod_name, namespace='default')
    print(api_response)
except ApiException as e:
    print(f'Found exception in reading the logs')
