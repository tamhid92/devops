pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'sudo apt-get update'
                sh 'sudo apt-get dist-upgrade'
                sh 'sudo apt-add-repository --yes --update ppa:ansible/ansible'
                sh 'sudo apt install ansible'
            }
        }
        stage('Build Docker App') {
            steps {
                sh 'docker build -t test_app:dev /react/tamhid_dev/'
            }
        }
        stage('Run Docker App') {
            steps {
                sh 'docker run -p 80:80 test_app:dev'
            }
        }
    }
}