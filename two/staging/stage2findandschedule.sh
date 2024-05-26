# This script is useful if you stopped stage2wstaging1.sh before all already downloaded html.zst files were processed to reschedule them.
# Finds html.zst files that were modified more than 1 minute ago (presumable already downloaded) and simulates an rclone log message
# about them downloaded. 
# Redirect this to the corresponding FIFO to schedule their processing.
# Limitations: 1-minute heiristic will not work when downloading of a file stopped before finishing (e.g. rclone was restarted, or didn't 
# update the file for a while for some internal reasons).
#
LPATH=$1
find $LPATH -mmin +1 -name html.zst|sed -r 's!.*/([^/]+/html.zst).*!: \1: Copied (new)!' 

