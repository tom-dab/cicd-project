pipeline {
    agent any

    /* ===== PARAMÈTRES JENKINS EXO6 ===== */
    parameters {
        string(
            name: 'APP_PORT',
            defaultValue: '5000', // Elle va modifié le confichier de config plus bas
            description: 'Port sur lequel le backend doit écouter'
        )
    }

    /* ===== VARIABLES D’ENVIRONNEMENT ===== */
    environment {
        FRONTEND_SERVER = "172.16.0.156"
        FRONTEND_USER   = "user"
        BACKEND_DIR     = "/opt/backend"
        CONFIG_FILE     = "backend/config.env"
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
                echo "⚙️ Configuration du port backend : ${APP_PORT}"
                sh '''
                    echo "APP_PORT=${APP_PORT}" > backend/config.env
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
                        scp build/frontend.zip ${FRONTEND_USER}@${FRONTEND_SERVER}:/tmp/
                        ssh ${FRONTEND_USER}@${FRONTEND_SERVER} "
                            unzip -o /tmp/frontend.zip -d /var/www/html &&
                            rm /tmp/frontend.zip
                        "
                    '''
                }
            }
        }

        stage('Deploy Backend') {
            steps {
                sh '''
                    echo "🚀 Déploiement backend"
                    mkdir -p ${BACKEND_DIR}
                    unzip -o build/backend.zip -d ${BACKEND_DIR}
                '''
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline réussie – application déployée sur le port ${APP_PORT}"
        }
        failure {
            echo "❌ Échec de la pipeline"
        }
    }
}
