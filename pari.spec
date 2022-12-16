%define _disable_lto 1

%define	liboname	lib%{name}
%define	major	8
%define	libname	%mklibname %{name}
%define	devname	%mklibname %{name} -d
%define	oldlibname	%mklibname %{name} %{major}

%define	shortver	%(echo %version | cut -d\. -f 1,2)
%define	gp2c_version	0.0.12

Summary:	PARI/GP - Number Theory-oriented Computer Algebra System
Name:		pari
Version:	2.15.1
Release:	1
License:	GPL+
Group:		Sciences/Mathematics
URL:		https://pari.math.u-bordeaux.fr/
Source0:	https://pari.math.u-bordeaux.fr/pub/pari/unix/pari-%{version}.tar.gz
Source1:	https://pari.math.u-bordeaux.fr/pub/pari/GP2C/gp2c-%{gp2c_version}.tar.gz
Source2:	https://pari.math.u-bordeaux.fr/pub/pari/packages/elldata.tgz
Source3:	https://pari.math.u-bordeaux.fr/pub/pari/packages/galdata.tgz
Source4:	https://pari.math.u-bordeaux.fr/pub/pari/packages/seadata.tgz
Source5:	https://pari.math.u-bordeaux.fr/pub/pari/packages/nftables.tgz
Source6:	https://pari.math.u-bordeaux.fr/pub/pari/packages/galpol.tgz
Source7:	pari-gp.xpm
Source8:	%{name}.rpmlintrc
# Use xdg-open rather than xdvi to display DVI files (#530565)
Patch0:		pari-2.13.3-xdgopen.patch
# Use our optflags, not upstream's
Patch1:		pari-2.13.3-optflags.patch
# Fix docs path
Patch2:		pari-2.13.3-gp2c_doc.patch
# Use bsdtar style
Patch100:	pari-2.13.3-fix_install_use_bsdtar_style.patch
# Fix compiler warnings
# http://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=1316
Patch10:	pari-2.13.3-missing-field-init.patch
#Patch11:	pari-2.13.3-declaration-not-prototype.patch
Patch12:	pari-2.15.1-clobbered.patch

BuildRequires:	perl-devel
BuildRequires:	fltk-devel
BuildRequires:	gmp-devel
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(x11)
BuildRequires:	texlive
#BuildRequires:	emacs
Requires:	perl
Requires:	xdg-utils

%description
PARI is a widely used computer algebra system designed for fast computations in
number theory (factorizations, algebraic number theory, elliptic curves...),
but also contains a large number of other useful functions to compute with
mathematical entities such as matrices, polynomials, power series, algebraic
numbers, etc., and a lot of transcendental functions.

This package contains the shared libraries. The interactive
calculator PARI/GP is in package pari-gp.

