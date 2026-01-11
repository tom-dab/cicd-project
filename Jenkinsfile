pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Clonage du projet'
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

        stage('Build artifacts') {
            // ce stage ne sera exécuté que si les stages précédents ont réussi
            steps {
                sh '''
                    echo "📦 Création de l'archive backend"
                    rm -f backend.zip frontend.zip

                    # backend : on archive le code Python et le requirements
                    zip -r backend.zip backend/app.py backend/test_app.py backend/requirements.txt

                    echo "📦 Création de l'archive frontend"
                    zip -r frontend.zip frontend/
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline Python réussie, publication des artifacts'
            archiveArtifacts artifacts: 'backend.zip, frontend.zip', fingerprint: true
        }
        failure {
            echo '❌ Échec de la pipeline Python (pas de build ni d\'artifacts)'
        }
        always {
            echo '🧹 Nettoyage terminé'
        }
    }
}
