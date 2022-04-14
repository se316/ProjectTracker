FROM alpine:latest

WORKDIR app/
COPY . . 

# get openssl
RUN apk update; apk add openssl

# make directories for certificates
ARG CADIR=/opt/rootca
RUN mkdir -p $CADIR && mkdir \
	$CADIR/csrs $CADIR/private \
	$CADIR/crl $CADIR/newcerts \
	$CADIR/rootcert $CADIR/pub \
	$CADIR/signedcerts 
