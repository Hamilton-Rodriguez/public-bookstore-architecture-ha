#!/bin/bash
sleep 30

function conf-firewalld() {
    setenforce 0
    sudo /usr/bin/firewall-cmd --zone=public --add-port=5000/tcp --permanent
    sudo /usr/bin/firewall-cmd --reload
    setenforce 1
}
conf-firewalld
sudo cp /home/opc/architecture-ha/bookapp.service /etc/systemd/system/bookapp.service
sudo systemctl daemon-reload
sudo systemctl enable bookapp.service
sudo systemctl start bookapp.service