%files
%doc AUTHORS CHANGES* COMPAT README
%config(noreplace) %{_sysconfdir}/gprc
%{_bindir}/gp-%{shortver}
%{_bindir}/gp
%{_bindir}/gphelp
%{_bindir}/tex2mail
%{_mandir}/man1/[^g]*.1*
%{_mandir}/man1/gp.1*
%{_mandir}/man1/gp-*.1*
%{_mandir}/man1/gphelp.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/examples/
%{_datadir}/%{name}/misc
%{_datadir}/%{name}/PARI
%{_datadir}/%{name}/pari.desc
%exclude %{_datadir}/%{name}/elldata
%exclude %{_datadir}/%{name}/galdata
%exclude %{_datadir}/%{name}/galpol
%exclude %{_datadir}/%{name}/nftables
%exclude %{_datadir}/%{name}/seadata
%{_iconsdir}/hicolor/*/apps/%{name}-gp.png
%{_datadir}/pixmaps/%{name}-gp.xpm
%{_datadir}/applications/openmandriva-%{name}.desktop
%{_docdir}/%{name}/*

#-----------------------------------------------------------------------

%package	data
Group:		Sciences/Mathematics
Summary:	Optional pari data packages
Requires:	%{name} = %{EVRD}

%description	data
 - elldata is PARI/GP version of J. E. Cremona Elliptic Curve Data,
needed by ellsearch and ellidentify.
 - galdata is needed by polgalois to compute Galois group in degrees
8 through 11.
 - seadata is needed by ellap for large primes.
 - nftables is a repackaging of the historical megrez number field
tables (errors fixed, 1/10th the size, easier to use).

%files data
%{_datadir}/%{name}/elldata
%{_datadir}/%{name}/galdata
%{_datadir}/%{name}/galpol
%{_datadir}/%{name}/nftables
%{_datadir}/%{name}/seadata

#-----------------------------------------------------------------------

%package -n	%{libname}
Group:		System/Libraries
Summary:	Shared PARI library
Provides:	%{liboname} = %{version}-%{release}
# Intentionally unversioned, because libname should not contain version number
Obsoletes:	%{oldlibname}

%description -n	%{libname}
This package contains the libraries needed to run pari.

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

#-----------------------------------------------------------------------

%package -n	%{devname}
Group:		System/Libraries
Summary:	Development files for PARI shared library
Requires:	%{libname} = %{version}-%{release}
Provides:	%{liboname}-devel = %{version}-%{release}
Obsoletes:	%{_lib}%{name}2-devel <= %{version}-%{release}

%description -n %{devname}
This package contains the header files needed to develop
applications using pari.

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/%{name}

#-----------------------------------------------------------------------

%package -n	gp2c
Summary:	PARI/GP to C translator
Version:	%{gp2c_version}
Group:		Development/C
Requires:	pari

%description -n	gp2c
PARI/GP to C translator. Use it to compile your own C
programs which use pari library, without necessarily being
a C programmer.
Note: use gp2c-run to run your programs inside the PARI/GP
environment.

%files -n gp2c
%{_bindir}/gp2c*
%{_datadir}/%{name}/gp2c
%{_datadir}/%{name}/doc
%{_mandir}/man1/gp2c*.1*
%{_docdir}/gp2c/gp2c.{dvi,html,pdf}
%{_docdir}/gp2c/gp2c001.png
%{_docdir}/gp2c/type.{dvi,html,pdf}
%{_docdir}/gp2c/type001.png
%doc gp2c-%{gp2c_version}/{AUTHORS,ChangeLog,NEWS,README,BUGS}

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -a1
#tar -xf %{SOURCE1}
tar -xf %{SOURCE2}
tar -xf %{SOURCE3}
tar -xf %{SOURCE4}
tar -xf %{SOURCE5}
tar -xf %{SOURCE6}

# move all data in data
mv -f nftables data

# Use our optflags, not upstream's (patch1)
sed -i -e 's|@OPTFLAGS@|%{optflags} -Wall -Wextra -Wstrict-prototypes -Wno-implicit-fallthrough|' config/get_cc

# Avoid unwanted rpaths
sed -i "s|runpathprefix='.*'|runpathprefix=''|" config/get_ld

%ifarch %{ix86}
# Apparently only required in Mandriva due to 'uname -m' parsing
ln -s Olinux-i386 Olinux-i686
%endif

%build
%setup_compile_flags
export CPPFLAGS=$CXXFLAGS
export OPTFLAGS=%{optflgs}

# Using --libdir to properly link with newer interface
# Using --disable-tls for safety due to other packages linked to pari
# (fedora)
# For as yet unknown reasons, 32-bit pari becomes extremely slow if built with
# pthread support. Enable it for 64-bit only until we can diagnose the issue.
./Configure \
	--prefix=%{_prefix} \
	--share-prefix=%{_datadir} \
	--bindir=%{_bindir} \
	--datadir=%{_datadir}/%{name} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir}/man1 \
%ifnarch %{ix86}
	--mt=pthread \
%endif
	--enable-tls \
	--with-fltk \
	--with-gmp

%make_build gp # bench # docpdf

# gp2c
pushd gp2c-%{gp2c_version}
%configure \
	--datadir=%{_datadir}/%{name} \
	--with-paricfg=../Olinux-%{_arch}/pari.cfg

%make_build
popd

%install
# pari, libpari & libpari-devel
export DESTDIR="%{buildroot}"
%make_install \
	INSTALL="install -p" \
	READMEDIR=%{buildroot}%{_docdir}/%{name} \
	LIBDIR=%{buildroot}%{_libdir} \
	DOCDIR=%{buildroot}%{_docdir}/%{name}

# gp2c
pushd gp2c-%{gp2c_version}
%make_install \
	docdir=%{_docdir}
popd

# Move the library directory on 64-bit systems
if [ "%{_lib}" != "lib" ]; then
	mkdir -p %{buildroot}%{_libdir}
	mv %{buildroot}%{_prefix}/lib/pari %{buildroot}%{_libdir}
fi

# Site-wide gprc
mkdir -p %{buildroot}%{_sysconfdir}
install -p -m 644 misc/gprc.dft %{buildroot}%{_sysconfdir}/gprc

# Install global configuration file.
mkdir -p %{buildroot}/%{_sysconfdir}
# Add some more reasonable "commented" sample configurations
sed	-e 's@/usr/local/@%{_prefix}/@'				\
	-e 's@path =.*@path = "%{_datadir}/%{name}:.:~/gpdir"@'	\
	-e 's@lib/gpalias@misc/gpalias@'			\
	misc/gprc.dft > %{buildroot}/%{_sysconfdir}/gprc

# don't need to install this file...
rm -f %{_docdir}/%{name}/%{name}/Makefile

# gphelp wants docs in %{_datadir}/%{name}/data/doc (removing the /data/ requirement)
ln -sf %{_docdir}/%{name} %{buildroot}%{_datadir}/%{name}/doc
sed -i -e 's@%{_datadir}/%{name}/data@%{_datadir}/%{name}@;' %{buildroot}/%{_bindir}/gphelp

# icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -size "${d}x${d}" \
		%{SOURCE7} \
		%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}-gp.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
install -pm 0755 %{SOURCE7} %{buildroot}%{_datadir}/pixmaps/%{name}-gp.xpm

# .desktop file
install -dm 0755 %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=PARI/GP
Comment="Programmable calculator based on PARI"
Exec=gp
Icon=%{name}-gp
Terminal=true
Type=Application
Categories=Application;Education;Science;Math;
Encoding=UTF-8
StartupNotify=false
X-Vendor=OpenMandriva
EOF

%check
export GP_DATA_DIR=$PWD/data
make test-all ||:

# .desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop

