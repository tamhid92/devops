pipeline {
    agent {label 'windows'}
    stages {
        stage('Python Script to build inventory file') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'user', usernameVariable: 'pass')]) {
                    bat '''
                        echo $JENKINS_HOME 
                    '''
                }
            }
        }
    }
}