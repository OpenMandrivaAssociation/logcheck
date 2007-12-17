Name:		logcheck
Summary:	Psionic LogCheck
Version:	1.1.1
Release:	%mkrel 12
License:	GPL
Group:		Monitoring
URL:		http://www.psionic.com

Source:		%name-%version.tar.bz2
Source1:	logcheck.cron
Patch:		logcheck.patch
Patch1:		logcheck-sh.patch
Patch2:		logcheck-1.1.1-crond-ignore.patch
#FIX http://www.mandriva.com/security/advisories?name=MDKSA-2004:155
Patch3:		logcheck-1.1.1-CAN-2004-0404.patch
Requires:	grep


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
%patch -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .can-2004-0404

%install
export INSTALLDIR=%{buildroot}%{_sysconfdir}/logcheck
export INSTALLDIR_BIN=%{buildroot}%{_bindir}
export INSTALLDIR_SH=%{buildroot}%{_bindir}
export TMPDIR=%{buildroot}%{_localstatedir}/%{name}
chmod -R go+r *
export CFLAGS=$RPM_OPT_FLAGS

install -d $INSTALLDIR
install -d $INSTALLDIR_BIN
install -d $INSTALLDIR_SH
install -d $TMPDIR

make linux TMPDIR=%buildroot%{_localstatedir}/%name

# rename files
pushd %buildroot/%_sysconfdir/logcheck
  mv -f logcheck.hacking hacking
  mv -f logcheck.violations violations
  mv -f logcheck.violations.ignore violations.ignore
  mv -f logcheck.ignore ignore
popd

install -d %buildroot/%_sysconfdir/cron.daily/
install -m755 %SOURCE1 %buildroot/%_sysconfdir/cron.daily/logcheck

%clean
rm -fr %buildroot

%pre

if [ -d /var/logcheck ]; then
  mv /var/logcheck %{_localstatedir}/logcheck
fi

%files
%defattr(-,root,root,0755)
%doc CHANGES CREDITS INSTALL LICENSE README* systems/linux/README*
%config(noreplace) %_sysconfdir/cron.daily/logcheck
%dir %_sysconfdir/logcheck
%config(noreplace) %_sysconfdir/logcheck/hacking
%config(noreplace) %_sysconfdir/logcheck/violations
%config(noreplace) %_sysconfdir/logcheck/violations.ignore
%config(noreplace) %_sysconfdir/logcheck/ignore
%_bindir/logcheck.sh
%_bindir/logtail
%attr(0700,root,root) %dir %{_localstatedir}/%name


