#!/bin/sh

#############
# Variables #
#############

# Directories
CERT_PATH=/opt/rootca
CONF_PATH=/app/conf
CSRS=$CERT_PATH/csrs

# Config files
CA_CNF=$CONF_PATH/ca.cnf
SERVER_CNF=$CONF_PATH/server.cnf

# Keys
CA_KEY=$CERT_PATH/rootcert/ca_key.pem
SERVER_KEY=$CERT_PATH/private/server_key.pem

# Signing Requests
CA_CSR=$CSRS/ca_req.pem
SERVER_CSR=$CSRS/server_req.pem

# Certificates
CA_CERT=$CERT_PATH/rootcert/ca_crt.pem
SERVER_CERT=$CERT_PATH/pub/server_crt.pem

################################
# Signed Certification Process #
################################

# Create a self signed root certificate and private key
if [[ ! -f $CA_KEY && ! -f $CA_CERT ]]
then
	export OPENSSL_CONF=$CA_CNF
	openssl req -x509 -sha256 -newkey rsa:4098 -nodes -keyout $CA_KEY -out $CA_CERT
	echo "$(date) The CA's key/cert pair has been created."
else
	echo "$(date) The CA's key/cert pair already exist. Leaving as is."
fi

# Make the server's private key and CSR
if [[ ! -f $SERVER_KEY && ! -f $SERVER_CSR ]]
then
	export OPENSSL_CONF=$SERVER_CNF
	openssl req -sha256 -newkey rsa:2048 -nodes -keyout $SERVER_KEY -out $SERVER_CSR
	echo "$(date) Created the server's private key and certificate signing request."
else
	echo "$(date) The server's private key and certificate signing request already exist. Leaving as is."
fi


# Sign the request, -batch to not be prompted for signing process
if [[ ! -f $SERVER_CERT ]]
then
	export OPENSSL_CONF=$CA_CNF
	openssl ca -batch -in $SERVER_CSR -out $SERVER_CERT
        echo "$(date) Created the server's CA signed certificate."
else
	echo "$(date) The server's certificate has already been signed by the CA"
fi
