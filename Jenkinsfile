pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/47aamir/openshift-demo.git'
        IMAGE_NAME = 'flask-app'
        OPENSHIFT_PROJECT = 'al-razzaq'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                git branch: 'main', changelog: false, poll: false, url: "${REPO_URL}"
            }
        }

        stage('Test Application') {
            steps {
                echo 'Setting up Python environment and testing the application...'
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    python -m unittest discover
                '''
            }
        }

        stage('Build Image using OpenShift') {
            steps {
                echo 'Building image using OpenShift BuildConfig...'
                script {
                    openshift.withCluster() {
                        openshift.withProject("${OPENSHIFT_PROJECT}") {
                            def bc = openshift.selector('bc', "${IMAGE_NAME}")
                            if (bc.exists()) {
                                bc.startBuild("--from-dir=.", "--wait")
                            } else {
                                openshift.newBuild("--binary=true", "--name=${IMAGE_NAME}")
                                openshift.startBuild("${IMAGE_NAME}", "--from-dir=.", "--wait")
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying the application to OpenShift...'
                script {
                    openshift.withCluster() {
                        openshift.withProject("${OPENSHIFT_PROJECT}") {
                            def dc = openshift.selector('dc', "${IMAGE_NAME}")
                            if (dc.exists()) {
                                dc.rollout().latest()
                            } else {
                                openshift.newApp("${OPENSHIFT_PROJECT}/${IMAGE_NAME}:latest")
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
            echo 'Deployment failed!'
        }
    }
}
