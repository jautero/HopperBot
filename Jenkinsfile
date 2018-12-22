pipeline {
    agent {
        label 'docker'
    }

    environment {
        PYTHONDONTWRITEBYTECODE = 'YES'
    }
    stages {
    
        stage('Clone repository') {
            /* Let's make sure we have the repository cloned to our workspace */
            steps { 
                checkout scm
            }
        }

        stage('Build image') {
            /* This builds the actual image; synonymous to
             * docker build on the command line */

            steps {
                script {
                    app = docker.build("jautero/hopperbot")
                }
            }
        }

        stage('Test image') {
            /* Ideally, we would run a test framework against our image.
             * For this example, we're using a Volkswagen-type approach ;-) */

            steps {
                script {
                    app.inside("-u 0") {
                        sh 'pip install pytest'
                        sh 'cd /app; python -m pytest $WORKSPACE/test'
                        sh 'rm -rf $WORKSPACE/.pytest_cache'
                    }
                }
            }
        }

        stage('Push image') {
            /* Finally, we'll push the image with two tags:
             * First, the incremental build number from Jenkins
             * Second, the 'latest' tag.
             * Pushing multiple tags is cheap, as all the layers are reused. */
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }
    }
}