"""
- remove delegators with less than minimum (50ATOM staked)
- remove CEXs
"""

# python3 snapshots/reduce_cosmos_delegators_minimum.py

import json

# copy atypes to this dir for this script 1 off
from airdrop.atypes import Delegation, ReDelegation

FILE = "snapshots/cosmos_delegators.json"
REDELEGATE_FILE = "snapshots/cosmos_redelegations.json"
UPDATED = "snapshots/updated_cosmos_delegators.json"

MINIMUM = 50 * 1_000_000  # 1ATOM = 1,000,000 uatom


CENTRAL_EXCHANGES = {
    "cosmosvaloper1c4k24jzduc365kywrsvf5ujz4ya6mwympnc4en": "Coinbase",
    "cosmosvaloper18ruzecmqj9pv8ac0gvkgryuc7u004te9rh7w5s": "Binance Node",
    "cosmosvaloper1z8zjv3lntpwxua0rtpvgrcwl0nm0tltgpgs6l7": "Kraken",
    "cosmosvaloper156gqf9837u7d4c4678yt3rl4ls9c5vuursrrzf": "Binance Staking",
    "cosmosvaloper1yw5s259jkcg0jzmh7sce29uk0lqqw2ump7578p": "CEX.IO",
}

def main():
    total_staked: dict[str, int] = {}

    updated: list[Delegation] = []

    delegators: list[Delegation] = []
    fastdelegators: dict[str, list[Delegation]] = {}
    with open(FILE, "r") as f:
        delegators = Delegation.load_all(json.load(f))

    # just iterate, we are putting into fastdelegators anyways
    redelegators: list[ReDelegation] = []
    with open(REDELEGATE_FILE, "r") as f:
        redelegators = ReDelegation.load_all(json.load(f))

    # Merge all delegations into 1 group
    for d in delegators:
        if d.validator_address in CENTRAL_EXCHANGES:
            continue

        if d.delegator_address not in fastdelegators:
            fastdelegators[d.delegator_address] = []
        fastdelegators[d.delegator_address].append(d)


        if d.delegator_address not in total_staked:
            total_staked[d.delegator_address] = 0

        total_staked[d.delegator_address] += int(d.shares)

    # Merge all redelegations into 1 group (treat as standard delegators to the new dst validator)
    for r in redelegators:
        if r.validator_dst_address in CENTRAL_EXCHANGES:
            continue

        if r.delegator_address not in fastdelegators:
            fastdelegators[r.delegator_address] = []

        asDelegation = ReDelegation.convert_redelegation_to_delegation(r)
        fastdelegators[r.delegator_address].append(asDelegation)

        if d.delegator_address not in total_staked:
            total_staked[d.delegator_address] = 0

        total_staked[d.delegator_address] += int(d.shares)

    # iter total_staked and ignore any which have < MINIMUM (total)
    for addr, shares in total_staked.items():
        if shares < MINIMUM:
            continue

        for d in fastdelegators[addr]:
            updated.append(d)


    # save updated to a new file called updated_FILE
    with open(f"{UPDATED}", "w") as f:
        json.dump([d.to_json() for d in updated], f, indent=2)


if __name__ == "__main__":
    main()
    print('now rename the file to cosmos_delegators.json')