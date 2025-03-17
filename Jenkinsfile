pipeline {
    stage('Python Script to build inventory file') {
        node('windows') {
            withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'user', usernameVariable: 'pass')])
            sh 'echo $user'
        }
    }
}