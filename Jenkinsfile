pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sinalimarasinghe25/devops-uptime-monitor'
        VM_HOST = 'up-monitor.duckdns.org'
        VM_PROJECT_DIR = '/home/azureuser/devops-uptime-monitor'
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
                    SCHEDULER_ENABLED=false PYTHONPATH=$WORKSPACE venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKER_IMAGE:latest -t $DOCKER_IMAGE:$BUILD_NUMBER .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    string(credentialsId: 'dockerhub-username', variable: 'DOCKERHUB_USERNAME'),
                    string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')
                ]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                        docker push $DOCKER_IMAGE:latest
                        docker push $DOCKER_IMAGE:$BUILD_NUMBER
                    '''
                }
            }
        }

        stage('Deploy to Azure VM') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'azure-vm-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$VM_HOST" "
                            cd $VM_PROJECT_DIR &&
                            git fetch origin &&
                            git checkout development &&
                            git pull origin development &&
                            docker compose -f docker-compose.prod.yml pull &&
                            docker compose -f docker-compose.prod.yml up -d &&
                            docker compose -f docker-compose.prod.yml ps
                        "
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    curl -f https://up-monitor.duckdns.org/health
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker logout || true
            '''
        }
        success {
            echo 'CI/CD pipeline completed successfully. Application deployed to Azure VM.'
        }
        failure {
            echo 'Pipeline failed. Check the failed stage logs.'
        }
    }
}