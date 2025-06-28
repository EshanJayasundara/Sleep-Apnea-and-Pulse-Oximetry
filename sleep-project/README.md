## Usage

#### How to use:

1. `git clone https://github.com/EshanJayasundara/Sleep-Apnea-and-Pulse-Oximetry.git`
2. `cd sleep-project`
3. `pip install build`
4. `python -m build`
5. `pip install dist/sleepdataspo2-0.1.0-py3-none-any.whl`
6. `cd ../usage`
7. place `.env` (which contains `NSRR_TOKEN`) and `cert.pem` (which used to verify the identity of a server. Since we only download files we don't need a private key) files into `usage` folder.
8. `python -m sleepdataspo2.download_shhs -d shhs1 -s 200028 -e 200030`
9. `python -m sleepdataspo2.create_odi -p data/shhs/polysomnography/edfs/shhs1 -n ODI -s data`

#### Here’s why only server public key `cert.pem` is enough:

- The private key belongs only to the server (sleepdata.org) — it stays secret and is used internally to establish secure TLS connections.

- You only needs:

  - Server’s public certificates (to verify the server’s identity).
  - Your authentication token (to prove you have permission).

- All encryption/decryption for the connection happens automatically via TLS.

- You never handle or need the private key yourself.
