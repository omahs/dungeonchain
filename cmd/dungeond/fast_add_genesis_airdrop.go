package main

import (
	"encoding/json"
	"fmt"
	"os"

	"cosmossdk.io/core/address"
	"github.com/cosmos/cosmos-sdk/client"
	"github.com/cosmos/cosmos-sdk/client/flags"
	"github.com/cosmos/cosmos-sdk/codec"
	"github.com/cosmos/cosmos-sdk/server"
	sdk "github.com/cosmos/cosmos-sdk/types"
	"github.com/cosmos/cosmos-sdk/types/bech32"
	authtypes "github.com/cosmos/cosmos-sdk/x/auth/types"
	banktypes "github.com/cosmos/cosmos-sdk/x/bank/types"
	genutiltypes "github.com/cosmos/cosmos-sdk/x/genutil/types"
	"github.com/spf13/cobra"
)

const (
	flagAppendMode = "append"
	denom          = "udgn"
)

// [
// {
// "address": "cosmos10lhwra8pyu6j7q39prez3ytp584fw9asyged6v",
// "shares": 20,
// "dragon": 15204244.153386
//
//	},
//
// ]
type GenesisAccount struct {
	Address string  `json:"address"` // cosmos1 by default, we will convert at run time
	Shares  int     `json:"shares"`
	Dragon  float64 `json:"dragon"`
}

// NOTE: does not support vesting accounts or modules. Just standard accounts.
// You run this after you add your base / genesis modifications. i.e. vesting accounts, core team accounts, etc
func AddFastGenesisAccountCmd(defaultNodeHome string, addressCodec address.Codec) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "fast-add-genesis-account [/abs/file/path.json]",
		Short: "Loads in a JSON file for new genesis accounts. Always appends",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			clientCtx := client.GetClientContextFromCmd(cmd)
			serverCtx := server.GetServerContextFromCmd(cmd)
			config := serverCtx.Config

			config.SetRoot(clientCtx.HomeDir)

			// read the file from args[0]
			f, err := os.Open(args[0])
			if err != nil {
				return fmt.Errorf("failed to open file: %w", err)
			}
			defer f.Close()

			// parse the JSON into an array of GenesisAccount
			var accounts []GenesisAccount
			if err := json.NewDecoder(f).Decode(&accounts); err != nil {
				return fmt.Errorf("failed to decode JSON: %w", err)
			}

			genesisFileURL := config.GenesisFile()
			appState, appGenesis, err := genutiltypes.GenesisStateFromGenFile(genesisFileURL)
			if err != nil {
				return fmt.Errorf("failed to unmarshal genesis state: %w", err)
			}

			fmt.Printf("Adding %d accounts\n", len(accounts))
			alwaysAppend := true
			if err := BatchAddGenesisAccounts(clientCtx.Codec, alwaysAppend, appState, appGenesis, accounts, addressCodec); err != nil {
				return fmt.Errorf("failed to add genesis account: %w", err)
			}

			return ExportGenesisFile(appGenesis, genesisFileURL)
		},
	}

	cmd.Flags().String(flags.FlagHome, defaultNodeHome, "The application home directory")
	cmd.Flags().String(flags.FlagKeyringBackend, flags.DefaultKeyringBackend, "Select keyring's backend (os|file|kwallet|pass|test)")
	cmd.Flags().Bool(flagAppendMode, false, "append the coins to an account already in the genesis.json file")
	flags.AddQueryFlagsToCmd(cmd)

	return cmd
}

