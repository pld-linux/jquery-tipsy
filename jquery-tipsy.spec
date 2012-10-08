# TODO
# - finish demo package
%define		plugin	tipsy
Summary:	tipsy - Facebook-style tooltip plugin for jQuery
Name:		jquery-%{plugin}
Version:	1.0.0a
Release:	1
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/jaz303/tipsy/tarball/v%{version}/%{plugin}-%{version}.tgz
# Source0-md5:	ce2049b166638fb75a307fd7520be954
URL:		http://onehackoranother.com/projects/jquery/tipsy/
BuildRequires:	closure-compiler
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
BuildRequires:	sed >= 4.0
BuildRequires:	yuicompressor
Requires:	jquery
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
Tipsy is a jQuery plugin for creating a Facebook-like tooltips effect
based on an anchor tag's title attribute.

%package demo
Summary:	Demo for jQuery.%{plugin}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu jQuery.%{plugin}
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for jQuery.%{plugin}.

%prep
%setup -qc
mv *-%{plugin}-*/* .

%{__sed} -i -e 's,../images/,,' src/stylesheets/*.css

%build
install -d build/stylesheets

# compress .js
for js in src/javascripts/*.js; do
	out=build/${js#*/jquery.}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $js -o $out
	js -C -f $out
%else
	cp -p $js $out
%endif
done

# pack .css
for css in src/stylesheets/*.css; do
	out=build/${css#*/}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $css -o $out
%else
	cp -p $css $out
%endif
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -p build/%{plugin}.js  $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p src/javascripts/jquery.%{plugin}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js

cp -p build/stylesheets/%{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.css
cp -p src/stylesheets/%{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.css
ln -s %{plugin}-%{version}.min.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}.css

cp -p src/images/*.gif $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE
%{_appdir}
