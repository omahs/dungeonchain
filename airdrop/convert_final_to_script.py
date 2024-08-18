# open final allocations, iterate, and build the genesis builder
# python3 convert_final_to_script.py
import json

from atypes import address_convert

with open("FINAL_ALLOCATION.json", "r") as f:
    airdrop_allocations = json.load(f)

WALLET_PREFIX: str = "dungeon"

class Allocation:
    def __init__(self, address: str, udragon_allocation: int):
        self.address = address_convert(address, WALLET_PREFIX)
        self.udragon_allocation = udragon_allocation

    # quicker than creating new instances every time
    @staticmethod
    def from_json(json: dict, baseAllocObj: "Allocation" = None) -> "Allocation":
        if baseAllocObj is not None:
            baseAllocObj.address = json["address"]
            baseAllocObj.udragon_allocation = int(json["dragon"]) * 1_000_000
            return baseAllocObj

        return Allocation(
            json["address"],
            int(json["dragon"]) * 1_000_000, # udragon
        )


# iterate airdrop_allocations

genesis_builder = []

base_alloc = Allocation("cosmos10r39fueph9fq7a6lgswu4zdsg8t3gxlqvvvyvn", 0)
for idx, u in enumerate(airdrop_allocations):
    alloc = Allocation.from_json(u, base_alloc)

    genesis_builder.append(
        f"dungeond genesis add-genesis-account {alloc.address} {alloc.udragon_allocation}udragon --append"
    )

    if idx % 1_000 == 0:
        print(f"Processed {idx:,} allocations.")

        genesis_builder.append(
            f"echo 'Processed {idx:,} allocations.'"
        )

# dump genesis_builder to a file named genesis_builder.sh
with open("genesis_builder.sh", "w") as f:
    f.write("\n".join(genesis_builder))
    print("Built the genesis builder.")
