pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python --version'
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Install Playwright Browser') {
            steps {
                bat 'python -m playwright install chromium'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'if not exist artifacts mkdir artifacts'
                bat 'python -m pytest -v --env=qa --browser chromium'
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                reportName: 'Playwright HTML Report',
                reportDir: 'reports',
                reportFiles: 'report.html',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])
            archiveArtifacts artifacts: 'reports/**, artifacts/**',
                             allowEmptyArchive: true
        }
    }
}