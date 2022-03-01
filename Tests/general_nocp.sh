#!/bin/bash
PBNAME=$1
IMIN=$2
IMAX=$3
TIMEOUT=600
PADDING=1

cd ..
mkdir ./Results
mkdir ./Results/$PBNAME-nocp
mkdir ./Results/$PBNAME-nocp/Graphs
mkdir ./Results/$PBNAME-nocp/Output
mkdir ./Results/$PBNAME-nocp/SatInstances/
mkdir ./Results/$PBNAME-nocp/Stats
mkdir ./Results/$PBNAME-nocp/Traces

if [[ "$1" == "" || "$2" == "" || "$3" == "" ]]; then
	echo "Usage: domain imin imax"
	exit 1
fi

if [[ "$4" == "-pad" ]]; then
	SEQ1=$(seq -f "%02g" $IMIN $IMAX)
else
	SEQ1=$(seq $IMIN $IMAX)
fi

echo "$IMIN,$IMAX" > ./Results/$PBNAME/graph_data

for i in $SEQ1
do
	if [[ "$4" == "-pad" ]]; then
		SEQ2=$(seq -f "%02g" $i $IMAX)
	else
		SEQ2=$(seq $i $IMAX)
	fi

	for j in $SEQ2
	do
	echo "Running $j against $i"
	timeout $TIMEOUT python3 ./Isofinder/main.py ./Benchmarks/$PBNAME/domain.pddl ./Benchmarks/$PBNAME/pfile$j.pddl ./Benchmarks/$PBNAME/domain.pddl ./Benchmarks/$PBNAME/pfile$i.pddl --trace ./Results/$PBNAME-nocp/Stats/pfile$j--pfile$i.csv --output ./Results/$PBNAME-nocp/Output/pfile$j--pfile$i.hm --cnfpath ./Results/$PBNAME-nocp/SatInstances/pfile$j--pfile$i.cnf --touist --clean --no-cp | tee ./Results/$PBNAME-nocp/Traces/pfile$j--pfile$i
	rm ./Results/$PBNAME-nocp/SatInstances/pfile$j--pfile$i.cnf
	done
done
