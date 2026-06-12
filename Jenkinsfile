pipeline {
    agent {
        label 'windows-ui-agent'
    }

    options {
        timestamps()
        timeout(time: 90, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        PYTHONIOENCODING = 'UTF-8'
        CHROME_USER_DATA_CLEANUP = 'true'
        CHROME_USER_DATA_DIR = "${WORKSPACE}\\jenkins-chrome-profile"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat '''
                    python -m venv .venv
                    call .venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install chrome
                '''
            }
        }

        stage('Prepare Chrome Profile') {
            steps {
                bat '''
                    if exist jenkins-chrome-profile rmdir /s /q jenkins-chrome-profile
                    if exist .chrome-profile rmdir /s /q .chrome-profile
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call .venv\\Scripts\\activate.bat
                    pytest
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']]
        }
        failure {
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
    }
}
