# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant Cassandra Project
# https://github.com/bcantoni/vagrant-cassandra
# Brian Cantoni

# This sample sets up 1 VM ('cassandra') with only Java installed.
# See the README for a walkthrough explaining Cassandra and DataStax installation.

# Adjustable settings
CFG_MEMSIZE = "3000"      # max memory for each VM
CFG_TZ = "US/Pacific"     # timezone, like US/Pacific, US/Eastern, UTC, Europe/Warsaw, etc.
CFG_IP = "10.211.54.10"   # private IP address

# if local Debian proxy configured (DEB_CACHE_HOST), install and configure the proxy client
deb_cache_cmds = ""
if ENV['DEB_CACHE_HOST']
  deb_cache_host = ENV['DEB_CACHE_HOST']
  deb_cache_cmds = <<CACHE
apt-get install squid-deb-proxy-client -y
echo 'Acquire::http::Proxy "#{deb_cache_host}";' | sudo tee /etc/apt/apt.conf.d/30autoproxy
echo "Acquire::http::Proxy { debian.datastax.com DIRECT; };" | sudo tee -a /etc/apt/apt.conf.d/30autoproxy
cat /etc/apt/apt.conf.d/30autoproxy
CACHE
end

# Provisioning script
node_script = <<SCRIPT
#!/bin/bash
# set timezone
echo "#{CFG_TZ}" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata
#{deb_cache_cmds}
# install Java and a few base packages
apt-get update
apt-get install vim curl zip unzip git python-pip openjdk-7-jdk -y
echo "Vagrant provisioning complete"
SCRIPT


# Configure VM server
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define :cassandra do |x|
    x.vm.box = "hashicorp/precise64"
    x.vm.provider "vmware_fusion" do |v|
      v.vmx["memsize"]  = CFG_MEMSIZE
    end
    x.vm.provider :virtualbox do |v|
      v.name = "cassandra"
      v.customize ["modifyvm", :id, "--memory", CFG_MEMSIZE]
    end
    x.vm.network :private_network, ip: CFG_IP
    x.vm.hostname = "cassandra"
    x.vm.provision :shell, :inline => node_script
  end
end