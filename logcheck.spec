Name:		logcheck
Summary:	Psionic LogCheck
Version:	1.2.45
Release:	%mkrel 1
License:	GPL
Group:		Monitoring
URL:		http://logcheck.org/
Source:		http://alioth.debian.org/frs/download.php/1677/%{name}_%{version}.tar.gz
BuildRoot:	%_tmppath/%name-%version

%description
Logcheck is a software package that is designed to automatically run and check 
system log files for security violations and unusual activity.  Logcheck 
utilizes a program called logtail that remembers the last position it read 
from in a log file and uses this position on subsequent runs to process new 
information.  All source code is available for review and the implementation 
was kept simple to avoid problems.  This package is a clone of the 
frequentcheck.sh script from the Trusted Information Systems Gauntlet(tm) 
firewall package.  TIS has granted permission for me to clone this package.

%prep
%setup -q

%install
%makeinstall_std

install -d %buildroot/%_sysconfdir/cron.daily/
cat > %buildroot/%_sysconfdir/cron.daily/logcheck <<EOF
#!/bin/sh
%{_bindir}/logcheck
EOF

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES CREDITS INSTALL LICENSE TODO
%config(noreplace) %_sysconfdir/cron.daily/logcheck
%config(noreplace) %_sysconfdir/logcheck
%_sbindir/logcheck
%_sbindir/logtail
%attr(0700,root,root) %dir %{_localstatedir}/lib/%name


