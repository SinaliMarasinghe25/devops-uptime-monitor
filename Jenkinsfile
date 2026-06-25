pipeline {
    agent any

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
                    pwd
                    ls -la
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
EOF
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t devops-uptime-monitor:jenkins .
                '''
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh '''
                    docker compose config --quiet
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}