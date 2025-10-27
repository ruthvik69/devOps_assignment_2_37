pipeline {
    agent any

    environment {
        DOCKERHUB_CRED = 'docker-id'
        KUBE_CONFIG = 'kubeconfig-id'
        IMAGE_NAME = "ruthvikvarma/myapp"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def tag = "${IMAGE_NAME}:${env.BUILD_NUMBER}"
                    def latest = "${IMAGE_NAME}:latest"
                    bat "docker build -t ${tag} -t ${latest} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CRED}", usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    bat """
                        echo ${PASSWORD} | docker login -u ${USERNAME} --password-stdin
                        docker push ${IMAGE_NAME}:${env.BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBE_CONFIG}", variable: 'KUBECONFIG')]) {
                    bat """
                        powershell -Command "(Get-Content k8s\\deployment.yaml) -replace 'image: .*', 'image: ${IMAGE_NAME}:${env.BUILD_NUMBER}' | Set-Content k8s\\deployment.tmp.yaml"
                        kubectl --kubeconfig=%KUBECONFIG% apply -f k8s\\deployment.tmp.yaml
                        kubectl --kubeconfig=%KUBECONFIG% apply -f k8s\\service.yaml
                        kubectl --kubeconfig=%KUBECONFIG% rollout status deployment/myapp
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Deployment failed. Please check logs."
        }
    }
}
