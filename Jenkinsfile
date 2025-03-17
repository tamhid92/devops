pipeline {
    agent {label 'windows'}
    stages {
        stage('Python Script to build inventory file') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'api_pass', usernameVariable: 'api_user')]) {
                    powershell '''
                        echo $env:JENKINS_HOME
                        python python\\get_vm_info.py dev-master
                        ls ansible
                    '''
                }
            }
        }
    }
    agent {label 'wsl'}
    stages {
        stage('Run Ansible') {
            steps{
                sh '''
                    pwd
                '''
            }
        }
    }
    post {
        always {
            echo 'Clean WS'
            deleteDir()
        }
    }
}