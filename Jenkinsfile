pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/edisonzhao166/test-jenkins.git' // Replace with your repo URL
        AIRFLOW_DAG_ID = 'demo1' // Replace with your Airflow DAG ID
        COMPOSE_FILE = 'docker-compose.yaml' // Name of the docker-compose file
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the GitHub repository
                git url: "${REPO_URL}", branch: "${env.BRANCH_NAME}"
            }
        }

        stage('Set Up Docker Environment') {
            steps {
                // Build and start the containers using docker-compose
                script {
                    sh "docker-compose -f ${COMPOSE_FILE} up -d --build"
                }
            }
        }

        stage('Trigger Airflow DAG') {
            steps {
                // Trigger the Airflow DAG for model training and evaluation
                script {
                    def response = sh(
                        script: '''
                            curl -X POST http://localhost:8081/api/v1/dags/demo1/dagRuns \
                            -H \"Content-Type: application/json\" \
                            -u airflow:airflow \
                            -d \'{"conf":{}}\'
                        ''',
                        returnStatus: true
                    )
                    if (response != 0) {
                        error("Failed to trigger Airflow DAG")
                    }
                }
            }
        }

//         stage('Monitor DAG') {
//             steps {
//                 // Monitor DAG status until completion
//                 script {
//                     def dag_status = ""
//                     while (dag_status != "success") {
//                         dag_status = sh(
//                             script: "docker exec -it airflow_webserver airflow dags state ${AIRFLOW_DAG_ID} $(date +%Y-%m-%d) | tail -n 1",
//                             returnStdout: true
//                         ).trim()
//                         if (dag_status == "failed") {
//                             error("DAG ${AIRFLOW_DAG_ID} failed.")
//                         }
//                         sleep(time: 30, unit: 'SECONDS')
//                     }
//                 }
//             }
//         }
    }

    post {
        always {
            // Stop and remove Docker containers
            sh 'docker ps -q | xargs -r docker stop'
            sh 'docker ps -aq | xargs -r docker rm'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details!!!!!!'
        }
    }
}
