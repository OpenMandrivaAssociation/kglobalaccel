%define major 5
%define libname %mklibname KF5GlobalAccel %{major}
%define devname %mklibname KF5GlobalAccel -d
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name: kglobalaccel
Version:	5.112.0
Release:	1
Source0: http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
Summary: The KDE Frameworks 5 global accelerator library
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: cmake(KF5Crash)
BuildRequires: cmake(KF5DBusAddons)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5WindowSystem)
BuildRequires: cmake(KF5Service)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(x11)
# For QCH format docs
BuildRequires: doxygen
BuildRequires: qt5-assistant
Requires: %{libname} = %{EVRD}
Requires: %{name}-runtime
Obsoletes: %{name}-dbus-interfaces < 5.240.0-1

%description
KGlobalAccel provides access to global accelerator keys.

%package -n %{libname}
Summary: The KDE Frameworks 5 global accelerator library
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
KGlobalAccel provides access to global accelerator keys.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/KDE and Qt
Requires: %{libname} = %{EVRD}

%description -n %{devname}
KGlobalAccel provides access to global accelerator keys.

%package -n %{name}-devel-docs
Summary: Developer documentation for %{name} for use with Qt Assistant
Group: Documentation
Suggests: %{devname} = %{EVRD}

%description -n %{name}-devel-docs
Developer documentation for %{name} for use with Qt Assistant

%prep
%autosetup -p1
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build

L="$(pwd)/%{name}.lang"
cd %{buildroot}
for i in .%{_datadir}/locale/*/LC_MESSAGES/*.qm; do
    LNG=$(echo $i |cut -d/ -f5)
    echo -n "%lang($LNG) " >>$L
    echo $i |cut -b2- >>$L
done

# As per
# https://community.kde.org/Plasma/Plasma_6#Packaging_notes
# we'll drop the runtime files from KF5 and use the KF6 versions
# even before the official release.
rm -f %{buildroot}%{_prefix}/lib/systemd/user/plasma-kglobalaccel.service

%files -f %{name}.lang
%{_datadir}/qlogging-categories5/kglobalaccel.categories
%{_datadir}/qlogging-categories5/kglobalaccel.renamecategories
%{_bindir}/kglobalaccel5
%dir %{_libdir}/qt5/plugins/org.kde.kglobalaccel5.platforms
%{_libdir}/qt5/plugins/org.kde.kglobalaccel5.platforms/KF5GlobalAccelPrivateXcb.so
%{_datadir}/dbus-1/services/org.kde.kglobalaccel.service
%{_datadir}/kservices5/kglobalaccel5.desktop
%{_datadir}/dbus-1/interfaces/kf5_*

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/libKF5GlobalAccel.so
%{_libdir}/cmake/KF5GlobalAccel
%{_libdir}/qt5/mkspecs/modules/*

%files -n %{name}-devel-docs
%{_docdir}/qt5/*.{tags,qch}
