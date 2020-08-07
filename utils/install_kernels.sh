#!/bin/bash -x

my_file="$(readlink -e "$0")"
my_dir="$(dirname $my_file)"

source /etc/os-release
KERNEL_REPOSITORIES_RHEL8=${KERNEL_REPOSITORIES_RHEL8:-"--disablerepo=* --enablerepo=BaseOS"}
KVERS=$($my_dir/get_kvers.sh)

for KVER in $KVERS; do
    K_MMP_VER=$(echo "$KVER" | awk -F '-' '{print $1}')
    PACKAGES=$(cat $my_dir/../kernel_dependencies.info | grep ^$K_MMP_VER | awk -F ":" '{print $2}')
    if [[ "$ID" == "rhel" && "$K_MMP_VER" == "4.18.0" ]]; then
        REPOQUERY_OPTS="${KERNEL_REPOSITORIES_RHEL8}"
    else
        REPOQUERY_OPTS=''
    fi
    for PACKAGE in $PACKAGES; do
        if ! rpm -q ${PACKAGE}-${KVER} 2>&1 > /dev/null ; then
            sudo rpm -ivh --nodeps --noscripts $(repoquery $REPOQUERY_OPTS --location ${PACKAGE}-${KVER})
        fi
    done
done
