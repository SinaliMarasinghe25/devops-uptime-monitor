pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'uptime-monitor-ci'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/python -m pip install --upgrade pip
                    venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    PYTHONPATH=$WORKSPACE venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Prepare Compose Environment') {
            steps {
                sh '''
                    cat > .env <<EOF
POSTGRES_DB=uptime_db
POSTGRES_USER=uptime_user
POSTGRES_PASSWORD=jenkins_test_password_123
DATABASE_URL=postgresql+psycopg2://uptime_user:jenkins_test_password_123@postgres:5432/uptime_db
APP_PORT=5050
POSTGRES_PORT=55432
EOF
                '''
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh '''
                    docker compose -p $COMPOSE_PROJECT_NAME config --quiet
                '''
            }
        }

        stage('Build and Start Containers') {
            steps {
                sh '''
                    docker compose -p $COMPOSE_PROJECT_NAME down -v --remove-orphans || true
                    docker compose -p $COMPOSE_PROJECT_NAME up -d --build
                    docker compose -p $COMPOSE_PROJECT_NAME ps
                '''
            }
        }

        stage('Check Application Health') {
            steps {
                sh '''
                    for i in $(seq 1 20); do
                        if docker compose -p $COMPOSE_PROJECT_NAME exec -T uptime-monitor python -c "import requests; r=requests.get('http://127.0.0.1:5000/health', timeout=3); print(r.status_code, r.text); raise SystemExit(0 if r.status_code == 200 else 1)"; then
                            echo "Application health check passed."
                            exit 0
                        fi

                        echo "Waiting for application to become healthy..."
                        sleep 3
                    done

                    echo "Application health check failed."
                    docker compose -p $COMPOSE_PROJECT_NAME logs uptime-monitor
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker compose -p $COMPOSE_PROJECT_NAME down -v --remove-orphans || true
            '''
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}