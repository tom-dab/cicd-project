pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Clonage du projet Python'
                checkout scm
            }
        }

        stage('Setup Virtualenv & Dependencies') {
            steps {
                sh '''
                    echo "🔧 Création d'un environnement virtuel"
                    python3 -m venv venv
                    . venv/bin/activate
                    echo "📦 Mise à jour de pip"
                    pip install --upgrade pip
                    echo "📦 Installation des dépendances"
                    if [ -f "backend/requirements.txt" ]; then
                        pip install -r backend/requirements.txt
                    else
                        pip install flask flask-cors requests pytest pytest-html pytest-cov
                    fi
                    echo "✅ Dépendances installées"
                    pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH="$PYTHONPATH:$PWD/backend"
                    pytest -v backend/
                '''
            }
        }

        stage('Build Artifacts') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "📦 Création de l'archive du front"
                    cd frontend
                    zip -r ../front.zip .
                    cd ..
                    echo "📦 Création de l'archive du back"
                    zip -r back.zip backend
                '''
                archiveArtifacts artifacts: 'front.zip', fingerprint: true
                archiveArtifacts artifacts: 'back.zip', fingerprint: true
            }
        }

        stage('Deploy to Server') {
    when {
        expression { currentBuild.currentResult == 'SUCCESS' }
    }
    steps {
        echo '🚀 Déploiement sur le serveur Linux'
        sshagent(['ssh-credential-id']) {
            sh '''
                export SERVER_IP=10.235.247.132
                export SSH_USER=jenkins

                echo "📤 Transfert des archives vers le serveur"
                scp front.zip ${SSH_USER}@${SERVER_IP}:/tmp/
                scp back.zip  ${SSH_USER}@${SERVER_IP}:/tmp/

                echo "🌐 Déploiement du front"
                ssh ${SSH_USER}@${SERVER_IP} << 'EOF'
cd /var/www/html
rm -rf *
unzip -q /tmp/front.zip
echo "✅ Front déployé"
EOF

                echo "🐍 Déploiement du back"
                ssh ${SSH_USER}@${SERVER_IP} << 'EOF'
mkdir -p /opt/app
cd /opt/app
unzip -qo /tmp/back.zip

python3 -m venv venv
. venv/bin/activate
pip install -r backend/requirements.txt

echo "✅ Back déployé"
# Exemple de lancement du back :
# nohup python backend/app.py > app.log 2>&1 &
EOF
            '''
        }
    }
}

    }

    post {
        always { echo '🧹 Nettoyage terminé' }
        success { echo '🎉 Pipeline Python réussie et déployée!' }
        failure { echo '❌ Échec de la pipeline Python' }
        unstable { echo '⚠️ Pipeline instable' }
    }
}
