# Artifactory HELM chart

This HELM chart is based on the [official docker-compose](https://releases.jfrog.io/artifactory/bintray-artifactory/org/artifactory/cpp/ce/docker/jfrog-artifactory-cpp-ce/[RELEASE]/jfrog-artifactory-cpp-ce-[RELEASE]-compose.tar.gz). [kompose](https://kompose.io/) was used to translate the original `docker-compose.yml`.

## Prerequisites

In case TLS is required, this cahrt requires [cert-manager](https://cert-manager.io/) to be installed.

## Install

```shell
helm install artifactory-cpp-ce --namespace artifactory-cpp-ce ./chart --set tls.cert.email=user@example.com --create-namespace --set tls.enabled=true --set tls.host=example.com --set tls.cert.server=https://acme-v02.api.letsencrypt.org/directory
```

By default, `Artifactory Community Edition for C and C++` will be installed. One can choose different products. For example, `--set artifactory.product=jcr` will install `JFrog Container Registry`.

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
  cert:
    email: user@example.com
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    name: letsencrypt-staging
    organization: Example Organization
```
