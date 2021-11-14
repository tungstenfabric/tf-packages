#!/bin/bash -e

my_file="$(readlink -e "$0")"
my_dir="$(dirname $my_file)"

source /etc/os-release
KERNEL_REPOSITORIES_RHEL8=${KERNEL_REPOSITORIES_RHEL8:-"--disablerepo=* --enablerepo=rhel-8-for-x86_64-baseos-eus-rpms"}
kvers=$($my_dir/get_kvers.sh)

for kver in $kvers; do
    echo "INFO: installing $kver for $ID $VERSION_ID"
    k_mmp_ver=$(echo "$kver" | awk -F '-' '{print $1}')
    packages=$(cat $my_dir/../kernel_dependencies.info | grep ^$k_mmp_ver | awk -F ":" '{print $2}')
    extra_repos='-q'
    if [[ "$ID" == "rhel" && "$k_mmp_ver" == "4.18.0" ]]; then
        extra_repos+=" ${KERNEL_REPOSITORIES_RHEL8}"
    fi
    echo "INFO: packages=$(echo $packages)"
    for package in $packages; do
        if ! rpm -q ${package}-${kver} 2>&1 > /dev/null ; then
            echo "INFO: installing package ${package}-${kver}"
            location=$(repoquery $extra_repos --location ${package}-${kver})
            echo "INFO: installing $location"
            sudo rpm -ivh --nodeps --noscripts --oldpackage $location
        fi
    done
done
