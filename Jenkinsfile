pipeline {
    agent { dockerfile true }
    stages {
        stage('Test') {
            steps {
                sh 'pip install pytest'
                sh 'py.test test/'
            }
        }
    }
}