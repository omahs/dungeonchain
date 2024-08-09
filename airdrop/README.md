# Dragon Airdrop

## Chain Groups
* ATOM Stakers
    - Minimum: 50 ATOM total staked (e.g. 10 to 5 validators, 50 to 1 validator, or any combination)
    - Excludes centralized exchanges
* [Crypto Dungeon JUNO Delegators](https://www.mintscan.io/juno/validators/junovaloper13x4pynlp86prhcmtns742kgsgu7pjtzjeknkwx) (52.36JUNO -> 1 ATOM conversion *($0.1207 / JUNO @ ATOM $6.32)*)


## Multipliers
* 2x - [Crypto Dungeon ATOM Delegators](https://www.mintscan.io/cosmos/validators/cosmosvaloper13x4pynlp86prhcmtns742kgsgu7pjtzj4djh7s)
* 2x - [OG Crypto Dungeon NFT Holders](https://www.stargaze.zone/m/cryptodungeon/tokens)
* 2x - Mad Scientist Holders (Stargaze & osmo)

## Stake Tiers
<!-- Holding 51-199 still is only the 50 group -->
- 50 $ATOM = 1 SHARE
- 200 $ATOM = 3 SHARES
- 1,000 $ATOM = 5 SHARES

> Max Share cap with multipliers: 40

---

# Snapshots

## Chain
- Cosmos Hub: 21383635
- Juno: 18100607

## NFTs
Snapshot Tool: [stargaze-nft-snapshots](https://github.com/Reecepbcups/stargaze-nft-snapshots)

- Crypto Dungeon
    - Stargaze: 2024-07-21 19:14:09
- Mad Scientist
    - Osmosis: 2024-07-21 19:16:42
    - Stargaze: 2024-07-21 19:16:42


## Share Conversions

Total Dragon being Airdroped: 99,940,890 DRAGON

1 SHARE = 245 DRAGON

| Wallets    | Shares |
| -------- | ------- |
| 2  | 40    |
| 22 | 20    |
| 19 | 12    |
| 249 | 10    |
| 3  | 8     |
| 529 | 6     |
| 13911 | 5     |
| 14 | 4     |
| 41794 | 3     |
| 1260 | 2     |
| 174104 | 1     |

---

Osmosis Streamswap

100m tokens for sale (ssdragon), which is then to be snapshotted after the stream swap. This is required since the team wants to stream before the chain launch (chicken and egg problem).

```bash
export OSMOSISD_NODE=https://osmosis-rpc.polkachu.com:443
git checkout v25.2.0 # osmosis

osmosisd tx tokenfactory create-denom ussdragon --from reece-main --gas=auto --gas-adjustment=1.3 --chain-id=osmosis-1 --fees=5000uosmo --yes
# osmosisd q tx B84E15D9CD3331DE244461C6F6CD6179D2BC9282AFA65DCCE37B1739240A3AAB

osmosisd q tokenfactory denoms-from-creator osmo10r39fueph9fq7a6lgswu4zdsg8t3gxlqyhl56p
# denoms:
# - factory/osmo10r39fueph9fq7a6lgswu4zdsg8t3gxlqyhl56p/ussdragon

# Mint 100m ssdragon = `100m * 10**6` to the CryptoDungeon account
#  (cosmos uses 6 decimals by default for fractions of a token)
osmosisd tx tokenfactory mint 100000000000000factory/osmo10r39fueph9fq7a6lgswu4zdsg8t3gxlqyhl56p/ussdragon osmo13x4pynlp86prhcmtns742kgsgu7pjtzjcz4jy3 --from=reece-main --gas-adjustment=1.3 --chain-id=osmosis-1 --fees=5000uosmo --yes
osmosisd q tx F5A57B47C684873935E5B5B91F3841E0D73495E6E718120F9EC8000ECD5E1F5A

# updates admin to osmosis governance (i.e. never to be changed again)
osmosisd tx tokenfactory change-admin factory/osmo10r39fueph9fq7a6lgswu4zdsg8t3gxlqyhl56p/ussdragon $(osmosisd q auth module-account gov --output=json | jq -r .account.base_account.address) --from=reece-main --gas-adjustment=1.3 --chain-id=osmosis-1 --fees=5000uosmo --yes
osmosisd q tx F8868C7CE5738A921151A18F946021C695F98982EA89A4BE40C2A5C7BBA5686D
```