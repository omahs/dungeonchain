# The sdk is to fucking slow to do this... go figures
# TODO: Instead use `make install && dungeond fast-add-genesis-account ./airdrop/FINAL_ALLOCATION.json` which is a batch genesis wrapper.
# I will look into getting this upstreamed. Speeds up the genesis add by ~99.9999% (days of time to seconds)

# # open final allocations, iterate, and build the genesis builder
# # python3 convert_final_to_script.py
# import json

# from atypes import address_convert

# with open("FINAL_ALLOCATION.json", "r") as f:
#     airdrop_allocations = json.load(f)

# WALLET_PREFIX: str = "dungeon"

# class Allocation:
#     def __init__(self, address: str, udragon_allocation: int):
#         self.address = address_convert(address, WALLET_PREFIX)
#         self.udragon_allocation = udragon_allocation

#     # quicker than creating new instances every time
#     @staticmethod
#     def from_json(json: dict) -> "Allocation":
#         return Allocation(
#             json["address"],
#             int(json["dragon"]) * 1_000_000, # udragon
#         )


# # iterate airdrop_allocations

# genesis_builder = []
# for idx, u in enumerate(airdrop_allocations):
#     alloc = Allocation.from_json(u)

#     genesis_builder.append(
#         f"dungeond fast-add-genesis-account {alloc.address} {alloc.udragon_allocation}udragon --append"
#     )

#     if idx % 100 == 0:
#         print(f"Processed {idx:,} allocations.")

#         genesis_builder.append(
#             f"echo 'Processed {idx:,} allocations.'"
#         )

# # dump genesis_builder to a file named genesis_builder.sh
# with open("genesis_builder.sh", "w") as f:
#     f.write("\n".join(genesis_builder))
#     print("Built the genesis builder.")
