#! /bin/bash
# -------------------------------------------------------------------------------------------------
#   The following script works assuming "psutil" and "flask" are installed.
# -------------------------------------------------------------------------------------------------
cp /root/load-balancer-demo/src/load-balancer-demo.service /etc/systemd/system/load-balancer-demo.service
chmod 644 /etc/systemd/system/load-balancer-demo.service
chmod +x /root/load-balancer-demo/src/load-balancer-demo.py

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable --now load-balancer-demo.service