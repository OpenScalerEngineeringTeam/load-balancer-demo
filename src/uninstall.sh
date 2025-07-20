rm -rf /root/load-balancer-demo
rm -f /etc/systemd/system/load-balancer-demo.service
systemctl daemon-reload
systemctl disable --now load-balancer-demo.service

echo "Load Balancer Demo has been uninstalled."
echo -e "\033[32mNOTE: You may need to remove the following packages manually:\033[0m"
echo ""
echo -e "If you are on Rocky Linux, you may need to remove the following packages manually:"
echo -e "\033[32myum remove python3-pip python3-devel\033[0m"
echo -e "If you are on Debian/Ubuntu, you may need to remove the following packages manually:"
echo -e "\033[32mapt remove python3-flask python3-psutil\033[0m"