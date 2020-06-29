#!/bin/bash

my_file="$(readlink -e "$0")"
my_dir="$(dirname $my_file)"

source /etc/os-release
[[ "$ID" == 'rhel' ]] && release=".rhel"
kvers=$(cat $my_dir/../kernel_version${release}.info)

echo ${kvers}
