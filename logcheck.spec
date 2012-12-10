Name:		logcheck
Summary:	Psionic LogCheck
Version:	1.3.13
Release:	%mkrel 1
License:	GPLv2
Group:		Monitoring
URL:		http://logcheck.org/
Source:		http://ftp.de.debian.org/debian/pool/main/l/logcheck/%{name}_%{version}.tar.gz
BuildRequires:	docbook-to-man
Requires:	lockfile-progs
Requires:	nail
Requires:	sendmail-command
Requires:	mime-construct
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
%setup -q -n %{name}

%build
cd docs
docbook-to-man logcheck.sgml > logcheck.8

%install
%makeinstall_std

install -d %buildroot%_mandir/man8
install -m 644 docs/*.8 %buildroot%_mandir/man8

install -d %buildroot/%_sysconfdir/cron.d
cat > %buildroot/%_sysconfdir/cron.d/logcheck <<EOF
2 * * * * logcheck %{_sbindir}/logcheck
EOF

cat > README.urpmi <<EOF
Mandriva package notes
----------------------
In order to finish installation, you have to ensure the logcheck user has read
access to all log files listed in %_sysconfdir/logcheck/logcheck.logfiles
EOF

%clean
rm -fr %buildroot

%pre
%_pre_useradd logcheck /var/lib/logcheck /bin/false

%postun
%_postun_userdel logcheck

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES CREDITS INSTALL LICENSE TODO docs/README.* README.urpmi
%config(noreplace) %_sysconfdir/cron.d/logcheck
%config(noreplace) %attr(-,root,logcheck) %_sysconfdir/logcheck
%_sbindir/logcheck
%_sbindir/logtail
%_bindir/logcheck-test
%_sbindir/logtail2
%_datadir/logtail
%_mandir/man8/logcheck.8*
%_mandir/man8/logtail.8*
%_mandir/man8/logtail2.8*
%attr(-,logcheck,logcheck) %dir %{_localstatedir}/lock/%name
%attr(0700,logcheck,logcheck) %dir %{_localstatedir}/lib/%name


%changelog
* Thu Sep 23 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.13-1mdv2011.0
+ Revision: 580710
- update to new version 1.3.13

* Sat Aug 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.12-1mdv2011.0
+ Revision: 569584
- new version

* Thu Mar 04 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.3.7-1mdv2010.1
+ Revision: 514301
- update to 1.3.7
- fix file list, %%_bindir/logcheck-test was missing
- fix license

* Wed Jan 27 2010 Frederik Himpe <fhimpe@mandriva.org> 1.3.6-1mdv2010.1
+ Revision: 497431
- Update to new version 1.3.6
- Remove mail command args patch: now mime-construct is used instead of
  mail parameters to insert custom headers, so also add
  Requires: mime-construct

* Fri Jan 01 2010 Frederik Himpe <fhimpe@mandriva.org> 1.3.5-1mdv2010.1
+ Revision: 484861
- Update to new version 1.3.5

* Wed Aug 19 2009 Frederik Himpe <fhimpe@mandriva.org> 1.3.3-1mdv2010.0
+ Revision: 417891
- Update to new version 1.3.3

* Mon Jun 29 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.2-2mdv2010.0
+ Revision: 390759
- don't use debian-specific flags for mail command (fix #51961)
- add README.urpmi advertising post-installation instructions

* Mon Jun 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.2-1mdv2010.0
+ Revision: 386125
- new version
- fix permissions on configuration directory

* Thu Feb 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.45-4mdv2009.1
+ Revision: 342996
- rebuild with a fixed docbook-to-man package
- change cron task to run as logcheck user

* Sun Feb 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.45-3mdv2009.1
+ Revision: 340602
- ship missing documentation files

* Fri Feb 13 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.45-2mdv2009.1
+ Revision: 340170
- fix dependencies
- create logcheck user
- create lock directory
- ensure cron task is executable (mdv bug #47427)

* Sun Jan 25 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.45-1mdv2009.1
+ Revision: 333545
- sync with upstream project
- drom all patches
- spec cleanup

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.1.1-14mdv2009.0
+ Revision: 223122
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Dec 27 2007 Emmanuel Andry <eandry@mandriva.org> 1.1.1-13mdv2008.1
+ Revision: 138662
- fix patch1 (bug #36378)

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 12mdv2008.1-current
+ Revision: 129436
- kill re-definition of %%buildroot on Pixel's request
- s/Mandrake/Mandriva/


* Sun Jan 28 2007 Olivier Thauvin <nanardon@mandriva.org> 1.1.1-12mdv2007.0
+ Revision: 114620
- mkrel

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.1.1-11mdk
- Rebuild

* Wed Mar 09 2005 Nicolas Lécureuil <neoclust@mandrake.org> 1.1.1-10mdk
- security fix for CAN-2004-0404

