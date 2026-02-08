import uuid

base_key_ = "photon-key-s3p8-proj="

def secret_key():
    return base_key_ + str(uuid.uuid4())

# print(secret_key())