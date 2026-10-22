
pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = 'dockerhub-credentials-id'
        DOCKER_IMAGE_NAME      = 'moaffan164/healthcare-appointment'
        IMAGE_TAG              = "${env.BUILD_NUMBER}"
        SONARQUBE_SERVER       = 'SonarQubeServer'
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo '=== Stage 1: Checking out GitHub Repository ==='
                checkout scm
            }
        }

        stage('Code Linting & Syntax Check') {
            steps {
                echo '=== Stage 2: Syntax Check and Unit Tests ==='
                sh '''
                    set -eu
                    docker build -f Dockerfile.ci -t healthcare-appointment-test .
                    docker run --rm healthcare-appointment-test \
                        python -m compileall -q app.py database.py tests/
                    docker run --rm healthcare-appointment-test \
                        python -m pytest -q
                '''
            }
        }

        stage('Unit Testing & Coverage') {
            steps {
                echo '=== Stage 3: Unit Tests and Coverage Reports ==='
                sh '''
                    set -eu

                    docker build -f Dockerfile.ci -t healthcare-appointment-test .

                    docker rm -f ci-coverage >/dev/null 2>&1 || true

                    docker create --name ci-coverage healthcare-appointment-test \
                        sh -c "python -m pytest \
                        --junitxml=/tmp/test-results.xml \
                        --cov=app --cov=database \
                        --cov-report=xml:/tmp/coverage.xml tests/"

                    set +e
                    docker start -a ci-coverage
                    test_exit=$?
                    set -e

                    docker cp ci-coverage:/tmp/test-results.xml "$WORKSPACE/test-results.xml"
                    docker cp ci-coverage:/tmp/coverage.xml "$WORKSPACE/coverage.xml"

                    docker rm -f ci-coverage >/dev/null 2>&1 || true

                    if [ "$test_exit" -ne 0 ]; then
                        exit "$test_exit"
                    fi
                '''
            }
            post {
                always {
                    junit allowEmptyResults: false, testResults: 'test-results.xml'
                }
            }
        }

        stage('SonarQube SAST Analysis') {
            steps {
                echo '=== Stage 4: SonarQube Static Analysis ==='
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh '''
                        set -eu

                        docker run --rm \
                          --network host \
                          --volumes-from jenkins \
                          -e SONAR_HOST_URL="$SONAR_HOST_URL" \
                          -e SONAR_TOKEN="$SONAR_AUTH_TOKEN" \
                          sonarsource/sonar-scanner-cli \
                          -Dsonar.projectKey=healthcare-appointment-devsecops \
                          -Dsonar.projectName="Healthcare Appointment DevSecOps System" \
                          -Dsonar.projectBaseDir="$WORKSPACE" \
                          -Dsonar.sources=app.py,database.py,templates,static \
                          -Dsonar.tests=tests \
                          -Dsonar.test.inclusions=tests/**/test_*.py \
                          -Dsonar.python.coverage.reportPaths=coverage.xml \
                          -Dsonar.scanner.metadataFilePath="$WORKSPACE/report-task.txt" \
                          -Dsonar.working.directory=/tmp/sonar-work
                    '''
                }
            }
        }

        stage('SonarQube Quality Gate') {
    steps {
        timeout(time: 5, unit: 'MINUTES') {
            script {
                def qg = waitForQualityGate()
                if (qg.status != 'OK') {
                    error "Quality Gate failed: ${qg.status}"
                }
            }
        }
    }
}

        stage('Docker Image Build') {
            steps {
                echo '=== Stage 6: Building Application Image ==='
                sh '''
                    set -eu
                    docker build \
                      -t "$DOCKER_IMAGE_NAME:$IMAGE_TAG" \
                      -t "$DOCKER_IMAGE_NAME:latest" .
                '''
            }
        }

        stage('Trivy Security Scanning') {
            steps {
                echo '=== Stage 7: Trivy Vulnerability Scanning ==='
                sh '''
                    set -eu
                    mkdir -p reports/security

                    docker run --rm \
                      --volumes-from jenkins \
                      -w "$WORKSPACE" \
                      aquasec/trivy:latest \
                      fs --scanners vuln,misconfig,secret \
                      --severity HIGH,CRITICAL \
                      --format table \
                      -o reports/security/trivy-fs-report.txt .

                    docker run --rm \
                      --volumes-from jenkins \
                      -w "$WORKSPACE" \
                      aquasec/trivy:latest \
                      fs --format json \
                      -o reports/security/trivy-fs-report.json .

                    docker run --rm \
                      --volumes-from jenkins \
                      -w "$WORKSPACE" \
                      aquasec/trivy:latest \
                      image --severity HIGH,CRITICAL \
                      --format table \
                      -o reports/security/trivy-image-report.txt \
                      "$DOCKER_IMAGE_NAME:$IMAGE_TAG"

                    docker run --rm \
                      --volumes-from jenkins \
                      -w "$WORKSPACE" \
                      aquasec/trivy:latest \
                      config --severity HIGH,CRITICAL \
                      --format table \
                      -o reports/security/trivy-iac-report.txt terraform/
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/security/**',
                                     allowEmptyArchive: true
                }
            }
        }

        stage('Push Image to Registry') {
            steps {
                echo '=== Stage 8: Pushing Image to Docker Hub ==='
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_HUB_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        set -eu
                        echo "$DOCKER_PASS" | docker login \
                          -u "$DOCKER_USER" --password-stdin

                        docker push "$DOCKER_IMAGE_NAME:$IMAGE_TAG"
                        docker push "$DOCKER_IMAGE_NAME:latest"

                        docker logout
                    '''
                }
            }
        }

        stage('Terraform IaC Provisioning') {
            steps {
                echo '=== Stage 9: Terraform Initialization and Validation ==='
                dir('terraform') {
                    sh '''
                        set -eu

                        docker run --rm \
                          --volumes-from jenkins \
                          -w "$WORKSPACE/terraform" \
                          hashicorp/terraform:1.11 \
                          init -input=false

                        docker run --rm \
                          --volumes-from jenkins \
                          -w "$WORKSPACE/terraform" \
                          hashicorp/terraform:1.11 \
                          validate
                    '''
                }
            }
        }

        stage('Automated Deployment & Smoke Test') {
            steps {
                echo '=== Stage 10: Local Container Smoke Test ==='
                sh '''
                    set -eu

                    CONTAINER_NAME="healthcare-smoke-${BUILD_NUMBER}"
                    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

                    cleanup() {
                        docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
                    }
                    trap cleanup EXIT

                    docker run -d \
                      --name "$CONTAINER_NAME" \
                      -p 127.0.0.1:5001:5000 \
                      "$DOCKER_IMAGE_NAME:$IMAGE_TAG"

                    attempt=0
                    until docker run --rm \
                        --network container:"$CONTAINER_NAME" \
                        curlimages/curl:latest \
                        -fsS http://127.0.0.1:5000/ >/dev/null; do

                        attempt=$((attempt + 1))

                        if [ "$attempt" -ge 12 ]; then
                            docker logs "$CONTAINER_NAME"
                            echo "Smoke test failed: application did not become healthy."
                            exit 1
                        fi

                        sleep 5
                    done

                    echo "Smoke test passed: application responded successfully."
                '''
            }
        }
    }

    post {
        always {
            echo '=== DevSecOps Pipeline Execution Finished ==='
            cleanWs deleteDirs: true, notFailBuild: true
        }
        success {
            echo '=== All configured pipeline stages succeeded. ==='
        }
        failure {
            echo '=== Pipeline failed. Review the stage logs above. ==='
        }
    }
}
