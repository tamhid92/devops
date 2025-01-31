pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'sudo apt-get -y update'
                sh 'sudo apt-get -y dist-upgrade'
            }
        }
        stage('Build Docker App') {
            steps {
                sh 'pwd'
                sh 'docker build -t test_app:dev react/tamhid_dev/'
            }
        }
        stage('Run Docker App') {
            steps {
                sh 'docker run -p 8000:80 test_app:dev'
            }
        }
    }
}