Summary:   Session applications to manage packages
Name:      gnome-packagekit
Version:   3.8.0
Release:   1%{?dist}
License:   GPLv2+
Group:     Applications/System
URL:       http://www.packagekit.org
Source0:   http://download.gnome.org/sources/gnome-packagekit/3.6/%{name}-%{version}.tar.xz

Requires:  gnome-icon-theme
Requires:  gnome-settings-daemon-updates
Requires:  dbus-x11 >= 1.1.2
Requires:  PackageKit >= 0.5.0
Requires:  PackageKit-libs >= 0.5.0
Requires:  PackageKit-device-rebind >= 0.5.0
Requires:  shared-mime-info
Requires:  iso-codes
Requires:  libcanberra >= 0.10
Requires:  upower >= 0.9.0

# required because KPackageKit provides exactly the same interface
Provides: PackageKit-session-service

BuildRequires: glib2-devel >= 2.25.8
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: libnotify-devel >= 0.7.0
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: libtool
BuildRequires: cairo-devel
BuildRequires: startup-notification-devel
BuildRequires: perl(XML::Parser)
BuildRequires: PackageKit-devel >= 0.5.0
BuildRequires: intltool
BuildRequires: xorg-x11-proto-devel
BuildRequires: fontconfig-devel
BuildRequires: libcanberra-devel
BuildRequires: libgudev1-devel
BuildRequires: libxslt
BuildRequires: upower-devel >= 0.9.0
BuildRequires: docbook-utils
BuildRequires: systemd-devel
BuildRequires: polkit-devel
BuildRequires: itstool

%description
gnome-packagekit provides session applications for the PackageKit API.
There are several utilities designed for installing, updating and
removing packages on your system.

%prep
%setup -q

%build
%configure --enable-systemd
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# nuke the ChangeLog file, it's huge
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/gnome-packagekit-*/ChangeLog

for i in gpk-application gpk-update-viewer gpk-install-local-file gpk-log gpk-prefs ; do
  desktop-file-install --delete-original                                \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications/                      \
    $RPM_BUILD_ROOT%{_datadir}/applications/$i.desktop
done

%find_lang %name --with-gnome

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gpk-*
%dir %{_datadir}/gnome-packagekit
%{_datadir}/gnome-packagekit/gpk-*.ui
%dir %{_datadir}/gnome-packagekit/icons
%dir %{_datadir}/gnome-packagekit/icons/hicolor
%dir %{_datadir}/gnome-packagekit/icons/hicolor/*
%dir %{_datadir}/gnome-packagekit/icons/hicolor/*/*
%{_datadir}/gnome-packagekit/icons/hicolor/*/*/*.png
%{_datadir}/gnome-packagekit/icons/hicolor/scalable/*/*.svg*
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg*
%{_datadir}/man/man1/*.1.gz
%{python_sitelib}/packagekit/*py*
%{_datadir}/applications/gpk-*.desktop
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/glib-2.0/schemas/org.gnome.packagekit.gschema.xml
%{_datadir}/GConf/gsettings/org.gnome.packagekit.gschema.migrate

%changelog
* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Wed Feb 06 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Wed Nov 28 2012 Richard Hughes <hughsient@gmail.com> - 3.6.1-2
- Don't crash if the window that invoked the task exits before
  the task starts up.
- Resolves: #756208

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1
- Minor spec file cleanup

* Fri Sep 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.0-2
- Depend on gnome-settings-daemon-updates. #699348
- Drop ancient obsoletes

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 28 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu May 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Sun Mar 18 2012 Richard Hughes <rhughes@redhat.com> - 3.3.92-1
- New upstream version.
- Many updated translations.

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-2
- Use systemd for session tracking

* Mon Feb 06 2012 Richard Hughes <rhughes@redhat.com> - 3.3.5-1
- New upstream version.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
