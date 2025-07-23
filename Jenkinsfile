pipeline {
    agent { label 'jai' }

    environment {
        DOCKER_IMAGE_NAME = 'library-management'
        DOCKER_TAG = 'latest'
        DOCKER_REPO = 'jaishankar7655'  // Your Docker Hub username
    }

    stages {
        stage('Code') {
            steps {
                echo 'Cloning the code'
                git url: 'https://github.com/Jaishankar7655/python-container-repo.git', branch: 'main'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the code'
                sh 'docker compose up -d --build'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing the code'
                // Add actual test commands here
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing images to Docker Hub'
                withCredentials([usernamePassword(credentialsId: 'dockerHubCred', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASS')]) {
                    sh '''
                        echo "Logging into Docker Hub..."
                        docker login -u "$DOCKER_HUB_USER" -p "$DOCKER_HUB_PASS"

                        echo "Tagging the image..."
                        docker tag django-app-django:latest $DOCKER_HUB_USER/$DOCKER_IMAGE_NAME:$DOCKER_TAG

                        echo "Pushing the image to Docker Hub..."
                        docker push $DOCKER_HUB_USER/$DOCKER_IMAGE_NAME:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the code'
                // Deployment logic here
            }
        }
    }
}
