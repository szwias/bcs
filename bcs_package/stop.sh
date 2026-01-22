#!/bin/bash
multipass exec bcs-test -- docker-compose -f /home/ubuntu/src/docker-compose.yml down
multipass stop bcs-test
