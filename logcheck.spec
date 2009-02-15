Name:		logcheck
Summary:	Psionic LogCheck
Version:	1.2.45
Release:	%mkrel 3
License:	GPL
Group:		Monitoring
URL:		http://logcheck.org/
Source:		http://alioth.debian.org/frs/download.php/1677/%{name}_%{version}.tar.gz
BuildRequires: docbook-to-man
Requires:   lockfile-progs
Requires:   nail
Requires:   sendmail-command
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

%build
cd docs
docbook-to-man logcheck.sgml > logcheck.8

%install
%makeinstall_std

install -d %buildroot%_mandir/man8
install -m 644 docs/*.8 %buildroot%_mandir/man8

install -d %buildroot/%_sysconfdir/cron.daily/
cat > %buildroot/%_sysconfdir/cron.daily/logcheck <<EOF
#!/bin/sh
%{_sbindir}/logcheck
EOF
chmod 755 %buildroot/%_sysconfdir/cron.daily/logcheck

%clean
rm -fr %buildroot

%pre
%_pre_useradd logcheck /var/lib/logcheck /bin/false

%postun
%_postun_userdel logcheck

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES CREDITS INSTALL LICENSE TODO docs/README.*
%config(noreplace) %_sysconfdir/cron.daily/logcheck
%config(noreplace) %_sysconfdir/logcheck
%_sbindir/logcheck
%_sbindir/logtail
%_mandir/man8/logcheck.8*
%_mandir/man8/logtail.8*
%attr(-,logcheck,logcheck) %dir %{_localstatedir}/lock/%name
%attr(0700,logcheck,logcheck) %dir %{_localstatedir}/lib/%name
