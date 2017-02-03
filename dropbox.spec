Summary: Dropbox file sync tool
Name: dropbox
Version: 19.4.12
Release: 4%{?dist}
License: Proprietary
Group: System Environment/Daemons 
URL: http://www.dropbox.com/

Source0: https://dl.dropboxusercontent.com/u/17/dropbox-lnx.x86_64-%{version}.tar.gz
Source1: dropbox.service
# Avoid duplicate provides
AutoReqProv: no
# Don't create debug
%global debug_package %{nil}
# No binary stripping
%define __os_install_post %{nil}

%description
Dropbox is software that syncs your files online and across your computers.

%prep
%setup -n .dropbox-dist -T -b 0

%build

%install
%{__rm} -rf %{buildroot}

mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
install -p -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_unitdir}/%{name}@.service
install -d %{buildroot}%{_libexecdir}/dropbox/
cp -a ./* %{buildroot}%{_libexecdir}/dropbox/

# Remove old unit file that did not support multi-user
rm -f %{_unitdir}/%{name}.service
rm -f %{_libexecdir}/dropbox/dropbox-lnx.x86_64-%{version}/dropbox
ln -s %{_libexecdir}/dropbox/dropbox-lnx.x86_64-%{version}/dropbox  %{buildroot}%{_libexecdir}/dropbox/dropbox

%post

%preun
if (( $1 == 0 )); then
    /usr/bin/systemctl disable dropbox &>/dev/null || :
fi

%files
%defattr(-,root,root,0755)
%{_libexecdir}/dropbox/
%{_unitdir}/dropbox@.service

%changelog
* Fri Feb 3 2017 ClearFoundation <developer@clearfoundation.com> - 19.4.12-4
- Remove old non-multiservice unit file

* Thu Feb 2 2017 ClearFoundation <developer@clearfoundation.com> - 19.4.12-3
- 64 bit only
- Migrate to sytemd

* Thu Feb 2 2017 ClearFoundation <developer@clearfoundation.com> - 19.4.12-1
- Update to latest version

* Thu Aug 18 2016 ClearFoundation <developer@clearfoundation.com> - 7.4.30-1
- Update to latest version

* Wed Aug 26 2015 ClearFoundation <developer@clearfoundation.com> - 3.8.8-1
- Update to latest version

* Mon Aug 18 2014 ClearFoundation <developer@clearfoundation.com> - 2.10.28-1
- Update to latest version

* Fri Nov  2 2012 ClearFoundation <developer@clearfoundation.com> - 1.4.20-1
- First import loosely based on rpmforge spec file
