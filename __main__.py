"""A Kubernetes Python Pulumi program"""
#https://www.pulumi.com/docs/get-started/kubernetes/modify-program/

import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts

app_name = "hello-k8s"
app_labels = { "app" : "hello-k8s" }

deployment = Deployment(
    "hello-k8s",
    spec={
        "selector": { "match_labels": app_labels },
        "replicas": 1,
        "template": {
            "metadata": { "labels": app_labels },
            "spec": { "containers": [{ "name": "hello-k8s", "image": "chrisley75/hello-kubernetes:v1", "env": [{ "name": "MESSAGE", "value": "Application deployee et geree avec Pulumi"}] }] }
        }
    })


frontend = Service(
    app_name,
    metadata={
        "labels": deployment.spec["template"]["metadata"]["labels"],
    },
    spec={
        "type": "LoadBalancer",
        "ports": [{ "port": 80, "target_port": 8080, "protocol": "TCP" }],
        "selector": app_labels,
    })

pulumi.export("name", deployment.metadata["name"])
