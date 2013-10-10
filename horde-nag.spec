%define	module	nag

Name:           horde-%{module}
Version:        2.3.6
Release:        3
Summary:	The Horde task list manager
License:	GPL
Group: 		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Patch:      %{module}-h3-2.3.1-fix-constant-loading.patch
Requires:	horde >= 3.3.5
BuildArch:	noarch

%description
Nag is the Horde task list application. It stores todo items, things
due later this week, etc. It is very similar in functionality to the
Palm ToDo application.

%prep
%setup -q -n %{module}-h3-%{version}
%patch -p 1

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Require all denied
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Nag Horde configuration file
//
 
$this->applications['nag'] = array(
    'fileroot'    => $this->applications['horde']['fileroot'] . '/nag',
    'webroot'     => $this->applications['horde']['webroot'] . '/nag',
    'name'        => _("Tasks"),
    'status'      => 'active',
    'provides'    => 'tasks',
    'menu_parent' => 'organizing'
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR js %{buildroot}%{_datadir}/horde/%{module}
cp -pR tasklists %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

# fix script shellbang
for file in `find %{buildroot}%{_datadir}/horde/%{module}/scripts`; do
	perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|' $file
done

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi
%if %mdkversion < 201010
%_post_webapp
%endif


%files
%defattr(-,root,root)
%doc COPYING README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Wed Mar 30 2011 Adam Williamson <awilliamson@mandriva.org> 2.3.6-1mdv2011.0
+ Revision: 648834
- new release 2.3.6

* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.3.5-1mdv2011.0
+ Revision: 567504
- Updated to 2..3.5
- added version 2..3.5 source file

* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.3.4-3mdv2011.0
+ Revision: 565289
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.4-2mdv2010.1
+ Revision: 493351
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sat Dec 26 2009 Funda Wang <fwang@mandriva.org> 2.3.4-1mdv2010.1
+ Revision: 482415
- new version 2.3.4

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.1-4mdv2010.0
+ Revision: 446020
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 2.3.1-3mdv2010.0
+ Revision: 437885
- rebuild

* Tue Nov 18 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.1-2mdv2009.1
+ Revision: 304319
- fix constant loading

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.1-1mdv2009.1
+ Revision: 295271
- update to new version 2.3.1

* Tue Jun 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2-3mdv2009.0
+ Revision: 223591
- add missing js and tasklists directories (fix #41533)

* Fri May 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.2-2mdv2009.0
+ Revision: 213374
- new version
  drop patch0
  uncompress sources
  don't duplicate spec-helper work

* Wed Jan 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.4-1mdv2008.1
+ Revision: 153804
- update to new version 2.1.4

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.3-1mdv2008.1
+ Revision: 133783
- update to new version 2.1.3

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Mon Dec 18 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.2-1mdv2007.0
+ Revision: 98606
- new version
  fix horde configuration

  + Andreas Hasenack <andreas@mandriva.com>
    - Import horde-nag

* Tue Jun 27 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.1-1mdv2007.0
- New version 2.1.1
- use herein document for horde config
- uncompress patch

* Tue Mar 07 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-1mdk
- new version

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.4-1mdk
- New release 2.0.4

* Sat Sep 17 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.2-2mdk
- explicit dependency exception, as all those modules are provided by horde itself 
- %%mkrel

* Sat Aug 20 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.2-1mdk
- New release 2.0.2
- better fix encoding

* Fri Jul 01 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.1-3mdk 
- better fix encoding
- fix requires

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.1-2mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Thu Jan 27 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0.1-1mdk 
- new version
- no automatic config generation, incorrect default values
- horde isn't a prereq
- spec cleanup

* Mon Jan 17 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-2mdk 
- fix inclusion path
- fix configuration perms
- generate configuration at postinstall
- horde and rpm-helper are now a prereq

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-1mdk 
- new version
- top-level is now /var/www/horde/nag
- config is now in /etc/horde/nag
- other non-accessible files are now in /usr/share/horde/nag
- drop old obsoletes
- rediff patch0
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Tue Jul 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.1.1-5mdk 
- apache config file in /etc/httpd/webapps.d

* Sun May 02 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.1.1-4mdk
- renamed to horde-nag
- pluggable horde configuration
- standard perms for /etc/httpd/conf.d/%%{order}_horde-nag.conf
- don't provide useless ADVXpackage virtual package

* Tue Apr 06 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.1.1-3mdk
- new version

* Sat Dec 20 2003 Guillaume Rousse <guillomovitch@mandrake.org> 1.1-2mdk
- untagged localisation files
- no more .htaccess files, use /etc/httpd/conf.d/%%{order}_nag.conf instead
- scripts now in  /usr/share/{name}

