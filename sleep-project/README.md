## Usage

#### How to use:

1. `git clone <repo>`
2. `cd sleep-project`
3. `pip install build`
4. `python -m build`
5. `pip install dist/sleepdataspo2-0.1.0-py3-none-any.whl`
6. `cd ../usage`
7. place `.env` (which contains `NSRR_TOKEN`) and `cert.pem` (which used to verify the identity of the server. Since we only download files we don't need a private key) files into `usage` folder.
8. Use one of the following:

   ```bash
     python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -s 200504 -e 200505 -t 2
   ```

   or

   ```bash
   python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -l "200315 200317 200313" -t 3
   ```

#### Here’s why only server public key `cert.pem` is enough:

- The private key belongs only to the server (sleepdata.org) — it stays secret and is used internally to establish secure TLS connections.

- You only needs:

  - Server’s public certificates (to verify the server’s identity).
  - Your authentication token (to prove you have permission).

- All encryption/decryption for the connection happens automatically via TLS.

- You never handle or need the private key yourself.
