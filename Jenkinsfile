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
                git url: "${REPO_URL}", branch: 'main'
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
                    sh """
                    curl -X POST http://localhost:8080/api/v1/dags/demo1/dagRuns \
                    -H "Content-Type: application/json" \
                    -u airflow:airflow \
                    -d '{"conf":{}}'
                    """
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
            sh 'docker stop $(docker ps -q)'
            sh 'docker rm $(docker ps -aq)'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
