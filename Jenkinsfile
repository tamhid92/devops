pipeline {
    agent {label 'windows'}
    stages {
        stage('Python Script to build inventory file') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    powershell '''
                        echo $env:JENKINS_HOME
                    '''
                }
            }
        }
    }
}