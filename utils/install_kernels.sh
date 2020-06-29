#!/bin/bash

my_file="$(readlink -e "$0")"
my_dir="$(dirname $my_file)"

source /etc/os-release

kvers=$($my_dir/get_kvers.sh)

for kver in $kvers; do
    k_mmp_ver=$(echo "$kver" | awk -F '-' '{print $1}')
    packages=$(cat $my_dir/../kernel_dependencies.info | grep ^$k_mmp_ver | awk -F ":" '{print $2}')
    if [[ "$ID" == "rhel" && "$packages" =~ "kernel-core" ]]; then
        repoquery_opts="--disablerepo=* --enablerepo=BaseOS"
    else
        repoquery_opts=''
    fi
    for package in $packages; do
        if ! rpm -q ${package}-${kver} 2>&1 > /dev/null ; then
            sudo rpm -ivh --nodeps --noscripts $(repoquery $repoquery_opts --location ${package}-${kver})
        fi
    done
done
