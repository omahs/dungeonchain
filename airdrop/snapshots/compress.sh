# sh snapshots/compress.sh
cd snapshots

mkdir -p ../archive

SFILE=cosmos_delegators.json && tar -czvf ../archive/$SFILE.tar.gz $SFILE # after running reduce_cosmos_delegators_minimum.py
SFILE=crytpodungeon.json && tar -czvf ../archive/$SFILE.tar.gz $SFILE
SFILE=juno_delegators.json && tar -czvf ../archive/$SFILE.tar.gz $SFILE
SFILE=mad_sci_osmo.json && tar -czvf ../archive/$SFILE.tar.gz $SFILE
SFILE=mad_sci_stars.json && tar -czvf ../archive/$SFILE.tar.gz $SFILE
SFILE=streamswap_osmosis.csv && tar -czvf ../archive/$SFILE.tar.gz $SFILE