from ecdsa import SigningKey, SECP256k1
import sha3
import re
import requests
from time import sleep
from datetime import datetime
TEST = False


def guess():
    keccak = sha3.keccak_256()

    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak.update(pub)
    address = keccak.hexdigest()[24:]
    print(datetime.now().isoformat(), flush=True)
    print("Private key:", priv.to_string().hex(), flush=True)
    print("Public key: ", pub.hex(), flush=True)
    print("Address:     0x" + address, flush=True)

    if TEST:
        address = "cc57c79d21f00ca45411871372522dd9739191ec"

    url = "https://www.etherchain.org/account/0x" + address
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    result = requests.get(url, headers=headers)
    content = result.content.decode("utf-8")
    m = re.search(r"<p class=\"mb-4\">(\d+) ETH</p>", content)
    if m:
        num = int(m.group(1))
        if num:
            print("found %d ETH" % num, flush=True)
            f = open("%s.eth" % priv.to_string().hex(), "w")
            f.write(address)
            f.close()
        else:
            print("no luck, 0 eth", flush=True)
    else:
        print("no match", flush=True)

while 1:
    guess()
    sleep(5)
