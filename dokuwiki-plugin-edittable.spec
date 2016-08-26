%define		subver	2015-06-17
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		edittable
%define		php_min_version 5.3.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki edittable plugin
Summary(pl.UTF-8):	Wtyczka edittable dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/cosmocode/%{plugin}/archive/%{subver}/%{plugin}-%{version}.tar.gz
# Source0-md5:	557d632e82389b8a94d88602387f5e92
URL:		https://www.dokuwiki.org/plugin:edittable
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20150810
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
Plugin that provides a visual table editing and inserting interfac

%prep
%setup -qc
mv %{plugin}-*/{*,.??*} .

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: version mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/{README*,.travis.yml}
%{__rm} -r $RPM_BUILD_ROOT%{plugindir}/_test

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README README.handsontable
%dir %{plugindir}
%{plugindir}/*.js
%{plugindir}/*.less
%{plugindir}/*.txt
%{plugindir}/action
%{plugindir}/images
%{plugindir}/less
%{plugindir}/renderer
%{plugindir}/script
