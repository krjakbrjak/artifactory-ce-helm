# Artifactory HELM chart

This HELM chart is based on the [official docker-compose](https://releases.jfrog.io/artifactory/bintray-artifactory/org/artifactory/cpp/ce/docker/jfrog-artifactory-cpp-ce/[RELEASE]/jfrog-artifactory-cpp-ce-[RELEASE]-compose.tar.gz). [kompose](https://kompose.io/) was used to translate the original `docker-compose.yml`.

## Install

```shell
helm install artifactory-cpp-ce --namespace artifactory-cpp-ce ./chart --create-namespace
```

And then it can be accessed with:
```shell
curl https://example.host/ -Lkv --resolve example.host:443:127.0.0.1
```

## TLS

The following yaml can be used to configure the tls:

```yaml
tls:
  enabled: true
  host: example.host
  crt: b64-encoded certificate
  key: b64-encoded key
```

An example of this block can be generated with:
```shell
python generate_values.yml
```
See `python generate_values.py --help` for more details.

The key and and the certificate could also be generated with the following command:
```shell
openssl req -x509 -nodes -days 730 -newkey rsa:2048 \
   -keyout tls.key \
   -out tls.crt \
   -config example.conf \
   -extensions 'v3_req'
```

Where `example.conf` could be defined as:
```ini
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
CN = example-address.com
[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = example-address.com
```

## Access from browser

In case there is no public name for the host, one can use reverse proxy to redirect the original request to the k8s cluster with the right Host header. The following command starts nginx proxy in docker:
```shell
docker run -v `pwd`/nginx.conf:/etc/nginx/nginx.conf --network host --rm nginx:latest
```
