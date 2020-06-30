%define         _contrailetc /etc/contrail
%define         _distropkgdir %{_sbtop}tools/packages/rpm/%{name}

%if 0%{?fedora} >= 17
%define         _servicedir  %{_libdir}/systemd/system
%endif

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

%bcond_without debuginfo

Name:             contrail-nodemgr
Version:          %{_verstr}
Release:          %{_relstr}%{?dist}
Summary:          Contrail Nodemgr %{?_gitVer}

Group:            Applications/System
License:          Commercial
URL:              http://www.juniper.net/
Vendor:           Juniper Networks Inc

Requires:         contrail-lib >= %{_verstr}-%{_relstr}
Requires:         xmltodict >= 0.7.0
Requires:         python-bottle >= 0.11.6
Requires:         python-contrail >= %{_verstr}-%{_relstr}
Requires:         ntp
Requires:         python-psutil
Requires:         PyYAML
Requires:         python-setuptools
Requires:         python2-future
Requires:         python-configparser

%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:         python-importlib
%endif

BuildRequires: bison
BuildRequires: boost-devel
BuildRequires: flex
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
%if 0%{?centos}
BuildRequires: python2-pip
BuildRequires: python3-pip
%endif

%description
Contrail Nodemgr package

%if %{with debuginfo}
%debug_package
%endif

%prep

%build
pushd %{_sbtop}/controller
scons --opt=%{_sconsOpt} -U contrail-nodemgr

if [ $? -ne 0 ] ; then
  echo "build failed"
  exit -1
fi
popd

%install

# Setup directories

pushd %{_sbtop}

#install files
install -d -m 755 %{buildroot}%{_bindir}

# install pysandesh files
%define _build_dist %{_sbtop}/build/%{_sconsOpt}
install -d -m 755 %{buildroot}

popd

mkdir -p build/python_dist
cd build/python_dist

tar zxf %{_build_dist}/nodemgr/dist/nodemgr-0.1dev.tar.gz
pushd nodemgr-0.1dev
%{__python} setup.py install --root=%{buildroot} --no-compile
popd

%files
%defattr(-,root,root,-)
%{_bindir}/contrail-nodemgr
%{python_sitelib}/nodemgr
%{python_sitelib}/nodemgr-*

%changelog
