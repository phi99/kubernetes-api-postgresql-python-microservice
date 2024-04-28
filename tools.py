import hashlib

def _hash(passw:str):
    return (hashlib.sha256(passw.encode())).hexdigest()

def passwcheck(targetpw, hashedpw):
    targetpw_h=_hash(targetpw)
    print(targetpw_h)
    return targetpw_h==hashedpw
