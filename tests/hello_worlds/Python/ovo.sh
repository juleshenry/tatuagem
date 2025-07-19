install-environment:
    centos:
        - sudo yum install -y python312
        - echo done installing python
    macos:
        - brew install python314
        - echo done installing python

run-hello-world:
    - python3 hello.py
