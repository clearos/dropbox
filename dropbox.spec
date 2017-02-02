Summary: Dropbox file sync tool
Name: dropbox
Version: 19.4.12
Release: 1%{?dist}
License: Proprietary
Group: System Environment/Daemons
URL: http://www.dropbox.com/

Source0: https://dl.dropboxusercontent.com/u/17/dropbox-lnx.x86-%{version}.tar.gz
Source1: https://dl.dropboxusercontent.com/u/17/dropbox-lnx.x86_64-%{version}.tar.gz
Source2: dropbox.init
Source3: dropbox.wrapper
# Avoid duplicate provides
AutoReqProv: no
# Don't create debug
%global debug_package %{nil}
# No binary stripping
%define __os_install_post %{nil}

%description
Dropbox is software that syncs your files online and across your computers.

%prep
%ifarch x86_64
%setup -n .dropbox-dist -T -b 1
%else
%setup -n .dropbox-dist -T -b 0
%endif

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dp -m0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/dropbox
%{__install} -Dp -m0755 %{SOURCE3} %{buildroot}%{_bindir}/dropbox
%{__install} -d %{buildroot}%{_libexecdir}/dropbox/
%{__cp} -a ./* %{buildroot}%{_libexecdir}/dropbox/

# symlink in tar.gz is derefenced, so recreate it here
%{__rm} -fv %{buildroot}%{_libexecdir}/dropbox/dropbox
ln -s %{_libexecdir}/dropbox/library.zip  %{buildroot}%{_libexecdir}/dropbox/dropbox

%post
if (( $1 < 2 )); then
    /sbin/chkconfig --add dropbox &>/dev/null || :
fi

%preun
if (( $1 == 0 )); then
    /sbin/chkconfig --del dropbox &>/dev/null || :
fi

%files
%defattr(-,root,root,0755)
%config %{_sysconfdir}/init.d/dropbox
%{_bindir}/dropbox
%{_libexecdir}/dropbox/

%changelog
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
