pipeline {
    agent none
    stages {
        stage('Python Script to build inventory file') {
            agent {label 'windows'}
            steps{
                withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'api_pass', usernameVariable: 'api_user')]) {
                    powershell '''
                        echo $env:JENKINS_HOME
                        python python\\get_vm_info.py dev-master
                        cd ansible
                        copy .\\hosts.ini \\\\wsl$\\Ubuntu\\home\\tamhid
                    '''
                }
            }
            post {
                always {
                    step {
                        echo 'Clean WS'
                        deleteDir()
                    }
                }
            }
        }
        stage('Run Ansible') {
            agent {label 'wsl'}
            steps{
                sh '''
                    pwd
                '''
            }
            post {
                always {
                    step {
                        echo 'Clean WS'
                        deleteDir()
                    }
                }
            }
        }
    }
}