<div align="center">

# 🚀 DevOps Uptime Monitor

### Cloud-Based Uptime Monitoring Platform with CI/CD, Docker, Jenkins, Azure, Nginx, SSL, and Terraform

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=for-the-badge\&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge\&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge\&logo=docker)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red?style=for-the-badge\&logo=jenkins)
![Azure](https://img.shields.io/badge/Azure-Cloud%20Deployment-0078D4?style=for-the-badge\&logo=microsoftazure)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?style=for-the-badge\&logo=terraform)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-green?style=for-the-badge\&logo=nginx)

</div>

---



## 📌 Project Overview

**DevOps Uptime Monitor** is a cloud-based web application designed to monitor website availability and display service health information in a simple dashboard.

The system checks whether a given website is reachable, captures the HTTP status code, measures response time, and stores monitoring results in a PostgreSQL database. It also includes scheduled monitoring and email alert configuration for service status changes.

The application is containerized with Docker, deployed on an Azure Linux VM, served through Nginx, secured with HTTPS, and automated using a Jenkins CI/CD pipeline.

---

## 🌐 Live Demo

> The live demo may be unavailable when the Azure VM is deallocated to reduce cloud costs.

| Service          | URL                                     |
| ---------------- | --------------------------------------- |
| Live Application | `https://up-monitor.duckdns.org`        |
| Health Endpoint  | `https://up-monitor.duckdns.org/health` |

Expected health response:

```json
{
  "service": "DevOps Uptime Monitor",
  "status": "healthy"
}
```

---

## ✨ Features

* Website uptime checking
* HTTP status code detection
* Response time measurement
* Monitoring result history
* PostgreSQL database integration
* Scheduled background monitoring
* Email alert configuration support
* Flask dashboard interface
* Health check endpoint
* Dockerized application
* Docker Compose multi-container setup
* Docker Hub image publishing
* Jenkins CI/CD pipeline
* Automated testing with Pytest
* Azure VM cloud deployment
* Nginx reverse proxy
* HTTPS with Certbot SSL
* DuckDNS domain setup
* Terraform Infrastructure as Code

---

## 🛠️ Tech Stack

### Application

| Technology       | Purpose                      |
| ---------------- | ---------------------------- |
| Python           | Backend programming language |
| Flask            | Web framework                |
| Flask-SQLAlchemy | ORM and database integration |
| PostgreSQL       | Relational database          |
| HTML / CSS       | Frontend interface           |
| Jinja2           | Flask templating             |

### DevOps / Cloud

| Technology     | Purpose                                |
| -------------- | -------------------------------------- |
| Git & GitHub   | Version control and repository hosting |
| Docker         | Application containerization           |
| Docker Compose | Multi-container orchestration          |
| Docker Hub     | Container image registry               |
| Jenkins        | CI/CD automation                       |
| Azure VM       | Cloud hosting                          |
| Nginx          | Reverse proxy                          |
| Certbot        | SSL certificate management             |
| DuckDNS        | Free domain/DNS                        |
| Terraform      | Infrastructure as Code                 |

### Testing

| Tool              | Purpose               |
| ----------------- | --------------------- |
| Pytest            | Automated testing     |
| Flask Test Client | Route testing         |
| Requests Mocking  | Website check testing |

---

## 🏗️ System Architecture

```text
User Browser
     |
     v
DuckDNS Domain
     |
     v
Nginx Reverse Proxy + HTTPS
     |
     v
Dockerized Flask Application
     |
     v
PostgreSQL Database
```

---

## 🔁 CI/CD Pipeline Workflow

```text
GitHub Development Branch
        |
        v
Jenkins Pipeline Trigger
        |
        v
Install Dependencies
        |
        v
Run Automated Tests
        |
        v
Build Docker Image
        |
        v
Push Image to Docker Hub
        |
        v
SSH into Azure VM
        |
        v
Pull Latest Docker Image
        |
        v
Restart Production Containers
        |
        v
Verify Live Deployment
```

---

## 📂 Project Structure

```text
devops-uptime-monitor/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── extensions.py
│   ├── models.py
│   ├── scheduler.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── monitor_service.py
│   │   └── email_service.py
│   ├── templates/
│   │   ├── base.html
│   │   └── dashboard.html
│   └── static/
│       └── css/
│           └── style.css
│
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_monitor_service.py
│   └── test_database.py
│
├── jenkins/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
│
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── Jenkinsfile
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root.

Example:

```env
POSTGRES_DB=uptime_db
POSTGRES_USER=uptime_user
POSTGRES_PASSWORD=change_this_password
DATABASE_URL=postgresql+psycopg2://uptime_user:change_this_password@postgres:5432/uptime_db
APP_PORT=5000

SCHEDULER_ENABLED=true
CHECK_INTERVAL_MINUTES=5

ALERT_EMAIL_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_FROM_EMAIL=your_email@gmail.com
ALERT_TO_EMAIL=receiver_email@gmail.com
```


---

## 🚀 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SinaliMarasinghe25/devops-uptime-monitor.git
cd devops-uptime-monitor
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python run.py
```

Application will be available at:

```text
http://127.0.0.1:5000
```

---

## 🐳 Run with Docker Compose

Start the application with PostgreSQL:

```bash
docker compose up -d --build
```

Check containers:

```bash
docker compose ps
```

Test the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

Stop containers:

```bash
docker compose down
```

---

## 🧪 Run Tests

```bash
pytest -v
```

Expected result:

```text
10 passed
```

---

## 📦 Docker Hub Image

Docker image:

```text
sinalimarasinghe25/devops-uptime-monitor
```

Build image:

```bash
docker build -t sinalimarasinghe25/devops-uptime-monitor:latest .
```

Push image:

```bash
docker push sinalimarasinghe25/devops-uptime-monitor:latest
```

---

## ☁️ Production Deployment

The production environment uses:

* Azure Ubuntu VM
* Docker Compose
* Docker Hub image
* PostgreSQL container
* Flask application container
* Nginx reverse proxy
* DuckDNS domain
* Certbot SSL certificate

Production deployment commands:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml ps
```

Verify deployment:

```bash
curl https://up-monitor.duckdns.org/health
```

---

## 🔧 Jenkins CI/CD

The Jenkins pipeline is defined in:

```text
Jenkinsfile
```

Pipeline stages:

1. Checkout source code
2. Create Python environment
3. Install dependencies
4. Run automated tests
5. Build Docker image
6. Tag Docker image
7. Push image to Docker Hub
8. SSH into Azure VM
9. Pull latest image
10. Restart production containers
11. Verify live deployment

Required Jenkins credentials:

| Credential ID        | Purpose                         |
| -------------------- | ------------------------------- |
| `dockerhub-username` | Docker Hub username             |
| `dockerhub-token`    | Docker Hub access token         |
| `azure-vm-ssh-key`   | SSH key for Azure VM deployment |

---

## 🌍 Nginx, DNS, and SSL

Production access is handled using:

| Component | Purpose                      |
| --------- | ---------------------------- |
| DuckDNS   | Domain name                  |
| Nginx     | Reverse proxy                |
| Certbot   | HTTPS SSL certificate        |
| Azure NSG | Allow HTTP/HTTPS/SSH traffic |

The application is served securely over HTTPS:

```text
https://up-monitor.duckdns.org
```

---

## 🏗️ Terraform Infrastructure as Code

Terraform files are included in the `terraform/` directory.

Common Terraform commands:

```bash
terraform init
terraform validate
terraform plan
terraform apply
```
---

## 🌱 Branching Strategy

```text
main         → Stable release branch
development  → Active development and CI/CD branch
feature/*    → Feature branches
```

Recommended workflow:

```text
feature branch → pull request → development → pull request → main
```


---

## 📚 Key Learning Outcomes

Through this project, I gained hands-on experience in:

* Building a Flask-based monitoring application
* Integrating PostgreSQL with SQLAlchemy
* Writing and running automated tests using Pytest
* Containerizing applications using Docker
* Managing multi-container services using Docker Compose
* Creating Jenkins CI/CD pipelines
* Publishing Docker images to Docker Hub
* Deploying applications to an Azure Linux VM
* Configuring Nginx as a reverse proxy
* Securing a live application with HTTPS using Certbot
* Managing DNS using DuckDNS
* Using Terraform for Infrastructure as Code
* Handling environment variables and deployment secrets securely
* Debugging real-world CI/CD and deployment issues

---

## 📌 Project Status

```text
Completed
```

---

## 👩‍💻 Author

**Sinali Marasinghe**

GitHub: [SinaliMarasinghe25](https://github.com/SinaliMarasinghe25)

---

<div align="center">

### ⭐ If you found this project useful, feel free to star the repository.

</div>
