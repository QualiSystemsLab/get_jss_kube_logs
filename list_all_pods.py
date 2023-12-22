import sys
from kubernetees import client, config

env_name = 'lab'
config_file = rf"c:\kubectl_configs\{env_name}"
config.load_kube_config(config_file=config_file)

v1 = client.CoreV1Api()

pods = [i.metadata.name for i in v1.list_pod_for_all_namespaces().items]
print(pods)

services = [i.metadata.name for i in v1.list_service_for_all_namespaces().items]
print(services)
