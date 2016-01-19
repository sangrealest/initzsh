#!/bin/bash
#Author:Shanker

clear
echo ""
echo "#############################################################"
echo "# Automatically to  Install oh-my-zsh and initialize it     #"
echo "# Intro: https://github.com/sangrealest/shanker             #"
echo "# Author: Shanker<shanker@yeah.net>                         #"
echo "#############################################################"
echo ""


if [ `id -u` -ne 0 ]
then
    echo "Need root to run is, try with sudo"
    exit 1
fi

function checkOs(){
    if [ -f /etc/redhat-release ]
    then
        OS=CentOS
    elif [ ! -z "`cat /etc/issue | grep -i bian`" ]
    then
        OS=Debian
    elif [ ! -z "`cat /etc/issue | grep -i ubuntu`" ]
    then
        OS=Ubuntu
    else
        echo "Not supported OS"
        exit 1
    fi
} 


if [ "$OS" == "CentOS" ]
then
    yum -y install zsh git 
else
    apt-get -y install zsh git
fi
zshPath="`which zsh`"

function downloadFile(){
    cd ~
    git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
    git clone https://github.com/joelthelion/autojump.git
    git clone https://github.com/sangrealest/initzsh 
}
function installAutojump(){
    cd ~/autojump
    ./install.py
}

function configZsh(){
    if [ -f ".zsh_history" ]
    then
        mv .zsh_history{.,backup}
    fi
    chsh -s "$zshPath"
    cp ~/initzsh/zshrc ~/.zshrc
   
}
downloadFile
installAutojump
configZsh
 

