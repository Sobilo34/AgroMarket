#!/usr/bin/env bash
# sudo wget -O mysql57 https://raw.githubusercontent.com/nuuxcode/alx-system_engineering-devops/master/scripts/mysql57 && sudo chmod +x mysql57 && sudo ./mysql57
echo ""
echo "if wanna read the guide:"
echo "https://docs.google.com/document/d/1btVRofXP75Cj90_xq2x8AmzuMPOKq6D_Dt_SCDD6GrU/"
echo ""
echo ""
echo "-------------------------------"
echo "# Remove Existing MySQL Versions"
echo "-------------------------------"
echo ""
sudo apt-get remove --purge mysql-server mysql-client mysql-common -y && sudo apt-get autoremove -y
echo ""

echo "-------------------------------"
echo "# Remove MySQL Apt Configuration"
echo "-------------------------------"
echo ""
sudo rm -rf /etc/apt/sources.list.d/mysql.list*
sudo rm -rf /var/lib/mysql-apt-config
sudo dpkg --purge mysql-apt-config

echo ""
echo "-------------------------------"
echo "# Remove MySQL Configuration Files"
echo "-------------------------------"
echo ""
sudo rm -rf /etc/mysql /var/lib/mysql
echo "Done!"

echo ""
echo "-------------------------------"
echo "# Update Packages"
echo "-------------------------------"
echo ""
sudo apt update

echo ""
echo "-------------------------------"
echo "# Clean APT Cache"
echo "-------------------------------"
echo ""
sudo apt clean
echo "Done!"

echo ""
echo "-------------------------------"
echo "# Configure Any Pending Packages"
echo "-------------------------------"
echo ""
sudo dpkg --configure -a
echo "Done!"

echo ""
echo "-------------------------------"
echo "# Download and Install MySQL APT configuration package"
echo "-------------------------------"
echo ""
sudo wget -O mysql-apt-config_0.8.12-1_all.deb https://dev.mysql.com/get/mysql-apt-config_0.8.12-1_all.deb
echo "mysql-apt-config mysql-apt-config/select-server select mysql-5.7" | sudo debconf-set-selections
echo "mysql-apt-config mysql-apt-config/select-server-5.7 select bionic" | sudo debconf-set-selections
sudo dpkg -i mysql-apt-config_0.8.12-1_all.deb

echo ""
echo "-------------------------------"
echo "# Import the GPG key for the MySQL repository"
echo "-------------------------------"
echo ""
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 467B942D3A79BD29
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C

echo ""
echo "-------------------------------"
echo "# Update Packages"
echo "-------------------------------"
echo ""
sudo apt update

echo ""
echo "-------------------------------"
echo "# Display information MySQL server package"
echo "-------------------------------"
echo ""
sudo apt-cache policy mysql-server

echo ""
echo "-------------------------------"
echo "# Install MySQL 5.7"
echo "-------------------------------"
echo ""
sudo apt install -f mysql-client=5.7* mysql-community-server=5.7* mysql-server=5.7* -y

echo ""
echo "-------------------------------"
echo "# Check if MySQL 5.7 installed correctly"
echo "-------------------------------"
echo ""
sudo mysql --version
echo ""
