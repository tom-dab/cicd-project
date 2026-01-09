pipeline {
    agent any

    environment {
        APP_PORT = "5001"
        FRONT_HOST = "172.16.0.156"
        FRONT_USER = "user"
        FRONT_PATH = "/var/www/html"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Clonage du projet Git"
                git branch: 'exercice6-coralie',
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

        stage('Configurer le port (Exercice 6)') {
            steps {
                echo "⚙️ Configuration du port backend"
                sh '''
                echo "PORT=${APP_PORT}" > backend/config.env
                cat backend/config.env
                '''
            }
        }

        stage('Tests') {
            steps {
                sh '''
                . venv/bin/activate
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
                archiveArtifacts artifacts: 'build/backend.zip'
            }
        }

        stage('Build Frontend') {
            steps {
                sh '''
                echo "📦 Packaging frontend"
                mkdir -p build
                zip -r build/frontend.zip frontend
                '''
                archiveArtifacts artifacts: 'build/frontend.zip'
            }
        }

        stage('Deploy Frontend') {
            steps {
                sshagent(credentials: ['ssh-frontend']) {
                    sh '''
                    echo "🚀 Déploiement frontend"
                    scp build/frontend.zip ${FRONT_USER}@${FRONT_HOST}:/tmp/
                    ssh ${FRONT_USER}@${FRONT_HOST} "sudo unzip -o /tmp/frontend.zip -d ${FRONT_PATH} && sudo rm /tmp/frontend.zip"
                    '''
                }
            }
        }

        stage('Deploy Backend') {
            steps {
                sh '''
                echo "🚀 Déploiement backend"
                sudo mkdir -p /opt/backend
                sudo unzip -o build/backend.zip -d /opt/backend/
                '''
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline réussie"
        }
        failure {
            echo "❌ Échec de la pipeline"
        }
    }
}
