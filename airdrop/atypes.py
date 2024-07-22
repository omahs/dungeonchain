# pip install bech32 - https://pypi.org/project/bech32/
import bech32

CRYPTO_DUNGEON_VALIDATOR = "cosmosvaloper13x4pynlp86prhcmtns742kgsgu7pjtzj4djh7s"

def address_convert(address="", prefix="cosmos"):
    _, data = bech32.bech32_decode(address)
    return bech32.bech32_encode(prefix, data)


class Delegation:
    def __init__(self, delegator_address, shares, validator_address, validator_bond):
        self.delegator_address = delegator_address
        self.shares: float = shares
        self.validator_address = validator_address
        self.validator_bond = validator_bond
        self.is_crypto_dungeon_delegator = False

    def __str__(self):
        return f"Delegator: {self.delegator_address} shares: {self.shares} validator: {self.validator_address} bond: {self.validator_bond}"

    def from_json(self, json: dict):
        d = Delegation(
            json["delegator_address"],
            float(json["shares"]),
            json["validator_address"],
            json.get("validator_bond", ""),
        )
        d.is_crypto_dungeon_delegator = json["validator_address"] == CRYPTO_DUNGEON_VALIDATOR
        return d

    def to_json(self):
        return self.__dict__

    @staticmethod
    def load_all(json: list[dict]) -> list["Delegation"]:
        return [Delegation.from_json(None, j) for j in json]


class User:
    address: str  # cosmos address
    shares: int = 0
    # This is JUST for users to see, calculation is done before.
    mult: int = 1

    def __init__(self, address: str, shares_amt: int, mult: int = 1):
        self.address = address
        self.shares = shares_amt
        self.mult = mult

    def get_allocation(self) -> int:
        return self.shares * 245 # hardcoded per share amount, ref: (100m tokens / 407922 shares = 245)

    def get_total_amt(self) -> int:
        return self.shares * self.multiple
