pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'exercice4-coralie',
                    url: 'https://github.com/tom-dab/cicd-project.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r backend/requirements.txt
                    pip install pytest pytest-html pytest-cov flask-cors
                '''
            }
        }

        stage('Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH=$PWD/backend
                    pytest backend/ --junitxml=results.xml
                '''
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }

        stage('Build Backend') {
            steps {
                sh '''
                    echo "📦 Packaging backend"
                    mkdir -p build
                    zip -r build/backend.zip backend
                '''
            }
        }

        stage('Build Frontend') {
            steps {
                sh '''
                    echo "📦 Packaging frontend"
                    mkdir -p build
                    zip -r build/frontend.zip frontend
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'build/*.zip'
            echo '✅ Build et archivage réussis'
        }
        failure {
            echo '❌ Pipeline échouée'
        }
    }
}
