def NODE = "${params.NODE}"
def NAME = "${params.VM_NAME}"
def SIZE = "${params.VM_SIZE}"
def OPERATION = "${params.OPERATION}"
pipeline {
    agent none
    stages {
        stage('Check VM Status') {
            agent {label "'${NODE}'"}
            steps{
                withCredentials([usernamePassword(credentialsId: 'proxmox_api', passwordVariable: 'TF_VAR_proxmox_api_token_secret', usernameVariable: 'TF_VAR_proxmox_api_token_id')]) {
                    script{
                        sh "export ANSIBLE_HOST_KEY_CHECKING=False"
                        sh "ansible-playbook ansible/main.yml -i ansible/hosts/host.ini -vvv --extra-vars \"vm_name='${NAME}' vm_size='${SIZE}' tf_op='${OPERATION}'\""
                    }
                }
            }
        }
    }
}