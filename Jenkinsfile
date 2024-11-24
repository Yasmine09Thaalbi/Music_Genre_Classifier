pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker-compose -f docker-compose.yml'
        GIT_LFS_SKIP_SMUDGE = '1'
        GITHUB_PAT = credentials('github-pat')  // Fetch the GitHub Personal Access Token
        JENKINS_PASSWORD = '1234'  // Replace with your Jenkins user's password
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    try {
                        // Set up Git configuration to use the GitHub PAT for LFS authentication
                        sh '''
                            git config --global filter.lfs.smudge "git-lfs smudge --skip %f"
                            git config --global credential.helper store
                            echo "https://github.com:${GITHUB_PAT}" > ~/.git-credentials
                        '''

                        // Checkout the repository using GitHub credentials stored in Jenkins
                        git credentialsId: 'github-pat', url: 'https://github.com/Yasmine09Thaalbi/Music_Genre_Classifier.git'

                        // Fetch LFS objects after checkout
                        dir('Music_Genre_Classifier') {
                            sh 'git lfs fetch --all'
                        }

                        echo "--- Checkout stage completed successfully! --- "
                    } catch (Exception e) {
                        echo "--- Checkout stage failed: ${e.message} ---"
                        error("Terminating pipeline due to failure in Checkout stage.")
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    try {
                        // Running docker-compose with mounted Docker socket
                        echo "--- Building Docker images using docker-compose ---"
                        sh '''
                            # Use sudo with password (-S flag) to change ownership of Docker socket
                            echo "${JENKINS_PASSWORD}" | sudo -S chown jenkins:docker /var/run/docker.sock
                            docker-compose build
                        '''

                        echo "--- Docker images built successfully! ---"
                    } catch (Exception e) {
                        echo "--- Build Docker Images stage failed: ${e.message} ---"
                        error("Terminating pipeline due to failure in Build Docker Images stage.")
                    }
                }
            }
        }

        stage('Run SVM Service Unit Test') {
            steps {
                script {
                    try {

                        sh '''
                            sudo apt-get update
                            sudo apt-get install -y python3 python3-pip python3-venv
                        '''

                         // Create a virtual environment
                        sh '''
                            python3 -m venv venv
                        '''

                          // Activate the virtual environment and install pytest
                        sh '''
                            . venv/bin/activate
                            pip install pytest
                        '''
                        

                        sh '''
                            . venv/bin/activate
                            export PYTHONPATH=$(pwd)/Music_Genre_Classifier:$PYTHONPATH
                            pip3 install -r /var/jenkins_home/workspace/Music_Genre_Classifier_CI/svm_service/requirements.txt
                            echo $PYTHONPATH
                            pytest tests/test_svm_service.py
                        '''

                        echo "--- Unit tests completed successfully! ---"
                    } catch (Exception e) {
                        echo "--- Unit Test stage failed: ${e.message} ---"
                        error("Terminating pipeline due to failure in Unit Test stage.")
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    try {
                        sh '''
                            docker-compose down --volumes --remove-orphans
                        '''

                        echo "--- Cleanup stage completed successfully! --- "
                    } catch (Exception e) {
                        echo "--- Cleanup stage failed: ${e.message} ---"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Build and tests succeeded!"
        }
        failure {
            echo "Pipeline failed. Check the logs for details. Build or tests failed!"
        }
    }
}