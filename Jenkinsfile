pipeline {
    agent {label 'windows'}
    stages {
        stage('Python Script to build inventory file') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'vmware-api', passwordVariable: 'user', usernameVariable: 'pass')]) {
                    script{'python3 $JENKINS_HOME\\python\\get_vm_info.py $user $pass dev-master' }
                }
            }
        }
    }
}