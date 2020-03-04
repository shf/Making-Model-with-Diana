#!/bin/sh
###
###  Shell script for submission of Diana batchjob using SLURM
###
###  LAST MODIFIED :: 20160525 Shayan Fahimi
###
###  To make it work for other users: Replace email address
###
###  Insert estimated time and analysis/analyses to be run on marked spots below
###
### ================================================================
###
###
### Mail on abort,begin and end
#SBATCH --mail-type=all
### Set your mail address
#SBATCH --mail-user "your-email"

### Insert estimated time here!
### Format is hh:mm:ss
#####################################
#SBATCH -t 30:00:00
#####################################

### Request 1 node and 16 processors on each node
#SBATCH -N 1
#SBATCH -n 1

### Specify project
#SBATCH -A C3SE503-13-1

### Request partition Glenn
#SBATCH -p cbi

### Set job name (should be the same as script file)
#SBATCH -J UNIQATotal

### copy files
cp -p -r /c3se/users/fahimi/Glenn/UNIQA/* $TMPDIR/
cd $TMPDIR/

### Submit the program
/c3se/apps/Common/Diana/hasplm/usr/sbin/hasplmd -l 4 -s
sleep 10

source $SLURM_SUBMIT_DIR/Makemac100
source $SLURM_SUBMIT_DIR/usrdialogin100
module load intel-compilers/14.0/080 
ifort -shared -fexceptions -ftz -i8 -r8 -fPIC -O3 -o usrifc.so usrifc.f /c3se/apps/Common/Diana/100/lib/liblbfl51.so /c3se/apps/Common/Diana/100/lib/liblber50.so  

###  Insert analysis/analyses to be run here! No &-sign at the end.
######################################################
python runOnCluster.py
#####################################################

### move files back to the directory from which this script was submitted

cd $SLURM_SUBMIT_DIR
# End of script