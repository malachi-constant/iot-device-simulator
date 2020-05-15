#!/bin/bash
export AWS_DEFAULT_REGION=us-east-1
BATCH_NUMBER=100
SIMULATIONS="${1}"
if [ -z "$SIMULATIONS" ]
then
  echo [*] You must specify a number of simulations! Exiting...
  exit
fi
if [ $SIMULATIONS -gt 10000 ] || [ $SIMULATIONS -lt 5 ]
then
  echo [*] Simulation amount must be between 5:10000 Exiting...
  exit
fi

echo '[*] Running' $SIMULATIONS 'simulations!'
for (( i = 1; i <= $SIMULATIONS; i++ ))
do
  if ! ((  $i % $BATCH_NUMBER ))
  then
    echo '[*] Running next ' $BATCH_NUMBER ' simulations in five seconds...'
    sleep 5
  fi
  OUTPUT=$(python3 clevertime-sim.py --region us-east-1 --iot-endpoint a28t31er3mx77a-ats.iot.us-east-1.amazonaws.com --simulation-table simulation-table --iot-topic connectedcar/trip/test > /tmp/$i.log ) & done


echo '[*] Started all simulations successfully'
