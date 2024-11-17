pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker-compose -f docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-pat', url: 'https://github.com/Yasmine09Thaalbi/Music_Genre_Classifier.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh "docker-compose build"
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh 'pytest tests/test_svm_service.py'
                    echo "Unit tests completed successfully!"
                }
            }
        }
    }

    post {
        success {
            echo 'Build and tests succeeded!'
        }
        failure {
            echo 'Build or tests failed!'
        }
    }
}
