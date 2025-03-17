pipeline {
    agent 'windows'
    stages {
        stage('Python Script to build inventory file') {
            withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'user', usernameVariable: 'pass')])
            sh 'echo $user'
        }
    }
}