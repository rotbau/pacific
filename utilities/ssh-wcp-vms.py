#!/usr/bin/python
# Copyright (c) 2019 VMware, Inc.  All rights reserved. -- VMware Confidential
# Run on vCenter / chmod to executable
import binascii
from Crypto.Cipher import AES
import base64
import psycopg2
def decrypt(encryptedTextBase64, key):
    """
    decrypt tries to decrypt cipher text using AES CBC and in case of failure
    falls back to AES GCM (for backward comaptibility with older testbeds).
    New testbeds should be using AES CBC.
    """
    # Add padding as necessary.
    rem = len(encryptedTextBase64) % 4
    paddedEncryptedTextBase64 = encryptedTextBase64 + "="*rem
    encryptedText = base64.b64decode(paddedEncryptedTextBase64)
    try:
        plaintext = decryptCBC(encryptedText, key)
    except:
        plaintext = decryptGCM(encryptedText, key)
    return plaintext.decode()
def decryptCBC(encryptedText, key):
    # IV is the first block of ciphertext.
    iv = encryptedText[:AES.block_size]
    cipherText = encryptedText[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    paddedtext = cipher.decrypt(cipherText)
    # Remove PKCS7 padding.
    padding = paddedtext[-paddedtext[-1]:]
    if padding != padding[-1:] * padding[-1]:
        raise ValueError("Incorrect padding!")
    return paddedtext[:-len(padding)]
def decryptGCM(encryptedText, key):
    # Nonce length is 12 (Source: https://golang.org/src/crypto/cipher/gcm.go
    # [line 150]).
    nonceLength = 12
    nonce = encryptedText[:nonceLength]
    # GCM tag size is 16 bytes
    # (Source: https://golang.org/src/crypto/cipher/gcm.go).
    cipherText = encryptedText[nonceLength:-16]
    gcmTag = encryptedText[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(cipherText, gcmTag)
def main():
    # Read secret key.
    with open("/etc/vmware/wcp/keyForCryptography.dat", "rb") as f:
        key = f.read()
        print ("Read key from file\n")
    # Read pwd from DB.
    with open("/etc/vmware/wcp/.pgpass", "r") as f:
         for line in f:
             if line.find("wcpuser") >= 0:
                 fRead = line.rstrip()
                 break
    connectionInfo = fRead.split(":")
    conn = psycopg2.connect(database=connectionInfo[2], user=connectionInfo[3],
                            password=connectionInfo[4], host=connectionInfo[0],
                            port=connectionInfo[1])
    print ("Connected to PSQL\n")
    cur = conn.cursor()
    res = cur.execute(
        '''select cluster, master_mgmt_ip, password from cluster_db_configs''')
    rows = cur.fetchall()
    for row in rows:
        pt = decrypt(row[2], key)
        print("Cluster: %s" % row[0])
        print("IP: %s" % row[1])
        print("PWD: %s" % pt)
        print("-" * 60 + "\n")
if __name__ == '__main__':
    main()
