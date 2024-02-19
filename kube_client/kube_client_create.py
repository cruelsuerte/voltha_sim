from kubernetes import client, config
from kubernetes.client.rest import ApiException

def create_namespace(namespace):

    CoreV1 = client.CoreV1Api()

    try:
        existing_namespace = CoreV1.read_namespace(name=namespace)
        print(f"Namespace '{namespace}' already exists.")
    except ApiException as e:
        if e.status == 404:
            namespace = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
            CoreV1.create_namespace(body=namespace)
            print(f"Namespace '{namespace}' created successfully.")
        else:
            print(f"Error during namespace read/creation: {e}")

def create_deployment(namespace, deployment):

    AppsV1 = client.AppsV1Api()

    try:
        existing_deployment = AppsV1.read_namespaced_deployment(name=deployment, namespace=namespace)
        print(f"Deployment '{deployment}' already exists in namespace '{namespace}'.")
    except ApiException as e:
        if e.status == 404:
            deployment = client.V1Deployment(
                api_version="apps/v1",
                kind="Deployment",
                metadata=client.V1ObjectMeta(name=deployment, namespace=namespace),
                spec=client.V1DeploymentSpec(
                    replicas=1,
                    selector=client.V1LabelSelector(match_labels={"app": deployment}),
                    template=client.V1PodTemplateSpec(
                        metadata=client.V1ObjectMeta(labels={"app": deployment}),
                        spec=client.V1PodSpec(
                            containers=[
                                client.V1Container(
                                    name=deployment,
                                    image="gcr.io/google-samples/hello-app:1.0",
                                )
                            ]
                        )
                    )
                )
            )
            AppsV1.create_namespaced_deployment(body=deployment, namespace=namespace)
            print(f"Deployment '{deployment}' created successfully in namespace '{namespace}'.")
        else:
            print(f"Error during deployment read/creation: {e}")

def expose_deployment(namespace, deployment, service_type):

    CoreV1 = client.CoreV1Api()

    try:
        existing_service = CoreV1.read_namespaced_service(name=deployment, namespace=namespace)
        print(f"Service '{deployment}' already exists in namespace '{namespace}'.")
    except ApiException as e:
        if e.status == 404:
            service = client.V1Service(
                api_version="v1",
                kind="Service",
                metadata=client.V1ObjectMeta(name=deployment, namespace=namespace),
                spec=client.V1ServiceSpec(
                    selector={"app": deployment},
                    ports=[client.V1ServicePort(port=8080, target_port=8080)],
                    type=service_type
                )
            )
            CoreV1.create_namespaced_service(body=service, namespace=namespace)
            print(f"Service '{deployment}' created successfully in namespace '{namespace}'.")
        else:
            print(f"Error during service read/creation: {e}")


def create_ingress(ingress_name, service_name, namespace, domain, whitelist_source_range):
    NetworkingV1 = client.NetworkingV1Api()

    try:
        existing_ingress = NetworkingV1.read_namespaced_ingress(name=ingress_name, namespace=namespace)
        print(f"Ingress '{ingress_name}' already exists in namespace '{namespace}'.")
    except ApiException as e:
        if e.status == 404:
            ingress = client.V1Ingress(
                api_version="networking.k8s.io/v1",
                kind="Ingress",
                metadata=client.V1ObjectMeta(
                    name=ingress_name,
                    namespace=namespace,
                    annotations={
                        "nginx.ingress.kubernetes.io/rewrite-target": "/$1",
                        "nginx.ingress.kubernetes.io/whitelist-source-range": whitelist_source_range
                    }
                ),
                spec=client.V1IngressSpec(
                    rules=[
                        client.V1IngressRule(
                            host=domain,
                            http=client.V1HTTPIngressRuleValue(
                                paths=[
                                    client.V1HTTPIngressPath(
                                        path="/",
                                        path_type="Prefix",
                                        backend=client.V1IngressBackend(
                                            service=client.V1IngressServiceBackend(
                                                name=service_name,
                                                port=client.V1ServiceBackendPort(
                                                    number=8080
                                                )
                                            )
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

            NetworkingV1.create_namespaced_ingress(namespace=namespace, body=ingress)
            print(f"Ingress '{ingress_name}' created successfully in namespace '{namespace}'.")
        else:
            print(f"Error during Ingress read/creation: {e}")


def main():

    kube_config = "~/kube_client/config_remote"
    namespace = "application"
    deployment = "hello-server"
    ingress = "hello-ingress"

    config.load_kube_config(kube_config)

    create_namespace(namespace)
    create_deployment(namespace, deployment)
    expose_deployment(namespace, deployment, "NodePort")
    create_ingress(ingress, deployment, namespace, "hello.app", "172.16.110.130")

if __name__ == "__main__":
    main()