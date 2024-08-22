pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/47aamir/openshift-demo.git'
        IMAGE_NAME = 'flask-app'
        OPENSHIFT_PROJECT = 'al-razzaq'
        IMAGE_TAG = "v${BUILD_NUMBER}" // Tag the image with the current build number
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                git url: "${REPO_URL}"
            }
        }

        stage('Test Application') {
            steps {
                echo 'Setting up Python environment and testing the application...'
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m unittest discover -s tests -p "test_*.py"
                '''
            }
        }

        stage('Build Image using OpenShift') {
            steps {
                echo "Building image ${IMAGE_NAME}:${IMAGE_TAG} using OpenShift BuildConfig..."
                script {
                    openshift.withCluster() {
                        openshift.withProject("${OPENSHIFT_PROJECT}") {
                            def bc = openshift.selector('bc', "${IMAGE_NAME}")
                            if (bc.exists()) {
                                bc.startBuild("--from-dir=.", "--wait").logs('-f')
                            } else {
                                openshift.newBuild("--binary=true", "--name=${IMAGE_NAME}")
                                openshift.startBuild("${IMAGE_NAME}", "--from-dir=.", "--wait").logs('-f')
                            }
                        }
                    }
                }
            }
        }

        stage('Tag Image with Build Number') {
            steps {
                echo "Tagging image with ${IMAGE_TAG}..."
                script {
                    openshift.withCluster() {
                        openshift.withProject("${OPENSHIFT_PROJECT}") {
                            openshift.tag("${OPENSHIFT_PROJECT}/${IMAGE_NAME}:latest", "${OPENSHIFT_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG}")
                        }
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying the application with image tag ${IMAGE_TAG} to OpenShift..."
                script {
                    openshift.withCluster() {
                        openshift.withProject("${OPENSHIFT_PROJECT}") {
                            def dc = openshift.selector('dc', "${IMAGE_NAME}")
                            if (dc.exists()) {
                                dc.patch([
                                    spec: [
                                        template: [
                                            spec: [
                                                containers: [
                                                    [name: "${IMAGE_NAME}", image: "${OPENSHIFT_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG}"]
                                                ]
                                            ]
                                        ]
                                    ]
                                ])
                                dc.rollout().latest()
                            } else {
                                openshift.newApp("${OPENSHIFT_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG}")
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Build or tests failed. Deployment aborted.'
        }
    }
}
