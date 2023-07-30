#!/bin/bash

# Check for existing pyenv installs
if ! command -v pyenv &> /dev/null; then
  echo "pyenv command not found. Checking for $PYENV_ROOT"
	# Check if install dir exists
	if [ ! -d $PYENV_ROOT ]; then
    echo "PYENV_ROOT not found, running automated install."
    echo "pyenv will be installed to $PYENV_ROOT."
		# Run automated install
		curl https://pyenv.run | bash
	fi
	# Add to path
  if ! grep -F PYENV_ROOT= ~/.bashrc; then
    echo "export PYENV_ROOT="$PYENV_ROOT"" >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  fi
fi

echo "pyenv setup complete."
echo "A shell restart may be necessary for changes to take effect"