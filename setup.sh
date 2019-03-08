#/usr/bin/env bash -e
#
# Auto-generate python virtual environments and install requirements.
#
# Usage
#	./setup.sh
# 

FULLPATH="venv"

# if path does not exist, generate a new virtual environment
if [ ! -d "$FULLPATH" ]
then

    PYTHON=`which python`

    if [ ! -f $PYTHON ]
    then
        echo "Could not find Python"
    fi
    virtualenv -p $PYTHON $FULLPATH

fi

# activate the virtual environment
. $FULLPATH/bin/activate

# install requirements
pip install -r requirements.txt
