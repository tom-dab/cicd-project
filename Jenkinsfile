pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Clonage du projet Python'
                git branch: 'exercice3', url: 'https://github.com/tom-dab/cicd-project.git'
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

                    echo "📦 Installation des dépendances du projet"
                    if [ -f "backend/requirements.txt" ]; then
                        pip install -r backend/requirements.txt
                    fi

                    # Installation des plugins pytest
                    pip install pytest pytest-html pytest-cov flask-cors

                    echo "✅ Dépendances installées"
                    pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "🧪 Exécution des tests Python"
                    . venv/bin/activate
                    export PYTHONPATH="${PYTHONPATH}:${PWD}/backend"

                    pytest -v \
                        --junitxml=results.xml \
                        --html=report.html \
                        --self-contained-html \
                        --cov=backend \
                        backend/ || echo "Tests terminés avec erreurs"
                '''
            }
            post {
                always {
                    script {
                        if (fileExists('results.xml')) { junit 'results.xml' }
                        if (fileExists('report.html')) { archiveArtifacts artifacts: 'report.html' }
                    }
                }
            }
        }
    }

    post {
        always { echo '🧹 Nettoyage terminé' }
        success { echo '🎉 Pipeline Python réussie!' }
        failure { echo '❌ Échec de la pipeline Python' }
        unstable { echo '⚠️ Pipeline instable' }
    }
}
