pipeline {
    agent any

    stages {
        stage('Setup venv & Install') {
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
    }

    post {
        always   { echo '🧹 Nettoyage terminé' }
        success  { echo '🎉 Pipeline Python réussie!' }
        failure  { echo '❌ Échec de la pipeline Python' }
        unstable { echo '⚠️ Pipeline instable' }
    }
}
