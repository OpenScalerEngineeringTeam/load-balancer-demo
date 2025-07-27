#cloud-config
package_update: true
packages:
- curl
- php-cli
- php-common
- php-xml
- php-mbstring
- php-zip
- php-bcmath
- php-curl

# -------------------------------------------------------------------------------------------------
#   Debian/Ubuntu
# -------------------------------------------------------------------------------------------------
runcmd:
# download source release
- cd /root
- wget https://github.com/OpenScalerEngineeringTeam/load-balancer-demo/archive/refs/tags/v0.0.5.tar.gz -O /root/load-balancer-demo.tar.gz
- tar -xzf /root/load-balancer-demo.tar.gz -C /root/
- rm /root/load-balancer-demo.tar.gz
- mv /root/load-balancer-demo-0.0.5 /root/load-balancer-demo
# Install dependenciess
- cd /root/load-balancer-demo/admin_app && . scripts/utils.sh && . scripts/install-dependencies.sh