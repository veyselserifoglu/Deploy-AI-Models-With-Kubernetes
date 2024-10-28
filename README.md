### End-to-End AI Model Deployment and Monitoring in Kubernetes
<!-- Tech used  -->
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326ce5?style=flat-square&logo=kubernetes&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white) 

## Project Overview

This project provides a practical demonstration of deploying an AI model using Kubernetes and monitoring its performance in real-time with Prometheus and Grafana. The setup showcases containerized deployment, metric collection, and visualization, making it suitable for production-level insights and management.

## Key Components
- FastAPI: Serves the AI model for inference requests.
- Docker: Rrunning the FastAPI application in containers.
- Kubernetes: Manages the containerized application, providing scalability and reliability.
- Prometheus: Collects performance metrics, including custom metrics from the FastAPI application.
- Grafana: Visualizes real-time metrics from Prometheus, enabling comprehensive monitoring of the AI model’s performance.


## Model Information

The AI model used for this demonstration is [deit-base-distilled-patch16-224](https://huggingface.co/facebook/deit-base-distilled-patch16-224) by Meta, a distilled vision transformer model optimized for efficient image classification tasks.


Mention what this outline won't provide. 

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Prometheus to Scrape Application Metrics](#prometheus-to-scrape-application-metrics)
- [Setting up Grafana to Visualize Prometheus Data](#setting-up-grafana-to-visualize-prometheus-data)
- [Setting up Alerts](#setting-up-alerts)


## Prerequisites
- Docker
- Helm
- Kubernetes (Minikube or any K8s cluster)
- Prometheus & Grafana
- Python 3.x

## Project Structure
- `src/`: Contains the AI model inference code (e.g., `app.py`).
- `k8s/`: Contains Kubernetes deployment and service YAML files.
- `Dockerfile`: Docker configuration for containerizing the AI model.
- `README.md`: Instructions for setting up and deploying the project.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/veyselserifoglu/Deploy-AI-Models-With-Kubernetes.git
cd Deploy-AI-Models-With-Kubernetes
```

### 2. Install Prerequisites
- Install [Docker](https://docs.docker.com/engine/install/ubuntu/).
- Install [Minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download).
- Install [Kubernetes](https://kubernetes.io/releases/download/).
- Install [Helm](https://helm.sh/docs/intro/install/).

### 3. Minikube Commands
Check all minikube commands from [here](https://minikube.sigs.k8s.io/docs/commands/):
```bash
# version
minikube version

# Start
Minikube start

# Stop
Minikube stop
```

### 4. Build Docker Image

#### 1. Deploy to Minikube environment:
If Minikube is running successfully, ensure Docker is using Minikube’s environment:

```bash
# Change the docker environment
eval $(minikube docker-env)
```

#### 2. Build docker image:
```bash
docker build -t deploy-ai-models-with-kubernetes-app:latest .
```

#### 3. Deploy to Kubernetes: 
```bash
kubectl apply -f k8s/fastapi_app/deployment.yaml
kubectl apply -f k8s/fastapi_app/service.yaml
```

### 5. Configure Monitoring with Prometheus and Grafana

#### 1. Install Prometheus:
```bash 
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus
```

#### 2. Deploy Prometheus
```bash
kubectl apply -f k8s/prometheus/prometheus-deployment.yaml
kubectl apply -f k8s/prometheus/prometheus-service.yaml
kubectl apply -f k8s/prometheus/prometheus-config.yaml
```

#### 3. Install Grafana
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana grafana/grafana
```

#### 4. Deploy Grafana
```bash
kubectl apply -f k8s/grafana/grafana-deployment.yaml
kubectl apply -f k8s/grafana/grafana-service.yaml
```

#### 5. Access Prometheus & Grafana
```bash
minikube service prometheus-service --url # To access prometheus URL.
minikube service grafana-service --url # To access grafana URL.
```

### 6. Verify Kubernetes pods
Run the following command:
```bash
kubectl get pods
```
All FastAPI, Prometheus and Grafana pods should show a status of Running. 

![kubernetes_pods](/static/images/kubernetes_pods.png)

#### Debug the pods
In case a pod is pending or failing, you can always check the logs

```bash
kubectl logs <pod-name>
```

## Prometheus to Scrape Application Metrics
In order to monitoring a specific application (e.g., FastAPI), we'll need to update the Prometheus scrape configuration to include the application’s info/metrics endpoint. 

<b>Note:</b> The script is already written, no need to do anything from your side.

#### 1. Setting up Scraping jobs:
Here, we are setting a job for prometheus to scrape matrics from the FastAPI application. 
```bash
scrape_configs:
    - job_name: 'fastapi-app'
    static_configs:
        - targets: ['fastapi-service:8000']  # Replace with FastAPI service name and port
    metrics_path: info/metrics  # Path to scrape metrics from FastAPI
```

And here, we are setting a new job to scrape data from the kubernets cluster such as CPU and Memory usage

```bash
scrape_configs:
    - job_name: 'node'
    static_configs:
        - targets: ['prometheus-prometheus-node-exporter:9100','prometheus-kube-state-metrics:8080','kube-state-metrics:8080']
```

#### 2. Jobs Demo
Here are the jobs which we defined in the prometheus-config.yaml.

![kubernetes_pods](/static/images/prometheus_jobs.png)

#### 3. Matrics Demo
Here is a snippet showing the memory usage by the node. 

![kubernetes_pods](/static/images/node_memory_usage.png)

## Setting up Grafana to Visualize Prometheus data
Grafana supports querying Prometheus, using the default port http://localhost:3000, and the default login credentials "admin" / "admin". [Official guide to connect both frameworks](https://prometheus.io/docs/visualization/grafana/).


#### 1. Grafana Dashboards:
Import Pre-built Dashboards, as Grafana has many community dashboards for Prometheus metrics, Node Exporter, Kubernetes, etc.

In this project, we are using the [Node Exporter](https://grafana.com/grafana/dashboards/1860-node-exporter-full/) dashboard. 

![kubernetes_pods](/static/images/grafana_visualization.png)

#### 2. Customize Dashboards
We can create custom panels to display specific metrics, with regard to the FastAPI applications such as:

- API response time. 
- File sizes. 
- Average response time. 

## Setting up Alerts 
