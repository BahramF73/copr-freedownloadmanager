%global __brp_check_rpaths %{nil}
%define debug_package %{nil}

Name:           freedownloadmanager
Version:        6.34.0.6878
Release:        1%{?dist}
Summary:        FDM is a powerful modern download accelerator and organizer
License:        Freeware
URL:            https://www.freedownloadmanager.org/
Source0:        https://files2.freedownloadmanager.org/6/latest/freedownloadmanager.deb

BuildRequires:  binutils
BuildRequires:  tar

Requires:       openssl
Requires:       xdg-utils
Requires:       ffmpeg
Requires:       libtorrent
Requires:       gstreamer1-plugins-base

%description
FDM is a powerful modern download accelerator and organizer.

%prep
mkdir -p %{name}-%{version}
ar x %{SOURCE0}
tar -xJf data.tar.xz -C %{name}-%{version}

%build
# No build step required, as we are converting from deb

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{name}-%{version}

# Modify desktop file paths
sed -i 's|\/opt\/freedownloadmanager\/icon\.png|freedownloadmanager|g' \
    ./usr/share/applications/freedownloadmanager.desktop
sed -i 's|\/opt\/freedownloadmanager\/fdm|\/usr\/bin\/fdm|g' \
    ./usr/share/applications/freedownloadmanager.desktop

# Add StartupWMClass
sed -i '/^Exec=/a StartupWMClass=fdm' \
    ./usr/share/applications/freedownloadmanager.desktop

# Copy files to buildroot
cp -dpr --no-preserve=ownership opt usr %{buildroot}

# Create icon symlink
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps
ln -sv /opt/%{name}/icon.png \
    %{buildroot}/usr/share/icons/hicolor/256x256/apps/%{name}.png

# Create binary symlink
mkdir -p %{buildroot}/usr/bin
ln -sv /opt/%{name}/fdm %{buildroot}/usr/bin/fdm

%files
%defattr(-,root,root,-)
/usr/bin/fdm
/usr/share/applications/freedownloadmanager.desktop
/usr/share/appdata/freedownloadmanager.appdata.xml
/usr/share/icons/hicolor/256x256/apps/%{name}.png
/opt/%{name}/*
