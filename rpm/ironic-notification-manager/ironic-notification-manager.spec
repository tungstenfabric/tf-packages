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

%define         _build_dist        %{_sbtop}build/debug
%define         _contrailetc       /etc/contrail
%define         _binusr            /usr/bin/
%define         _ironic_notif_mgr  %{_sbtop}controller/src/config/ironic-notification-manager

Name:           ironic-notification-manager
Version:        %{_verstr}
Release:        %{_relstr}%{?dist}
Summary:        BMS Notfication daemon for Contrail Analytics%{?_gitVer}
Group:          Applications/System
License:        Commercial
URL:            http://www.juniper.net
Vendor:         Juniper Networks Inc

BuildArch:      noarch

BuildRequires: bison
BuildRequires: boost-devel = 1.53.0
BuildRequires: flex
BuildRequires: gcc-c++

%if 0%{?rhel} < 8
Requires: python-ironicclient
Requires: python-keystoneclient >= 0.2.0
Requires: python-gevent
Requires: python-netaddr
Requires: python-kombu
%endif

Requires: python-contrail >= %{_verstr}-%{_relstr}

%description
BMS Notification daemon to interface between Openstack Ironic and Contrail Analytics

%prep
%if 0%{?_pre_cleanup:1}
rm -rf %{_sbtop}build/debug/config/ironic-notification-manager/
rm -rf %{buildroot}%{_installdir}
%endif


%build
pushd %{_sbtop}controller
scons -U src/config/ironic-notification-manager
popd

%install
# Setup directories
install -d -m 755 %{buildroot}/etc/
install -d -m 755 %{buildroot}%{_contrailetc}
install -d -m 755 %{buildroot}/usr/
install -d -m 755 %{buildroot}%{_binusr}
install -d -m 755 %{buildroot}%{python_sitelib}
install -d -m 755 %{buildroot}%{python_sitelib}/ironic-notification-manager/

# install files

pushd %{_sbtop}build/debug/config/ironic-notification-manager/
mkdir -p dist_tmp
cd dist_tmp
last=$(ls -1 --sort=v -r ../dist/*.tar.gz | head -n 1| xargs -i basename {})
echo "DBG: $(pwd)/../dist/ last tar.gz = $last"
tar zxf ../dist/$last
cd ${last//\.tar\.gz/}
%{__python} setup.py install --root=%{buildroot} --no-compile %{?_venvtr}
cd ../..
rm -rf dist_tmp
popd

pushd %{_sbtop}
install -p -m 755 %{_ironic_notif_mgr}/ironic-notification-manager.conf %{buildroot}%{_contrailetc}/ironic-notification-manager.conf
popd

%files
%defattr(-,root,root,-)
%{_contrailetc}/ironic-notification-manager.conf
%{_binusr}/ironic-notification-manager
%{python_sitelib}/ironic_notification_manager
%{python_sitelib}/ironic_notification_manager-*

%if 0%{?rhel} >= 8
%post
set -e
%{__python} -m pip install \
  gevent \
  ironicclient \
  "keystoneclient>=0.2.0" \
  kombu \
  netaddr
%endif
