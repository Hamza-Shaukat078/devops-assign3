pipeline {
    agent any

    environment {
        // Docker Hub image names
        APP_IMAGE             = "hamzashaukat078/devops-assign3-app"
        SELENIUM_IMAGE        = "hamzashaukat078/devops-assign3-selenium-tests"

        // Jenkins credentials to log in to Docker Hub
        DOCKERHUB_CREDENTIALS = "dockerhub-credentials-id"

        // docker-compose project name for network resolution
        COMPOSE_PROJECT_NAME  = "devops-assign3"
    }

    stages {

        // -------------------- GIT CHECKOUT --------------------
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Hamza-Shaukat078/devops-assign3.git'
            }
        }

        // -------------------- PYTHON DEPENDENCIES --------------------
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        // -------------------- CODE LINTING --------------------
        stage('Code Linting') {
            steps {
                // Lint only our app code, not third-party libraries in venv
                sh '. venv/bin/activate && flake8 --max-line-length=120 app.py'
            }
        }  
        
        // -------------------- CODE BUILD --------------------
        stage('Code Build') {
            steps {
                sh '. venv/bin/activate && python -m py_compile app.py'
            }
        }

        // -------------------- UNIT TESTING --------------------
        stage('Unit Testing') {
            steps {
                sh '. venv/bin/activate && pytest'
            }
        }

        // -------------------- BUILD APP DOCKER IMAGE --------------------
        stage('Build App Docker Image') {
            steps {
                script {
                    sh "docker build -t ${APP_IMAGE}:latest ."
                }
            }
        }

        // -------------------- PUSH APP IMAGE --------------------
        stage('Push App Docker Image') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: DOCKERHUB_CREDENTIALS,
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh "docker push ${APP_IMAGE}:latest"
                    }
                }
            }
        }

        // -------------------- CONTAINERIZED DEPLOYMENT --------------------
        stage('Containerized Deployment') {
            steps {
                script {
                    // Stop old containers, start new ones
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d --build'
                }
            }
        }

        // -------------------- BUILD SELENIUM TEST IMAGE --------------------
        stage('Build Selenium Test Image') {
            steps {
                script {
                    sh "docker build -t ${SELENIUM_IMAGE}:latest ./selenium-tests"
                }
            }
        }

        // -------------------- PUSH SELENIUM TEST IMAGE --------------------
        stage('Push Selenium Test Image') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: DOCKERHUB_CREDENTIALS,
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh "docker push ${SELENIUM_IMAGE}:latest"
                    }
                }
            }
        }

        // -------------------- SELENIUM TESTING --------------------
        stage('Selenium Testing') {
            steps {
                script {
                    // Compose network name: <project>_default
                    def networkName = "${COMPOSE_PROJECT_NAME}_default"

                    sh """
                    docker run --rm \
                        --network=${networkName} \
                        -e APP_URL=http://web:5000 \
                        ${SELENIUM_IMAGE}:latest
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}
