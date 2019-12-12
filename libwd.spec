Name: libwd
Summary: Huawei Accelerator Library
Version:1.2.1
Release: 1
Source: %{name}-%{version}.tar.gz
Vendor: Huawei Corporation
License: Apache-2.0
ExclusiveOS: linux
Group: System Environment/Kernel
Provides: %{name} = %{version}
URL:https://support.huawei.com
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Conflicts: %{name} < %{version}
BuildRequires: automake, autoconf, libtool
BuildRequires: gcc, make

%description
This package contains the Huawei Accelerator Library

%prep
%global debug_package %{nil}
%setup -c -n %{name}-%{version}

%build
cd warpdrive
sh autogen.sh
./configure
make

%install
mkdir -p ${RPM_BUILD_ROOT}/usr/lib64
install -p -m 0755 warpdrive/.libs/libwd.so.%{version} ${RPM_BUILD_ROOT}/usr/lib64
mkdir -p ${RPM_BUILD_ROOT}/usr/include/warpdrive
mkdir -p ${RPM_BUILD_ROOT}/usr/include/warpdrive/include
cp warpdrive/wd.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/wd_cipher.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/wd_comp.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/wd_dh.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/wd_digest.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/wd_rsa.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/wd_bmm.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/smm.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/config.h ${RPM_BUILD_ROOT}/usr/include/warpdrive
cp warpdrive/include/uacce.h ${RPM_BUILD_ROOT}/usr/include/warpdrive/include

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,root,root)
/usr/lib64/libwd.so.%{version}
/usr/lib64/libwd.so.1
%defattr(644,root,root)
/usr/include/warpdrive/wd.h
/usr/include/warpdrive/wd_cipher.h
/usr/include/warpdrive/wd_comp.h
/usr/include/warpdrive/wd_dh.h
/usr/include/warpdrive/wd_digest.h
/usr/include/warpdrive/wd_rsa.h
/usr/include/warpdrive/wd_bmm.h
/usr/include/warpdrive/smm.h
/usr/include/warpdrive/config.h
/usr/include/warpdrive/include/uacce.h


%pre
if [ "$1" = "2" ] ; then  #2: update
    rm -rf /usr/lib64/libwd.so   > /dev/null 2>&1 || true
fi

%post
if [[ "$1" = "1" || "$1" = "2" ]] ; then  #1: install 2: update
    cd /usr/lib64
    ln -sf libwd.so.%{version} libwd.so
fi
/sbin/ldconfig

%preun
if [ "$1" = "0" ] ; then  #0: uninstall
    rm -rf /usr/lib64/libwd.so    > /dev/null 2>&1 || true
fi

%postun
/sbin/ldconfig

%changelog

