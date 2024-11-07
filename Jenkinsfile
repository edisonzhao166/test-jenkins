pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    // Define a closure (essentially a function in Groovy)
                    def helloWorld = {
                        return "Hello, World!!"
                    }
                    // Call the closure and print the result
                    echo helloWorld()
                }
            }
        }
    }
}
