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

            steps {
                script {
                    def baseimage = docker.image('jautero/alpine-chatterbot')
                    baseimage.pull()
                    app = docker.build("jautero/hopperbot")
                }
            }
        }

        stage('Test image') {
            
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

        stage('Deploy') {
            steps {
                sshagent(['jenkins-deploy']) {
                    sh 'ssh core@docker.eipystyilman.beer <docker/deploy.sh'
                }
            }
        }        
    }
}