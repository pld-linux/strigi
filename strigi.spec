#
# TODO:
# - what about strigi daemon?
#
Summary:	Strigi desktop search
Summary(pl.UTF-8):	System wyszukiwania Strigi
Name:		strigi
Version:	0.5.7
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://www.vandenoever.info/software/strigi/%{name}-%{version}.tar.bz2
# Source0-md5:	01015166eb49a523219d3b1d7e46b672
URL:		http://www.vandenoever.info/software/strigi/
BuildRequires:	QtDBus-devel >= 4.3.0
BuildRequires:	QtGui-devel >= 4.3.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clucene-core-devel
BuildRequires:	cmake
BuildRequires:	rpmbuild(macros) >= 1.293
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Here are the main features of Strigi Desktop Search: very fast
crawling, very small memory footprint, no hammering of the system,
pluggable backend (currently clucene and hyperestraier, sqlite3 and
xapian are in the works), communication between daemon and search
program over an abstract interface with two implementations: DBus and
a simple unix socket. Especially the DBus interface makes it very easy
to write client applications. There are a few sample scripts in the
code using Perl, Python, GTK+ and Qt. Writing clients is so easy that
any GNOME or KDE app could implement this. Additionally, there is a
simple interface for implementing plugins for extracting information.
We'll try to reuse the kat plugins, although native plugins will have
a large speed advantage. Strigi also has calculation of sha1 for every
file crawled which allows for fast finding of duplicate files.

%description -l pl.UTF-8
Główne cechy systemu wyszukiwania Strigi to: bardzo szybkie
przeglądanie, bardzo mały narzut pamięciowy, nieprzytykanie systemu,
backend z obsługą wtyczek (aktualnie clucene i hyperestraier, sqlite3
i xapian w trakcie rozwoju), komunikacja między demonem a programem
wyszukującym po abstrakcyjnym interfejsie z dwiema implementacjami:
DBus i prostym gdzieździe uniksowym. Zwłaszcza interfejs DBus znacznie
ułatwia pisanie aplikacji klienckich. Istnieje kilka przykładowych
skryptów napisanych z użyciem Perla, Pythona, GTK+ i Qt. Tworzenie
klientów jest tak proste, że każda aplikacja GNOME czy KDE może to
zaimplementować. Ponadto istnieje prosty interfejs do implementowania
wtyczek do wydobywania informacji. Autorzy będą próbowali
wykorzystywać wtyczki kata, ale natywne wtyczki będą miały większą
szybkość. Strigi ma także obliczanie sha1 dla każdego przeglądanego
pliku, co pozwala na szybkie znajdowanie duplikatów.

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
	-DCMAKE_VERBOSE_MAKEFILE=1 \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libsearchclient.so.*.*.*
%attr(755,root,root) %{_libdir}/libstreamanalyzer.so.*.*.*
%attr(755,root,root) %{_libdir}/libstreams.so.*.*.*
%attr(755,root,root) %{_libdir}/libstrigihtmlgui.so.*.*.*
%attr(755,root,root) %{_libdir}/libstrigiqtdbusclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsearchclient.so.0
%attr(755,root,root) %ghost %{_libdir}/libstreamanalyzer.so.0
%attr(755,root,root) %ghost %{_libdir}/libstreams.so.0
%attr(755,root,root) %ghost %{_libdir}/libstrigihtmlgui.so.0
%attr(755,root,root) %ghost %{_libdir}/libstrigiqtdbusclient.so.0
%dir %{_libdir}/strigi
%attr(755,root,root) %{_libdir}/strigi/*.so
%{_datadir}/dbus-1/services/*.service
%dir %{_datadir}/strigi
%{_datadir}/strigi/fieldproperties

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsearchclient.so
%attr(755,root,root) %{_libdir}/libstreamanalyzer.so
%attr(755,root,root) %{_libdir}/libstreams.so
%attr(755,root,root) %{_libdir}/libstrigihtmlgui.so
%attr(755,root,root) %{_libdir}/libstrigiqtdbusclient.so
%{_libdir}/strigi/*.cmake
%dir %{_includedir}/strigi
%{_includedir}/strigi/*.h
%{_includedir}/strigi/qtdbus
%{_pkgconfigdir}/libstreamanalyzer.pc
%{_pkgconfigdir}/libstreams.pc
