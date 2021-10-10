%define _unpackaged_files_terminate_build 0
%if 0%{?_buildTag:1}
%define         _relstr      %{_buildTag}
%else
%define         _relstr      %(date -u +%y%m%d%H%M)
%endif
%if 0%{?_srcVer:1}
%define         _verstr      %{_srcVer}
%else
%define         _verstr      1
%endif
%if 0%{?_opt:1}
%define         _sconsOpt      %{_opt}
%else
%define         _sconsOpt      debug
%endif

Name:       contrail-vcenter-fabric-manager
Version:    %{_verstr}
Release:    %{_relstr}%{?dist}
Summary:    Contrail vCenter Fabric Manager

Group:      Applications/System
License:    Commercial
URL:        http://www.juniper.net/
Vendor:     Juniper Networks Inc

BuildArch: noarch
BuildRequires: python2-setuptools
BuildRequires: python3-setuptools
%if 0%{?rhel} < 8
BuildRequires: scons
%endif
Requires: python-contrail
%if 0%{?rhel} < 8
Requires: python-gevent
Requires: python-kombu
%endif
Requires: python2-future
# tpc bin
Requires: python-bitarray
Requires: python2-pyvmomi = 6.7.3
#tpc
Requires: python-kazoo
Requires: python-pycassa
Requires: python-attrdict
Requires: python-configparser

%description
Contrail vCenter Fabric Manager package

%prep

%build

%install
pushd %{_sbtop}
scons --opt=%{_sconsOpt} --root=%{buildroot} cvfm-install
popd

%files
%defattr(-,root,root,-)
%{python_sitelib}/cvfm*
%{python_sitelib}/contrail_vcenter_fabric_manager*
%attr(755, root, root) %{_bindir}/contrail-vcenter-fabric-manager
%exclude %{python_sitelib}/tests*

%post
set -e
%if 0%{?rhel} >= 8
python2 -m pip \
  gevent \
  kombu
%endif
mkdir -p /etc/contrail/contrail-vcenter-fabric-manager
