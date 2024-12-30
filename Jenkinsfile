pipeline{
    agent any
    environment {
        DOCKER_IMAGE = "jorgthor/multi-stage-add"
        DOCKER_CREDENTIALS = "docker-hub-credentials"
        DOCKER_TAG = "latest"
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from git'
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                echo 'Installing dependencies'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Tests') {
            steps {
                echo 'Running tests'
                sh 'python3 -m unittest discover -s tests'
            }
        }
        stage('Build image') {
            steps {
                echo 'Building docker image'
                script {
                    sh "docker build -t $DOCKER_IMAGE:$DOCKER_TAG ."
                }
            }
        }
        stage('Push') {
            steps {
                echo 'Pushing docker image'
                script {
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh "docker login -u jorgthor -p $DOCKER_PASSWORD"
                        sh "docker push $DOCKER_IMAGE:$DOCKER_TAG"
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                echo 'Cleaning up'
                sh 'docker rmi $DOCKER_IMAGE:$DOCKER_TAG'
            }
        }
    }
    post {
        success {
            echo 'Build successful'
        }
        failure {
            echo 'Build failed'
        }
        always {
            echo 'Build finished'
        }
    }
}