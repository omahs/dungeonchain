# open final allocations, iterate, and build the genesis builder
# python3 convert_final_to_script.py
import json

from atypes import address_convert

with open("FINAL_ALLOCATION.json", "r") as f:
    airdrop_allocations = json.load(f)

WALLET_PREFIX: str = "dragon"

class Allocation:
    def __init__(self, address: str, udragon_allocation: int):
        self.address = address_convert(address, WALLET_PREFIX)
        self.udragon_allocation = udragon_allocation

    @staticmethod
    def from_json(json: dict):
        return Allocation(
            json["address"],
            int(json["dragon"]) * 1_000_000, # udragon
        )


# iterate airdrop_allocations

genesis_builder = []

for u in airdrop_allocations:
    alloc = Allocation.from_json(u)

    genesis_builder.append(
        f"dragond genesis add-genesis-account {alloc.address} {alloc.udragon_allocation}udragon --append"
    )

# dump genesis_builder to a file named genesis_builder.sh
with open("genesis_builder.sh", "w") as f:
    f.write("\n".join(genesis_builder))
