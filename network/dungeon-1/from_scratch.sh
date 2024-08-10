# Takes a default genesis and creates a new modified genesis file.
#
# sh network/dungeon-1/from_scratch.sh
#

CHAIN_ID=dungeon-1

make install

export HOME_DIR=$(eval echo "${HOME_DIR:-"~/.dungeonchain"}")

rm -rf $HOME_DIR && echo "Removed $HOME_DIR"

dungeond init moniker --chain-id=$CHAIN_ID --default-denom=udgn --home $HOME_DIR

update_genesis () {
    cat $HOME_DIR/config/genesis.json | jq "$1" > $HOME_DIR/config/tmp_genesis.json && mv $HOME_DIR/config/tmp_genesis.json $HOME_DIR/config/genesis.json
}

update_genesis '.app_version="1.0.0"'

update_genesis '.consensus["params"]["block"]["max_gas"]="-1"'
update_genesis '.consensus["params"]["abci"]["vote_extensions_enable_height"]="1"'

# auth
update_genesis '.app_state["auth"]["params"]["max_memo_characters"]="512"'

update_genesis '.app_state["bank"]["denom_metadata"]=[
        {
            "base": "udgn",
            "denom_units": [
            {
                "aliases": [],
                "denom": "udgn",
                "exponent": 0
            },
            {
                "aliases": [],
                "denom": "DGN",
                "exponent": 6
            }
            ],
            "description": "Denom metadata for Dungeon Token (udgn)",
            "display": "DGN",
            "name": "DGN",
            "symbol": "DGN"
        }
]'

update_genesis '.app_state["crisis"]["constant_fee"]={"denom": "udgn","amount": "1000000000"}'

update_genesis '.app_state["distribution"]["params"]["community_tax"]="0.025000000000000000"' # 2.5%

update_genesis '.app_state["gov"]["params"]["min_deposit"]=[{"denom":"udgn","amount":"100000000"}]'
update_genesis '.app_state["gov"]["params"]["max_deposit_period"]="259200s"'
update_genesis '.app_state["gov"]["params"]["voting_period"]="259200s"'
update_genesis '.app_state["gov"]["params"]["expedited_min_deposit"]=[{"denom":"udgn","amount":"1000000000"}]'
update_genesis '.app_state["gov"]["params"]["min_deposit_ratio"]="0.100000000000000000"' # 10%

update_genesis '.app_state["mint"]["minter"]["inflation"]="0.100000000000000000"'
update_genesis '.app_state["mint"]["minter"]["annual_provisions"]="0.000000000000000000"'
update_genesis '.app_state["mint"]["params"]["mint_denom"]="udgn"'
update_genesis '.app_state["mint"]["params"]["inflation_rate_change"]="0.000000000000000000"'
update_genesis '.app_state["mint"]["params"]["inflation_max"]="0.100000000000000000"'
update_genesis '.app_state["mint"]["params"]["inflation_min"]="0.100000000000000000"'
update_genesis '.app_state["mint"]["params"]["blocks_per_year"]="18934560"' # 2s blocks (( 6s blocks = 6311520 per year ))

update_genesis '.app_state["slashing"]["params"]["signed_blocks_window"]="30000"'
update_genesis '.app_state["slashing"]["params"]["min_signed_per_window"]="0.010000000000000000"'
update_genesis '.app_state["slashing"]["params"]["downtime_jail_duration"]="60s"'
update_genesis '.app_state["slashing"]["params"]["slash_fraction_double_sign"]="0.000000000000000000"' # no need to slash delegators, ATOM Will slash
update_genesis '.app_state["slashing"]["params"]["slash_fraction_downtime"]="0.000000000000000000"'

update_genesis '.app_state["staking"]["params"]["bond_denom"]="udgn"' # leaving unbonding time at 1814400s (21 days)
update_genesis '.app_state["staking"]["params"]["min_commission_rate"]="0.000000000000000000"' # TODO:
update_genesis '.app_state["staking"]["params"]["max_validators"]="20"' # 0%?

update_genesis '.app_state["tokenfactory"]["params"]["denom_creation_fee"]=[]'
update_genesis '.app_state["tokenfactory"]["params"]["denom_creation_gas_consume"]="250000"'

update_genesis '.app_state["wasm"]["params"]["code_upload_access"]["permission"]="AnyOfAddresses"'
update_genesis '.app_state["wasm"]["params"]["instantiate_default_permission"]="AnyOfAddresses"'
update_genesis '.app_state["wasm"]["params"]["code_upload_access"]["addresses"]=["dungeon13gd97ke6erejqk2p050xkpc63jhtujre26s0gg"]' # TODO: this is currently lee, need a team wallet / multisig?

# TODO: ics params? (check with hypha)
update_genesis '.app_state["ccvconsumer"]["params"]["enabled"]=true'
update_genesis '.app_state["ccvconsumer"]["params"]["blocks_per_distribution_transmission"]="3000"' # since 3x faster blocks

## === GENESIS ACCOUNTS ===

# base / core accounts for the operations of this chain.
dungeond genesis add-genesis-account dungeon13gd97ke6erejqk2p050xkpc63jhtujre26s0gg 1udgn --append # TODO: shared cosmwasm addr (currently lee)

