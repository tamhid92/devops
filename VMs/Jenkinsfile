pipeline {
    agent none
    stages {
        stage('Check VM Status') {
            agent {label 'linux'}
            steps{
                withCredentials([usernamePassword(credentialsId: 'proxmox_api', passwordVariable: 'TF_VAR_proxmox_api_token_secret', usernameVariable: 'TF_VAR_proxmox_api_token_id')]) {
                    sh '''
                        
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
    }
}