#!/bin/bash
sleep 30
sudo /usr/bin/firewall-cmd --zone=public --add-port=5000/tcp --permanente
sudo /usr/bin/firewall-cmd --reload
sudo cp /home/opc/architecture-ha/bookapp.service /etc/systemd/system/bookapp.service
sudo systemctl daemon-reload
sudo systemctl enable bookapp.service
sudo systemctl start bookapp.service
