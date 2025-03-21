pipeline {
    agent none
    stages {
        stage('Check VM Status') {
            agent {label 'windows'}
            steps{
                withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'api_pass', usernameVariable: 'api_user')]) {
                    powershell '''
                        Start-Process -FilePath "C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrest.exe"
                        echo $env:JENKINS_HOME
                        python python\\get_vm_info.py dev-master
                        cd ansible
                        copy .\\hosts.ini \\\\wsl$\\Ubuntu\\home\\tamhid
                    '''
                }
            }
            post {
                always {
                    echo 'Clean WS'
                    deleteDir()
                }
            }
        }
        stage('Run Ansible') {
            agent {label 'wsl'}
            steps{
                sh '''
                    ansible-galaxy collection install community.docker
                    ansible-playbook ansible/main.yml -i /home/tamhid/hosts.ini
                '''
            }
            post {
                always {
                    echo 'Clean WS'
                    deleteDir()
                    sh '''
                        rm /home/tamhid/hosts.ini
                    '''
                }
            }
        }
    }
}