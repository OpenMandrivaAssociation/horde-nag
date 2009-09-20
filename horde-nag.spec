%define	module	nag
%define	name	horde-%{module}
%define version 2.3.1
%define release %mkrel 4
%define _requires_exceptions pear(.*)

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:	The Horde task list manager
License:	GPL
Group: 		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Patch:      %{module}-h3-2.3.1-fix-constant-loading.patch
Requires(post):	rpm-helper
Requires:	horde >= 3.3.5
BuildArch:	noarch
BuildRoot: 	%{_tmppath}/%{name}-%{version}

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
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Deny from all
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
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc COPYING README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
