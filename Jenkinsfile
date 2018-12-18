pipeline {
    agent { dockerfile true }
    stages {
        stage('Test') {
            steps {
                sh 'pip install pytest'
                sh 'ls;pwd'
                sh 'py.test test/'
            }
        }
    }
}