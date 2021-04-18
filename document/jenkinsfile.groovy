stage('pull source code') {
    node('master'){
        git([url: 'git@github.com:xiaochengyez/my_test_container.git', branch: 'master'])
    }
}

stage('clean docker environment') {
    node('master'){
        try{
            sh 'docker stop my_test'
        }catch(exc){
            echo 'my_test is not running!'
        }

        try{
            sh 'docker rm my_test'
        }catch(exc){
            echo 'my_test does not exist!'
        }
        try{
            sh 'docker rmi test:v1.0'
        }catch(exc){
            echo 'test:v1.0 image does not exist!'
        }
    }
}

stage('make new docker image') {
    node('master'){
        try{
            sh 'docker build -t test:v1.0 .'
        }catch(exc){
            echo 'Make test:v1.0 docker image failed, please check the environment!'
        }
    }
}

stage('start docker container') {
    node('master'){
        try{
            sh 'docker run --name my_test -d -p 8008:8008  test:v1.0'
        }catch(exc){
            echo 'Start docker image failed, please check the environment!'
        }
    }
}