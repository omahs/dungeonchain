# Instructions

Place chain exports in this directory (chains/)

---

# Juno

```sh
# Sync node up to height or download archive
mkdir -p chains/juno && lz4 -c -d chains/juno.tar.lz4  | tar -x -C chains/juno

# install junod v23.0.0

cd chains/juno
junod export --output-document=../juno_export.json --modules-to-export=staking

cd ../
rm -rf juno/

jq -r '.app_state.staking.delegations' juno_export.json > ../snapshots/juno_delegators.json
```

---

# Cosmos

```sh
# Sync node up to height or download archive
mkdir -p chains/cosmos && lz4 -c -d chains/cosmos.tar.lz4  | tar -x -C chains/cosmos

# install gaiad v17.3.0

cd chains/cosmos
gaiad export --output-document=../cosmos_export.json --modules-to-export=staking

cd ../
rm -rf cosmos/

jq -r '.app_state.staking.delegations' cosmos_export.json > ../snapshots/cosmos_delegators.json
```