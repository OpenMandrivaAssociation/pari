%define	pari_version	2.5.4
%define	gp2c_version	0.0.7pl5
%define	lib_name_orig	lib%{name}
%define	lib_major	2
%define	lib_name	%mklibname %{name} %{lib_major}

Summary:	PARI/GP - Number Theory-oriented Computer Algebra System
Name:		pari
Version:	%{pari_version}
Release:	1
License:	GPL+
Group:		Sciences/Mathematics
URL:		http://pari.math.u-bordeaux.fr/
Source0:	http://pari.math.u-bordeaux.fr/pub/pari/unix/pari-%{pari_version}.tar.gz
Source1:	http://pari.math.u-bordeaux.fr/pub/pari/packages/elldata.tgz
Source2:	http://pari.math.u-bordeaux.fr/pub/pari/packages/galdata.tgz
Source3:	http://pari.math.u-bordeaux.fr/pub/pari/packages/seadata.tgz
Source4:	http://pari.math.u-bordeaux.fr/pub/pari/packages/nftables.tgz
Source5:	http://pari.math.u-bordeaux.fr/pub/pari/packages/galpol.tgz
Source6:	http://pari.math.u-bordeaux.fr/pub/pari/GP2C/gp2c-%{gp2c_version}.tar.gz
Source7:        gp.desktop
Source8:	%{name}.rpmlintrc
Patch0:         pari-2.5.1-xdgopen.patch
Patch1:         pari-2.5.1-optflags.patch
Patch10:        pari-2.5.4-missing-field-init.patch
Patch11:        pari-2.5.3-declaration-not-prototype.patch
Patch12:        pari-2.5.2-clobbered.patch

BuildRequires:	perl-devel
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	texlive
BuildRequires:	emacs
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

%package	data
Group:		Sciences/Mathematics
Summary:	Optional pari data packages
Requires:	%{name} = %{EVRD}

%description	data
  elldata is PARI/GP version of J. E. Cremona Elliptic Curve Data,
needed by ellsearch and ellidentify.
  galdata is needed by polgalois to compute Galois group in degrees
8 through 11.
  seadata is needed by ellap for large primes.
  nftables is a repackaging of the historical megrez number field
tables (errors fixed, 1/10th the size, easier to use).

%package -n	%{lib_name}
Group:		System/Libraries
Summary:	Shared PARI library
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the libraries needed to run pari.

%package -n	%{lib_name}-devel
Group:		System/Libraries
Summary:	Development files for PARI shared library
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the header files needed to develop
applications using pari.

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

%prep
%setup -q -a1 -a2 -a3 -a4 -a5 -a6
mv -f nftables data

# Use xdg-open rather than xdvi to display DVI files (#530565)
%patch0

# Use our optflags, not upstream's
%patch1
sed -i -e 's|@OPTFLAGS@|%{optflags} -Wall -Wextra -Wstrict-prototypes|' config/get_cc

# Fix compiler warnings
# http://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=1316
%patch10
%patch11
%patch12

# Avoid unwanted rpaths
sed -i "s|runpathprefix='.*'|runpathprefix=''|" config/get_ld

%build
%define pkgdocdir	%{_docdir}/%{name}
%define pkgdatadir	%{_datadir}/%{name}-%{pari_version}

# Using --libdir to properly link with newer interface
# Using --disable-tls for safety due to other packages linked to pari
sh Configure						\
	--prefix=%{_prefix}				\
	--includedir=%{_includedir}/%{name}		\
	--datadir=%{pkgdatadir}/data			\
	--sysdatadir=%{_libdir}/%{name}-%{pari_version}	\
	--share-prefix=%{_datadir}			\
	--host=%{_arch}-%{_os}				\
	--graphic=X11					\
	--with-gmp					\
	--libdir=%{buildroot}%{_libdir}			\
	--disable-tls

make gp docpdf bench

# gp2c
cd gp2c-%{gp2c_version}
%configure	--datadir=%{pkgdatadir}			\
		--with-paricfg=../Olinux-%{_arch}/pari.cfg

# FIXME just satisfy build dependency
ln -sf ../config/missing desc

make
cd ..

%install

# pari, libpari & libpari-devel
%makeinstall_std					\
	READMEDIR='$(DESTDIR)'%{pkgdocdir}		\
	LIBDIR='$(DESTDIR)'%{_libdir}			\
	DOCDIR='$(DESTDIR)'%{pkgdocdir}

# gp2c
cd gp2c-%{gp2c_version}
%makeinstall_std					\
	docdir=%{_docdir}
cd ..

# Install global configuration file.
mkdir %{buildroot}/%{_sysconfdir}
# Add some more reasonable "commented" sample configurations
sed	-e 's@/usr/local/@%{_prefix}/@'				\
	-e 's@path =.*@path = "%{pkgdatadir}:.:~/gpdir"@'	\
	-e 's@lib/gpalias@misc/gpalias@'			\
	misc/gprc.dft > %{buildroot}/%{_sysconfdir}/gprc

# don't need to install this file...
rm -f %{pkgdocdir}/%{name}/Makefile

# gphelp wants docs in %{pkgdatadir}/data/doc (removing the /data/ requirement)
ln -sf %{pkgdocdir} %{buildroot}%{pkgdatadir}/doc
perl -pi -e 's@%{pkgdatadir}/data@%{pkgdatadir}@;'		\
	%{buildroot}/%{_bindir}/gphelp

# Desktop menu entry
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE7}

%files
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/gprc
%{_bindir}/gp-2.5
%{_bindir}/gp
%{_bindir}/gphelp
%{_bindir}/tex2mail
%{_mandir}/man1/[^g]*.1*
%{_mandir}/man1/gp.1*
%{_mandir}/man1/gp-*.1*
%{_mandir}/man1/gphelp.1*
%doc AUTHORS CHANGES COMPAT MACHINES README
%dir %{pkgdatadir}
%{pkgdatadir}/doc
%{_datadir}/applications/gp.desktop

%files data
%dir %{pkgdatadir}/data
%{pkgdatadir}/data/*

%files -n %{lib_name}
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%{_includedir}/%{name}
%{_libdir}/*.so
%dir %{_libdir}/%{name}-%{pari_version}
%dir %{_libdir}/%{name}-%{pari_version}/*

%files -n gp2c
%attr(755,root,root) %{_bindir}/gp2c*
%doc gp2c-%{gp2c_version}/{AUTHORS,ChangeLog,NEWS,README,BUGS}
%{pkgdatadir}/gp2c
%{_mandir}/man1/gp2c*.1*
