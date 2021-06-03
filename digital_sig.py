import hashlib
import time

PRIVATE_SERVER_KEY = 42


def get_unique_signature(nombres, primer_ap, segundo_ap):
    my_hash = hashlib.sha256()
    my_hash.update(str(PRIVATE_SERVER_KEY).encode("utf-8"))
    my_hash.update(str(time.time()).encode("utf-8"))
    my_hash.update(nombres.encode("utf-8"))
    my_hash.update(primer_ap.encode("utf-8"))
    my_hash.update(segundo_ap.encode("utf-8"))

    digest = my_hash.hexdigest()

    formatted = "{}-{}-{}-{}-{}".format(digest[0:4],
                                        digest[4:8], digest[8:12], digest[12:16], digest[16:20])

    return formatted