## === GENESIS / INTERNAL DISTRIBUTION ===
# - Addresses from Lee, found in: https://github.com/CryptoDungeon/dungeonchain/pull/2
# converted to dragon1 prefix with https://bech32.scrtlabs.com/

# FOUNDERS
# - 1.8% of total supply each (1bn) = 18,000,000DGN tokens per founder
# - locked for 1 year
# - no staking / inflation rewards
# - Vesting End: Aug 30, 2025 -> https://www.epochconverter.com/
dungeond genesis add-genesis-account dungeon13gd97ke6erejqk2p050xkpc63jhtujre26s0gg 18000000000000udgn --vesting-amount 18000000000000udgn --vesting-end-time=1725027635 --append # Cyril
dungeond genesis add-genesis-account dungeon1z0nvmv57cqax4s6lssft9yhfn8ksxcf79vmagu 18000000000000udgn --vesting-amount 18000000000000udgn --vesting-end-time=1725027635 --append # Lee
dungeond genesis add-genesis-account dungeon10dx7clngek0ya05nzgx5sd2cmlszltfa2c69qs 18000000000000udgn --vesting-amount 18000000000000udgn --vesting-end-time=1725027635 --append # Brad
dungeond genesis add-genesis-account dungeon1mzp9lhpjl8ndppzmuzh7c5zdjha597yes44qch 18000000000000udgn --vesting-amount 18000000000000udgn --vesting-end-time=1725027635 --append # Sanju
dungeond genesis add-genesis-account dungeon1ggasywhgu0yjg6jmgrv38sr75gu37c6cv2mfu9 18000000000000udgn --vesting-amount 18000000000000udgn --vesting-end-time=1725027635 --append # Josh
dungeond genesis add-genesis-account dungeon1g048ed4sh35v9hr6mlpe27fv57gq2g27fev8e3 18000000000000udgn --vesting-amount 18000000000000udgn --vesting-end-time=1725027635 --append # John
dungeond genesis add-genesis-account dungeon1ejacr05zf89226xfly8tn6hxafs3mwfajc00hu 18000000000000udgn --vesting-amount 18000000000000udgn --vesting-end-time=1725027635 --append # Donoven

# PARTNERS
# 0.5% of total supply (1bn) = 5,000,000DGN tokens per partner
dungeond genesis add-genesis-account dungeon17dj9ht0kp7a2gdq3l9jm2wyfzt8stw6nhucfrv 5000000000000udgn --vesting-amount 5000000000000udgn --vesting-end-time=1725027635 --append # Unknown

# FRIENDS AND FAMILY
# 0.25% of total supply each (1bn) = 2,500,000DGN tokens per person
dungeond genesis add-genesis-account dungeon12h772nnaz4249s4sz5p5a6we9qz583kypyyhh0 2500000000000udgn --vesting-amount 2500000000000udgn --vesting-end-time=1725027635 --append # Eric(Astro Vault)
dungeond genesis add-genesis-account dungeon1e8238v24qccht9mqc2w0r4luq462yxtt47evk4 2500000000000udgn --vesting-amount 2500000000000udgn --vesting-end-time=1725027635 --append # Vlad(Posthuman)
dungeond genesis add-genesis-account dungeon1fs67g6a7jdf4u6lkhyuwwlyyf9dw8ljtynhhpj 2500000000000udgn --vesting-amount 2500000000000udgn --vesting-end-time=1725027635 --append # Mike(Cybernetics)
dungeond genesis add-genesis-account dungeon1s6jjyxxmwx8jns4ye0yf92tdyq8cs8qsyydl6m 2500000000000udgn --vesting-amount 2500000000000udgn --vesting-end-time=1725027635 --append # Stoner
dungeond genesis add-genesis-account dungeon1mk2yasfjljrvrxrjwj5823xh6lctkjc990zuea 2500000000000udgn --vesting-amount 2500000000000udgn --vesting-end-time=1725027635 --append # Cosmos news
dungeond genesis add-genesis-account dungeon1zxg7695uplngjylndt46xms77v9lyxx8fm6fxy 2500000000000udgn --vesting-amount 2500000000000udgn --vesting-end-time=1725027635 --append # Cryptotank

# TODO: run the airdrop/genesis_builder.sh script here (airdrop)

# iterate through the gentx directory, print the files
# https://github.com/strangelove-ventures/bech32cli
for filename in network/dungeon-1/gentx/*.json; do
    echo "Processing $filename"
    addr=`cat $filename | jq -r .body.messages[0].validator_address | xargs -I {} bech32 transform {} dragon`
    raw_coin=`cat $filename | jq -r .body.messages[0].value` # { "denom": "udgn", "amount": "1000000" }
    coin=$(echo $raw_coin | jq -r '.amount + .denom') # make coin = 1000000udgn
    dungeond genesis add-genesis-account $addr $coin --append
done
dungeond genesis collect-gentxs --gentx-dir network/dungeon-1/gentx --home $HOME_DIR

cp $HOME_DIR/config/genesis.json ./network/$CHAIN_ID/genesis.json

dungeond genesis validate