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

Name:       contrail-vcenter-manager
Version:    %{_verstr}
Release:    %{_relstr}%{?dist}
Summary:    Contrail vCenter Manager

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
Requires: contrail-vrouter-agent
Requires: python-contrail-vrouter-api
Requires: python-contrail
Requires: python2-future
%if 0%{?rhel} < 8
Requires: python-gevent
Requires: PyYAML
%endif

# tpc bin
Requires: python2-pyvmomi
Requires: python2-ipaddress
# tpc
Requires: python-configparser

%description
Contrail vCenter Manager package

%prep

%build

%install
pushd %{_sbtop}
scons --opt=%{_sconsOpt} --root=%{buildroot} cvm-install
popd

%files
%defattr(-,root,root,-)
%{python_sitelib}/cvm*
%{python_sitelib}/contrail_vcenter_manager*
%attr(755, root, root) %{_bindir}/contrail-vcenter-manager
%exclude %{python_sitelib}/tests*

%post
%if 0%{?rhel} >= 8
%{__python} -m pip install --no-compile \
  "gevent>=1.0,<1.5.0" \
  "PyYAML>=5.1"
%endif
mkdir -p /etc/contrail/contrail-vcenter-manager
