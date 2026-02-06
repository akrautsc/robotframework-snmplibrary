pipeline {
    agent {
        label 'mpodman901'
    }
    stages {
        stage('Build preparation') {
            steps {
                echo 'Using branch: ' + env.BRANCH_NAME
                sh '''
                    POETRY_VIRTUALENVS_IN_PROJECT=true poetry install
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    POETRY_VIRTUALENVS_IN_PROJECT=true eval $(poetry env activate)
                    poetry run invoke tests
                '''
            }
        }
        stage('Build and package') {
            steps {
                echo 'Using branch: ' + env.BRANCH_NAME
                sh '''
                    POETRY_VIRTUALENVS_IN_PROJECT=true eval $(poetry env activate)
                    poetry build
                '''
            }
        }
//         stage('Quality Analysis') {
//             steps {
//                 sh 'mvn sonar:sonar -Dsonar.branch.name=' + env.BRANCH_NAME
//             }
//         }
        stage('Create keyword docs') {
            steps {
                echo 'Using branch: ' + env.BRANCH_NAME
                sh '''
                    POETRY_VIRTUALENVS_IN_PROJECT=true eval $(poetry env activate)
                    poetry run invoke libdoc
                '''
            }
        }
        stage('Deploy release version') {
            when { branch 'master' }
            steps {
                echo 'Archiving artifacts generated from branch: ' + env.BRANCH_NAME
                sh '''
                    source venv/bin/activate
                    twine upload --repository-url  http://mnexus001:8081/repository/pypi-releases/ -u deploy -p deploy dist/*.whl
                '''
            }
        }
        stage('Deploy development version') {
            when { anyOf { branch 'feature/*'; branch 'develop' } }
            steps {
                echo 'Archiving artifacts generated from branch: ' + env.BRANCH_NAME
                sh '''
                    source venv/bin/activate
                    twine upload --repository-url  http://mnexus001:8081/repository/pypi-releases/ -u deploy -p deploy dist/*.whl
                '''
            }
        }
        
    }
    post {
        always {
            dir('reports') {
                archiveArtifacts artifacts: '**', allowEmptyArchive: true
            }
            dir('docs') {
                archiveArtifacts artifacts: '**', allowEmptyArchive: true
            }
            cleanWs()
        }
        success {
            mail mimeType:'text/html', body: "<br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL : ${env.BUILD_URL}", subject: "SUCCESS CI: Project name -> ${env.JOB_NAME}", to: "andre.krautschick@eurocontrol.int";
        }
        failure {
            mail mimeType:'text/html', body: "<br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL : ${env.BUILD_URL}", subject: "ERROR CI: Project name -> ${env.JOB_NAME}", to: "andre.krautschick@eurocontrol.int";
        }
    }
//     tools {
//         maven 'Maven 3.5.2'
//         jdk 'openjdk 11.0.1'
//     }
}
