%define		plugin		edittable
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki edittable plugin
Summary(pl.UTF-8):	Wtyczka edittable dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	20101029
Release:	3
License:	GPL v2
Group:		Applications/WWW
Source0:	http://github.com/cosmocode/%{plugin}/tarball/master?/%{plugin}.tgz
# Source0-md5:	742bade615520592ceaa711c0db13469
URL:		http://www.dokuwiki.org/plugin:edittable
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20091225
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%define		_noautopear	pear
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
Plugin that provides a visual table editing and inserting interfac

%prep
%setup -qc
mv *-%{plugin}-*/* .

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
#	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

# use this post section if you package .css or .js files
%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.txt
%{plugindir}/*.php
%{plugindir}/*.css
%{plugindir}/images
%{plugindir}/script
%{plugindir}/script.js
