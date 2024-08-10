# pip install bech32 - https://pypi.org/project/bech32/
import bech32

CRYPTO_DUNGEON_VALIDATOR = "cosmosvaloper13x4pynlp86prhcmtns742kgsgu7pjtzj4djh7s"

def address_convert(address="", prefix="cosmos"):
    _, data = bech32.bech32_decode(address)
    return bech32.bech32_encode(prefix, data)


# {
#     "delegator_address": "cosmos1qqymhez0x480l90lxdhzhg5ee847xs2jdkgcp3",
#     "entries": [
#       {
#         "completion_time": "2024-06-07T19:44:48.204743724Z",
#         "creation_height": "20470888",
#         "initial_balance": "4200000",
#         "shares_dst": "4200000.000000000000000000",
#         "unbonding_id": "696429",
#         "unbonding_on_hold_ref_count": "1"
#       }
#     ],
#     "validator_src_address": "cosmosvaloper10wljxpl03053h9690apmyeakly3ylhejrucvtm",
#     "validator_dst_address": "cosmosvaloper1c4k24jzduc365kywrsvf5ujz4ya6mwympnc4en"
#   },

class ReDelegationEntry:
    def __init__(self, completion_time, creation_height, initial_balance, shares_dst, unbonding_id, unbonding_on_hold_ref_count):
        self.completion_time = completion_time
        self.creation_height = creation_height
        self.initial_balance = initial_balance
        self.shares_dst = shares_dst
        self.unbonding_id = unbonding_id
        self.unbonding_on_hold_ref_count = unbonding_on_hold_ref_count

    def __str__(self):
        return f"ReDelegationEntry: {self.completion_time} creation_height: {self.creation_height} initial_balance: {self.initial_balance} shares_dst: {self.shares_dst} unbonding_id: {self.unbonding_id} unbonding_on_hold_ref_count: {self.unbonding_on_hold_ref_count}"

    @staticmethod
    def from_json(json: dict) -> "ReDelegationEntry":
        return ReDelegationEntry(
            json["completion_time"],
            json["creation_height"],
            json["initial_balance"],
            json["shares_dst"],
            json["unbonding_id"],
            json["unbonding_on_hold_ref_count"],
        )

class ReDelegation:
    def __init__(self, delegator_address: str, validator_src_address: str, validator_dst_address: str, entries: list[ReDelegationEntry]):
        self.delegator_address = delegator_address
        self.validator_src_address = validator_src_address
        self.validator_dst_address = validator_dst_address
        self.entries = entries

    def __str__(self):
        return f"ReDelegation: {self.delegator_address} src: {self.validator_src_address} dst: {self.validator_dst_address} entries: {self.entries}"

    @staticmethod
    def from_json(json: dict) -> "ReDelegation":
        return ReDelegation(
            json["delegator_address"],
            json["validator_src_address"],
            json["validator_dst_address"],
            [ReDelegationEntry.from_json(e) for e in json["entries"]],
        )

    def to_json(self):
        return self.__dict__

    @staticmethod
    def load_all(json: list[dict]) -> list["ReDelegation"]:
        return [ReDelegation.from_json(j) for j in json]

    # just to keep types the same is nice
    @staticmethod
    def convert_redelegation_to_delegation(reDel: "ReDelegation") -> "Delegation":
        # sum up all enteries to the dst for a given val
        sharesSum = 0
        for e in reDel.entries:
            sharesSum += float(e.shares_dst)

        return Delegation(reDel.delegator_address, float(sharesSum), reDel.validator_dst_address, True)

class Delegation:
    def __init__(self, delegator_address: str, shares, validator_address: str, validator_bond: bool | str):
        if type(validator_bond) == str:
            validator_bond = bool(validator_bond)

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
