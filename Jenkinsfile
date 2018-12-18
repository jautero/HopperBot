pipeline {
    agent { dockerfile true }
    stages {
        stage('Test') {
            steps {
                sh 'pip install pytest'
                sh 'cd /app; py.test $WORKSPACE/test/'
            }
        }
    }
}