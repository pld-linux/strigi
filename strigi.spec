#
# TODO:
# - pl
# - what about strigi daemon?
#
Summary:	Strigi
Summary(pl.UTF-8):	Strigi
Name:		strigi
Version:	0.5.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://www.vandenoever.info/software/strigi/%{name}-%{version}.tar.bz2
# Source0-md5:	b976b4f3cf451fc53cd773c338d78994
URL:		http://www.vandenoever.info/software/strigi/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cmake
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Strigi.

#%description -l pl.UTF-8

%package devel
Summary:        Header files for strigi
Summary(pl.UTF-8):      Pliki nagłówkowe dla strigi
Group:          Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
Header files for strigi.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla strigi.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        ../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /usr/lib/*.so*
%dir /usr/lib/strigi
%attr(755,root,root) /usr/lib/strigi/*.so

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/strigi
%{_includedir}/strigi/*.h
/usr/lib/pkgconfig/*.pc
%dir %{_datadir}/strigi
%{_datadir}/strigi/fieldproperties
