#!/bin/sh

CERT_PATH=/opt/rootca
# Make sure the required files exist to perform CA signing operations
# check for serial file
if [ ! -f "$CERT_PATH/serial" ]
then
	echo '01' > $CERT_PATH/serial
	echo "$(date) Created the CA's serial file."
else
	echo "$(date) A serial file already exists. Leaving as is."
fi

# Check for the index file
if [ ! -f "$CERT_PATH/index.txt" ]
then
	touch $CERT_PATH/index.txt
	echo "$(date) Created the CA's index file."
else
	echo "$(date) An index for the CA already exists. Leaving as is."
fi

# Start the certificate check/creation process
./make_certs.sh
