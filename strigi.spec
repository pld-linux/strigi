#
# TODO:
# - pl
# - what about strigi daemon?
#
Summary:	Strigi desktop search
#Summary(pl.UTF-8):	Strigi
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
Strigi Desktop Search

Here are the main features of Strigi: very fast crawling very small
memory footprint no hammering of the system pluggable backend,
currently clucene and hyperestraier, sqlite3 and xapian are in the
works communication between daemon and search program over an abstract
interface with two implementations: DBus and a simple unix socket.
Especially the DBus interface makes it very easy to write client
applications. There are a few sample scripts in the code using Perl,
Python, GTK and Qt. Writing clients is so easy that any Gnome or KDE
app could implement this. Aditionally, there is a simple interface for
implementing plugins for extracting information. We'll try to reuse
the kat plugins, although native plugins will have a large speed
advantage. Strigi also has calculation of sha1 for every file crawled
which allows for fast finding of duplicate files.

#%description -l pl.UTF-8

%package devel
Summary:	Header files for strigi
Summary(pl.UTF-8):	Pliki nagłówkowe dla strigi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
%attr(755,root,root) %{_prefix}/lib/*.so*
%dir %{_prefix}/lib/strigi
%attr(755,root,root) %{_prefix}/lib/strigi/*.so

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/strigi
%{_includedir}/strigi/*.h
/usr/lib/pkgconfig/*.pc
%dir %{_datadir}/strigi
%{_datadir}/strigi/fieldproperties
