#
# Conditional build:
%bcond_without	dbus		# dbus support
#
%define		qtver	4.6.3

Summary:	Strigi desktop search
Summary(pl.UTF-8):	System wyszukiwania Strigi
Name:		strigi
Version:	0.7.8
Release:	15
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://www.vandenoever.info/software/strigi/%{name}-%{version}.tar.bz2
# Source0-md5:	d69443234f4286d71997db9de543331a
Patch0:		%{name}-as-needed.patch
Patch1:		ffmpeg3.patch
Patch2:		gcc7.patch
Patch3:		ffmpeg4.patch
Patch4:		gcc8.patch
Patch5:		exiv2.patch
Patch6:		%{name}-gccversion.patch
Patch7:		%{name}-includes.patch
URL:		http://strigi.sourceforge.net/
BuildRequires:	QtDBus-devel >= %{qtver}
BuildRequires:	QtGui-devel >= %{qtver}
BuildRequires:	attr-devel
BuildRequires:	bzip2-devel
BuildRequires:	clucene-core-devel >= 0.9.21
BuildRequires:	cmake >= 2.8.9
BuildRequires:	cppunit-devel
%{?with_dbus:BuildRequires:	dbus-devel >= 1.0}
%{?with_dbus:BuildRequires:	dbus-x11 >= 1.0}
BuildRequires:	exiv2-devel >= 0.21
BuildRequires:	expat-devel
BuildRequires:	fam-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2
BuildRequires:	log4cxx-devel
%{?with_dbus:BuildRequires:	pkgconfig}
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-qmake >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel
Requires:	QtDBus >= %{qtver}
Requires:	QtGui >= %{qtver}
Requires:	clucene-core >= 0.9.21
%{?with_dbus:Requires:	dbus-libs >= 1.0}
Requires:	exiv2-libs >= 0.21
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Here are the main features of Strigi Desktop Search: very fast
crawling, very small memory footprint, no hammering of the system,
pluggable backend (currently clucene and hyperestraier, sqlite3 and
xapian are in the works), communication between daemon and search
program over an abstract interface with two implementations: DBus and
a simple Unix socket. Especially the DBus interface makes it very easy
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
Requires:	libstdc++-devel

%description devel
Header files for strigi.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla strigi.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
install -d build
cd build
# note: package expects relative CMAKE_INSTALL_LIBDIR
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DFORCE_DEPS=1 \
	-DENABLE_FAM=1 \
	-DENABLE_INOTIFY=1 \
	-DENABLE_LOG4CXX=1

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
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/deepfind
%attr(755,root,root) %{_bindir}/deepgrep
%attr(755,root,root) %{_bindir}/lucene2indexer
%attr(755,root,root) %{_bindir}/rdfindexer
%attr(755,root,root) %{_bindir}/strigiclient
%attr(755,root,root) %{_bindir}/strigicmd
%attr(755,root,root) %{_bindir}/strigidaemon
%attr(755,root,root) %{_bindir}/xmlindexer
%attr(755,root,root) %{_libdir}/libsearchclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsearchclient.so.0
%attr(755,root,root) %{_libdir}/libstreamanalyzer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstreamanalyzer.so.0
%attr(755,root,root) %{_libdir}/libstreams.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstreams.so.0
%attr(755,root,root) %{_libdir}/libstrigihtmlgui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstrigihtmlgui.so.0
%attr(755,root,root) %{_libdir}/libstrigiqtdbusclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstrigiqtdbusclient.so.0
%dir %{_libdir}/strigi
%attr(755,root,root) %{_libdir}/strigi/*.so
%{?with_dbus:%{_datadir}/dbus-1/services/org.freedesktop.xesam.searcher.service}
%{?with_dbus:%{_datadir}/dbus-1/services/vandenoever.strigi.service}
%dir %{_datadir}/strigi
%{_datadir}/strigi/fieldproperties

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsearchclient.so
%attr(755,root,root) %{_libdir}/libstreamanalyzer.so
%attr(755,root,root) %{_libdir}/libstreams.so
%attr(755,root,root) %{_libdir}/libstrigihtmlgui.so
%attr(755,root,root) %{_libdir}/libstrigiqtdbusclient.so
%dir %{_libdir}/cmake/Strigi
%{_libdir}/cmake/Strigi/*.cmake
%dir %{_libdir}/cmake/LibSearchClient
%{_libdir}/cmake/LibSearchClient/LibSearchClientConfig.cmake
%dir %{_libdir}/cmake/LibStreamAnalyzer
%{_libdir}/cmake/LibStreamAnalyzer/LibStreamAnalyzerConfig.cmake
%{_libdir}/cmake/LibStreamAnalyzer/LibStreamAnalyzerConfigVersion.cmake
%dir %{_libdir}/cmake/LibStreams
%{_libdir}/cmake/LibStreams/LibStreamsConfig.cmake
%{_libdir}/cmake/LibStreams/LibStreamsConfigVersion.cmake
%{_libdir}/cmake/LibStreams/LibStreamsTargets-pld.cmake
%{_libdir}/cmake/LibStreams/LibStreamsTargets.cmake
%dir %{_includedir}/strigi
%{_includedir}/strigi/*.h
%{_includedir}/strigi/qtdbus
%{_pkgconfigdir}/libstreamanalyzer.pc
%{_pkgconfigdir}/libstreams.pc
