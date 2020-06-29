#!/bin/bash

my_file="$(readlink -e "$0")"
my_dir="$(dirname $my_file)"

kvers=$(cat $my_dir/../kernel_dependencies.info | awk -F ":" '{print $1}')

echo ${kvers}
