#!/bin/bash


while IFS="," read a b c d; do
	echo "$b, $c"
done < $1


