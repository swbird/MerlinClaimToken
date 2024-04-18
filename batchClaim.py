import requests
from eth_account import Account
from eth_account.messages import encode_defunct,SignableMessage,to_bytes,HexBytes, \
    encode_intended_validator #
from web3.auto import w3
from Utils import load_from_file_pro
def FromPrivateKeyToAddress(private_key):
    return Account.privateKeyToAccount(private_key)._address
def signMsg(pk):
    addr = w3.toChecksumAddress(FromPrivateKeyToAddress(pk))
    message = encode_defunct(text=f"(1/merlinchain.io): I agree to claim $MERL token to this address - {addr}")
    res = Account.sign_message(message, pk)
    signature = res.signature.hex()
    return signature

def claim(pk):
    addr = w3.toChecksumAddress(FromPrivateKeyToAddress(pk))
    url = 'https://bridge.merlinchain.io/api/v1/merl_claim'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Content-Type': "application/json",
        'Referer': 'https://merlin.meson.fi/'
    }
    signature = signMsg(pk)
    print(addr,signature)
    json = {"signature": signature, "address": addr,"chain": "EVM", "domain": "merlinchain.io",
            "to_address": addr,"term": 1}
    r = requests.post(url,json=json,headers=headers)
    print(addr, r.json())
    if r.json()['code']==0:
        with open('success.txt', 'a', encoding='utf-8') as file:
            file.write(f'{addr}----{r.json()['msg']}\n')


if __name__ == '__main__':
    addrs,secks = load_from_file_pro('你的文件名, 文件格式=>地址----0x私钥')
    for seck in secks:
        claim(seck)
