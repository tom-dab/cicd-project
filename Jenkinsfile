pipeline {
    agent any

    environment {
        FRONTEND_SSH = 'ssh-frontend' // ID du credential SSH pour le front
        FRONTEND_HOST = '172.16.0.156' // Remplace par l'IP de la VM Apache
        FRONTEND_USER = 'user'   // Remplace par ton user SSH
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Clonage du projet Git"
                git branch: 'exercice5-coralie', url: 'https://github.com/tom-dab/cicd-project.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    echo "⚡ Activation du venv"
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
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
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
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
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
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sshagent([env.FRONTEND_SSH]) {
                    sh """
                        echo "🚀 Déploiement frontend sur ${FRONTEND_HOST}"
                        scp build/frontend.zip ${FRONTEND_USER}@${FRONTEND_HOST}:/tmp/
                        ssh ${FRONTEND_USER}@${FRONTEND_HOST} 'unzip -o /tmp/frontend.zip -d /var/www/html && rm /tmp/frontend.zip'
                    """
                }
            }
        }

        stage('Deploy Backend') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "🚀 Déploiement backend (local ou VM Jenkins)"
                    unzip -o build/backend.zip -d /opt/backend/
                '''
                // Ici tu peux ajouter le restart de service si tu as un service systemd
                // sh 'systemctl restart backend.service'
            }
        }
    }

    post {
        always { echo "🧹 Pipeline terminée" }
        success { echo "🎉 Pipeline réussie!" }
        failure { echo "❌ Échec de la pipeline" }
    }
}
