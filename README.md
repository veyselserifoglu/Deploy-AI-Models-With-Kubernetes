# AI Model Deployment and Monitoring with Kubernetes, Prometheus, and Grafana

This project demonstrates how to deploy an AI model using Kubernetes and monitor its performance with Prometheus and Grafana.

## Prerequisites
- Docker
- Kubernetes (Minikube or any K8s cluster)
- Helm
- Prometheus & Grafana
- Python 3.x

## Project Structure
- `src/`: Contains the AI model inference code (e.g., `app.py`).
- `k8s/`: Contains Kubernetes deployment and service YAML files.
- `helm-charts/`: Helm charts for deploying Prometheus and Grafana (optional if using Helm).
- `Dockerfile`: Docker configuration for containerizing the AI model.
- `README.md`: Instructions for setting up and deploying the project.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-k8s-monitoring.git
cd ai-k8s-monitoring