// Taken from the genutil.AddGenesisAccount in the SDK.
// This loads in the genesis state, updates the values within a map (for super fast modification)
// then verifies and saves it to state in 1 go. before: 100 accounts would take ~5 seconds.
// Now 250k accounts can be done in a few seconds.
func BatchAddGenesisAccounts(
	cdc codec.Codec,
	// accAddr sdk.AccAddress,
	appendAcct bool,
	// amountStr, vestingAmtStr string,
	// vestingStart, vestingEnd int64,
	// moduleName string,
	appState map[string]json.RawMessage,
	appGenesis *genutiltypes.AppGenesis,
	accounts []GenesisAccount,
	addressCodec address.Codec,
) error {

	// load genesis state as caches
	authGenState := authtypes.GetGenesisStateFromAppState(cdc, appState)
	bankGenState := banktypes.GetGenesisStateFromAppState(cdc, appState)

	// this is an array, too slow.
	accs, err := authtypes.UnpackAccounts(authGenState.Accounts)
	if err != nil {
		return fmt.Errorf("failed to get accounts from any: %w", err)
	}

	// cosmos1 -> balance
	inState := make(map[string]banktypes.Balance)
	newlyAddedCoins := sdk.NewCoins() // for the supply

	// load all accounts currently in the genesis state
	for _, acc := range accs {
		for _, balance := range bankGenState.GetBalances() {
			if balance.Address == acc.GetAddress().String() {
				inState[acc.GetAddress().String()] = balance
			}
		}
	}

	// iterate accounts
	for i, acc := range accounts {
		_, bz, err := bech32.DecodeAndConvert(acc.Address)
		if err != nil {
			return fmt.Errorf("failed to decode and convert address: %w", err)
		}

		// convert acc.Address from cosmos to dungeon
		addStr, err := bech32.ConvertAndEncode("dungeon", bz)
		if err != nil {
			return fmt.Errorf("failed to convert address: %w", err)
		}

		addrBz, err := addressCodec.StringToBytes(addStr)
		if err != nil {
			panic(fmt.Errorf("failed to parse address from arg[0]: %w", err))
		}

		coinStr := fmt.Sprintf("%d%s", int64(acc.Dragon*1_000_000), denom)
		coins, err := sdk.ParseCoinsNormalized(coinStr)
		if err != nil {
			return fmt.Errorf("failed to parse coins: %w", err)
		}

		if i%1_000 == 0 {
			fmt.Printf("Adding account %d\n", i)
		}

		// if account is in inState, we will just append it
		if _, ok := inState[addStr]; ok {
			// fmt.Printf("Account %s already exists, updating bank gen state\n", addStr)
			for idx, acc := range bankGenState.Balances {
				if acc.Address != addStr {
					continue
				}

				updatedCoins := acc.Coins.Add(coins...)
				bankGenState.Balances[idx] = banktypes.Balance{Address: addStr, Coins: updatedCoins.Sort()}
				break
			}
		} else {
			balances := banktypes.Balance{Address: addStr, Coins: coins.Sort()}
			genAccount := authtypes.NewBaseAccount(addrBz, nil, 0, 0)

			if err := genAccount.Validate(); err != nil {
				return fmt.Errorf("failed to validate new genesis account: %w", err)
			}

			// does not exist, new
			// Add the new account to the set of genesis accounts and sanitize the accounts afterwards.
			accs = append(accs, genAccount)
			bankGenState.Balances = append(bankGenState.Balances, balances)
		}

		newlyAddedCoins = newlyAddedCoins.Add(coins...)
	}

	// auth accounts
	accs = authtypes.SanitizeGenesisAccounts(accs)

	genAccs, err := authtypes.PackAccounts(accs)
	if err != nil {
		return fmt.Errorf("failed to convert accounts into any's: %w", err)
	}
	authGenState.Accounts = genAccs

	authGenStateBz, err := cdc.MarshalJSON(&authGenState)
	if err != nil {
		return fmt.Errorf("failed to marshal auth genesis state: %w", err)
	}
	appState[authtypes.ModuleName] = authGenStateBz

	//  bank
	bankGenState.Balances = banktypes.SanitizeGenesisBalances(bankGenState.Balances)

	bankGenState.Supply = bankGenState.Supply.Add(newlyAddedCoins...)

	bankGenStateBz, err := cdc.MarshalJSON(bankGenState)
	if err != nil {
		return fmt.Errorf("failed to marshal bank genesis state: %w", err)
	}
	appState[banktypes.ModuleName] = bankGenStateBz

	appStateJSON, err := json.Marshal(appState)
	if err != nil {
		return fmt.Errorf("failed to marshal application genesis state: %w", err)
	}

	appGenesis.AppState = appStateJSON
	return nil
}

// ExportGenesisFile creates and writes the genesis configuration to disk. An
// error is returned if building or writing the configuration to file fails.
func ExportGenesisFile(genesis *genutiltypes.AppGenesis, genFile string) error {
	if err := genesis.ValidateAndComplete(); err != nil {
		return err
	}

	return genesis.SaveAs(genFile)
}
