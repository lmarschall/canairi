# Canairi - Air Quaility Monitoring

Project utilizing the Raspberry PI Zero W to retrieve sensor data from
BME680 and calculate an air quality index to retrieve information about
the pollution of indoor rooms. All set up in a dockerized environment.

---

## Prerequisite

* Raspberry Pi Zero W
* BME 680
* SD Card

---

## Get Started

1. Flash the official Raspberry Pi Lite Image on SD Card
2. Edit SD Card Boot Folder to boot Raspberry Pi0W into headless mode
3. Install dependencies on PI0W
4. Clone Repository
5. Build and Start Docker Compose

---

## Edit SD Card

```bash
# create empty wifi config file
touch wpa_supplicant.conf

# enter the following into file
country=DE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
  ssid="NETWORK_NAME"
  psk="NETWORK_PASSWORD"
  key_mgmt=WPA-PSK
}

# create empty ssh file
touch ssh
```

---

## Install Dependencies on PI0W

```bash

# update system
sudo apt-get update
sudo apt-get upgrade

# enter raspberry config and enable i2c interface
sudo raspi-config

# install git
sudo apt-get install git

# install docker and docker-compose
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo systemctl enable docker
sudo apt-get install python3-pip
sudo pip3 install docker-compose

# restart system
sudo reboot
```

---

## Setup Software
```bash
git clone https://github.com/lmarschall/air_quality_monitoring.git
cd ~/air_quality_monitoring
docker-compose build
docker-compose up
```