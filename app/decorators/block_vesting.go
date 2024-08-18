package decorators

import (
	"context"
	"fmt"

	vestingtypes "github.com/cosmos/cosmos-sdk/x/auth/vesting/types"
	stakingtypes "github.com/cosmos/cosmos-sdk/x/staking/types"

	sdk "github.com/cosmos/cosmos-sdk/types"
)

type AuthAccKeeperI interface {
	GetAccount(ctx context.Context, addr sdk.AccAddress) sdk.AccountI
}

type MsgStakingVestingDeny struct {
	AuthKeeper AuthAccKeeperI
}

func NewMsgStakingVestingDeny(ak AuthAccKeeperI) MsgStakingVestingDeny {
	return MsgStakingVestingDeny{
		AuthKeeper: ak,
	}
}

// AnteHandle performs an AnteHandler check that returns an error if the tx contains a message that is not allowed
func (mfd MsgStakingVestingDeny) AnteHandle(ctx sdk.Context, tx sdk.Tx, simulate bool, next sdk.AnteHandler) (newCtx sdk.Context, err error) {
	if err := mfd.VestingAccountTriesToStake(ctx, tx.GetMsgs()); err != nil {
		currHeight := ctx.BlockHeight()
		return ctx, fmt.Errorf("tx contains unsupported message types at height %d. %w", currHeight, err)
	}

	return next(ctx, tx, simulate)
}

// block from delegating with vesting accounts.
func (mfd MsgStakingVestingDeny) VestingAccountTriesToStake(ctx sdk.Context, msgs []sdk.Msg) error {
	for _, msg := range msgs {
		if m, ok := msg.(*stakingtypes.MsgDelegate); ok {
			addr, err := sdk.AccAddressFromBech32(m.DelegatorAddress)
			if err != nil {
				return fmt.Errorf("error decoding delegator address: %w", err)
			}

			// check if they are a vesting account
			acc := mfd.AuthKeeper.GetAccount(ctx, addr)

			// check if they are a vesting account
			if acc != nil {
				switch acc.(type) {
				case *vestingtypes.BaseVestingAccount,
					*vestingtypes.DelayedVestingAccount,
					*vestingtypes.ContinuousVestingAccount,
					*vestingtypes.PeriodicVestingAccount:
					// *vestingtypes.PermanentLockedAccount, // this account is specifically for delegations only in the SDK.
					return fmt.Errorf("vesting accounts cannot delegate tokens: %s", addr)
				}
			}

		}
	}

	return nil
}
