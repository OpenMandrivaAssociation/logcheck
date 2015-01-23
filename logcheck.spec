%define debug_package %{nil}

Name:		logcheck
Summary:	Psionic LogCheck
Version:	1.3.15
Release:	3
License:	GPLv2
Group:		Monitoring
URL:		http://logcheck.org/
Source:		http://ftp.de.debian.org/debian/pool/main/l/logcheck/logcheck_1.3.15.tar.gz
BuildRequires:	docbook-to-man
Requires:	lockfile-progs
Requires:	nail
Requires:	sendmail-command
Requires:	mime-construct

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
echo "d /var/lock/logcheck 1700 logcheck logcheck 1d" > etc/tmpfiles.d-logcheck

%build
cd docs
docbook-to-man logcheck.sgml > logcheck.8

%install
%makeinstall_std

install -d %{buildroot}%{_mandir}/man8
install -m 644 docs/*.8 %{buildroot}%{_mandir}/man8

install -d %{buildroot}/%{_sysconfdir}/cron.d
cat > %{buildroot}/%{_sysconfdir}/cron.d/logcheck <<EOF
2 * * * * logcheck %{_sbindir}/logcheck
EOF

mkdir -pm 755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -pm 644 etc/tmpfiles.d-logcheck %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

cat > README.urpmi <<EOF
Package notes
----------------------
In order to finish installation, you have to ensure the logcheck user has read
access to all log files listed in %{_sysconfdir}/logcheck/logcheck.logfiles
EOF

%clean

%pre
%_pre_useradd logcheck /var/lib/logcheck /bin/false

%post
systemd-tmpfiles --create %{name}.conf

%postun
%_postun_userdel logcheck

%files
%doc AUTHORS CHANGES CREDITS INSTALL LICENSE TODO docs/README.* README.urpmi
%config(noreplace) %{_sysconfdir}/cron.d/logcheck
%config(noreplace) %attr(-,root,logcheck) %{_sysconfdir}/logcheck
%{_sbindir}/logcheck
%{_sbindir}/logtail
%{_bindir}/logcheck-test
%{_sbindir}/logtail2
%{_datadir}/logtail
%{_mandir}/man8/logcheck.8*
%{_mandir}/man8/logtail.8*
%{_mandir}/man8/logtail2.8*
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(0700,logcheck,logcheck) %dir %{_localstatedir}/lib/%{name}
