#! /usr/bin/env python

import argparse
import base64
import datetime

import yaml
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509.oid import NameOID

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="Country name", default="AT")
    parser.add_argument(
        "-s", "--state", help="State or province name", default="Vienna"
    )
    parser.add_argument("-l", "--locality", help="Locality name", default="Vienna")
    parser.add_argument(
        "-on",
        "--organization",
        help="Organization name",
        default="Example Organization",
    )
    parser.add_argument("-d", "--domain", help="Domain", default="example.organization")
    parser.add_argument("--expire", help="Valid period (days)", type=int, default=365)
    parser.add_argument("-o", "--output", help="Output location", default="values.yaml")
    args = parser.parse_args()

    root_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, args.country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, args.state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, args.locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, args.organization),
            x509.NameAttribute(NameOID.COMMON_NAME, args.domain),
        ]
    )
    root_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(root_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=args.expire)
        )
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(args.domain)]),
            critical=False,
        )
        .sign(root_key, hashes.SHA256(), default_backend())
    )

    with open(args.output, "w") as outfile:
        data = dict(
            tls=dict(
                enabled=True,
                host=args.domain,
                crt=base64.b64encode(root_cert.public_bytes(Encoding.PEM)).decode(),
                key=base64.b64encode(
                    root_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                ).decode(),
            )
        )
        yaml.dump(data, outfile, default_flow_style=False)
