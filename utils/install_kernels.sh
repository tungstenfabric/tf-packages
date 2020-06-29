#!/bin/bash

my_file="$(readlink -e "$0")"
my_dir="$(dirname $my_file)"
KERNELS_REPOSITORY=${KERNELS_REPOSITORY:-}

if [[ -n "$KERNELS_REPOSITORY" ]]; then
    repoquery_opts="--disablerepo=* --enablerepo=$KERNELS_REPOSITORY"
fi

kvers=$($my_dir/get_kvers.sh)

for kver in $kvers; do
    mmp_ver=$(echo "$kver" | awk -F '-' '{print $1}')
    packages=$(cat $my_dir/../kernel_dependencies.info | grep ^$mmp_ver | awk -F ":" '{print $2}')
    for package in $packages; do
        if ! rpm -q ${package}-${kver} 2>&1 > /dev/null ; then
            sudo rpm -ivh --nodeps --noscripts $(repoquery $repoquery_opts --location ${package}-${kver})
        fi
    done
done
