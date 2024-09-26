# -*- mode: ruby -*-
# vi: set ft=ruby :

# Тестовый стенд на Kali
Vagrant.configure("2") do |config|
  config.vm.box = "kalilinux/rolling"
  config.vm.box_version = "2024.2.0"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 2
  end
  config.vm.provision "shell", inline: <<-SHELL
    # Установка зависимостей
    apt-get update
    apt-get upgrade -y
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common

    # Установка docker
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
    echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
    apt-get update
    apt-get install -y docker-ce

    # Установка docker-compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    # Запуск проекта
    git clone https://github.com/light-hat/looking-glass /app
    cd /app
    docker-compose up -d
  SHELL
end
