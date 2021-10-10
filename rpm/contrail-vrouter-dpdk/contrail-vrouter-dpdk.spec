%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%define     _contrailetc  /etc/contrail
%define     _distropkgdir %{_sbtop}tools/packages/rpm/%{name}

%if 0%{?_buildTag:1}
%define     _relstr %{_buildTag}
%else
%define     _relstr %(date -u +%y%m%d%H%M)
%endif

%if 0%{?_srcVer:1}
%define     _verstr %{_srcVer}
%else
%define     _verstr 1
%endif

%if 0%{?_opt:1}
%define         _sconsOpt      %{_opt}
%else
%define         _sconsOpt      debug
%endif

%if 0%{?_enableMellanox:1}
%define         _enableMlx %{_enableMellanox}
%else
%define         _enableMlx FALSE
%endif

%if 0%{?_dpdk_build_dir:1}
%define         _dpdk_args --dpdk-dir=%{_dpdk_build_dir}
%else
%define         _dpdk_args %{nil}
%endif

%bcond_without debuginfo

Name:       contrail-vrouter-dpdk
Version:    %{_verstr}
Release:    %{_relstr}%{?dist}
Summary:    Contrail vrouter DPDK %{?_gitVer}

Group:      Applications/System
License:    Commercial
URL:        http://www.juniper.net/
Vendor:     Juniper Networks Inc

BuildRequires: boost-devel = 1.53.0
BuildRequires: liburcu-devel
BuildRequires: numactl-devel
BuildRequires: libnl3-devel
%if 0%{?rhel} < 8
BuildRequires: scons
%endif
BuildRequires: gcc
BuildRequires: flex
BuildRequires: bison
BuildRequires: gcc-c++
BuildRequires: libpcap
BuildRequires: libpcap-devel
%if 0%{?centos}
BuildRequires: python2-pip
BuildRequires: python3-pip
%endif
Requires: which
Requires: liburcu2
Requires: userspace-rcu = 0.10.0-3.el7
Requires: libnl3
Requires: numactl-libs
%if %{_enableMlx} == "TRUE"
BuildRequires: rdma-core-devel = 47mlnx1-1.47329
Requires: rdma-core = 47mlnx1-1.47329
Requires: libibverbs = 47mlnx1-1.47329
%define         _sconsAddOpts      enableMellanox
%else
%define         _sconsAddOpts      none
%endif

%description
Provides contrail-vrouter-dpdk binary

%if %{with debuginfo}
%debug_package
%endif

%prep
%if 0%{?_pre_cleanup:1}
    # Cleanup
pushd %{_sbtop}
scons -c \
    --opt=%{_sconsOpt} \
    %{_dpdk_args} \
    --root=%{_builddir} \
    --add-opts=%{_sconsAddOpts} \
    vrouter/dpdk
popd
%endif

%build
pushd %{_sbtop}
scons \
    --opt=%{_sconsOpt} \
    %{_dpdk_args} \
    --root=%{_builddir} \
    --add-opts=%{_sconsAddOpts} \
    vrouter/dpdk
popd

%install
# Install Directories
install -d -m 755 %{buildroot}/%{_bindir}
install -p -m 755 %{_sbtop}build/%{_sconsOpt}/vrouter/dpdk/contrail-vrouter-dpdk %{buildroot}/%{_bindir}/contrail-vrouter-dpdk
install -d -m 755 %{buildroot}/opt/contrail/ddp/
install -p -m 755 %{_sbtop}vrouter/dpdk/ddp/mplsogreudp.pkg %{buildroot}/opt/contrail/ddp/mplsogreudp.pkg
install -d -m 755 %{buildroot}/opt/contrail/bin/
install -p -m 755 %{_sbtop}build/%{_sconsOpt}/vrouter/dpdk/dpdk-devbind.py %{buildroot}/opt/contrail/bin/dpdk_nic_bind.py
# tools
install -p -m 755 %{_sbtop}/build/%{_sconsOpt}/vrouter/dpdk/x86_64-native-linuxapp-gcc/app/testpmd %{buildroot}/usr/bin/testpmd

%files
%defattr(-,root,root,-)
%{_bindir}/contrail-vrouter-dpdk
/opt/contrail/ddp/mplsogreudp.pkg
/opt/contrail/bin/dpdk_nic_bind.py

%changelog
* Thu Feb 16 2017 Nagendra Maynattamai <npchandran@juniper.net> 4.1.1-2.1contrail1
- Initial Build. Rebuilt with patches for Opencontrail

%package tools
Summary: Contrail tools for DPDK mode
Group: Applications/System

%description tools
Contrail DPDK tools for debug purposes.

%files tools
%{_bindir}/testpmd
