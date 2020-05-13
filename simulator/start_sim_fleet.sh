#!/bin/bash

# Echo commands in the shell
set -e

# Set variables
ASG="${1}"
NUMBER_OF_SIMULATIONS="${2}"

if [ $NUMBER_OF_SIMULATIONS == "0" ]
then
 echo '[*] Turning off simulation fleet...'
 OUTPUT=$(aws autoscaling update-auto-scaling-group --auto-scaling-group-name $ASG --min-size 0 --max-size 0 --desired-capacity 0)
 echo '[*] Done. ASG set to 0'
 exit
fi

# Calculate Instances required for simulation
LOAD_RANGE=2000
INSTANCES_REQUIRED=$(( ($NUMBER_OF_SIMULATIONS - 1) / $LOAD_RANGE + 1))
echo '[*] Instances required for simulation: '$INSTANCES_REQUIRED

echo '[*] Turning on simulation fleet...'

OUTPUT=$(aws autoscaling update-auto-scaling-group --auto-scaling-group-name $ASG --min-size $INSTANCES_REQUIRED --max-size $INSTANCES_REQUIRED --desired-capacity $INSTANCES_REQUIRED)
echo '[*] Done. ASG set to '$INSTANCES_REQUIRED
