# Upload html.zst file to LUMI-O to free space
DIR=$1
OUT="lumi-o:stage2-htmls/$(basename $DIR)"

module purge
module load lumio

echo Uploading html.zst files from $DIR to $OUT
rclone copy --log-file $(basename $DIR).tolumio.log --log-format INFO --transfers 32  -P $DIR $OUT --include html.zst
