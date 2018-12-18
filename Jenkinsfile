pipeline {
    agent { dockerfile true }
    stages {
        stage('Test') {
            steps {
                sh 'pip install pytest'
                sh 'cd /app'
                sh 'py.test $WORKSPACE/test'
            }
        }
    }
}