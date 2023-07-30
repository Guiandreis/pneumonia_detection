#! /bin/bash

# Exit if any command fails
set -e
IFS=$'\n'
export nonroot=$SUDO_USER

echo "###################### INSTALL DEPENDENCIES ###########################################"
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev


echo "###################### CHECK PYENV REPOSITORY #########################################"

if [ -d ${HOME}/.pyenv ]; then
    echo "There is pyenv directory"

else
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    cd ~/.pyenv && src/configure && make -C src

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init -)"' >> ~/.profile
fi

echo "###################### INSTALL PYTHON VERSIONS #########################################"

source ~/.bashrc

pyenv install 3.9.14
pyenv install 3.8.10