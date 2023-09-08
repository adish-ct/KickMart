import uuid


def generate_referal_code():
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code