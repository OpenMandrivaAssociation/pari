%define	name		pari
%define	pari_version	2.4.3.alpha
%define	gp2c_version	0.0.5pl10
%define	release		%mkrel 1
%define	lib_name_orig	lib%{name}
%define	lib_major	2
%define	lib_name	%mklibname %{name} %{lib_major}

Summary:	PARI/GP - Number Theory-oriented Computer Algebra System
Name:		%{name}
Version:	%{pari_version}
Release:	%{release}
License:	GPL
Group:		Sciences/Mathematics
Source0:	http://pari.math.u-bordeaux.fr/pub/pari/unix/pari-%{pari_version}.tar.gz
Source1:	http://pari.math.u-bordeaux.fr/pub/pari/packages/elldata.tgz
Source2:	http://pari.math.u-bordeaux.fr/pub/pari/packages/galdata.tgz
Source3:	http://pari.math.u-bordeaux.fr/pub/pari/packages/seadata.tgz
Source4:	http://pari.math.u-bordeaux.fr/pub/pari/packages/nftables.tgz
Source5:	http://pari.math.u-bordeaux.fr/pub/pari/GP2C/gp2c-%{gp2c_version}.tar.gz
URL:		http://pari.math.u-bordeaux.fr/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Patch0:		pari-arch.patch
Patch1:		pari-Werror=format.patch
Patch2:		pari-gphelp.patch
Patch3:		pari-runpath.patch

BuildRequires:	perl-devel
BuildRequires:	libgmp-devel
BuildRequires:	libx11-devel
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	tetex tetex-dvips
BuildRequires:	emacs
Requires:	perl
Requires:	xdg-utils

%description
PARI/GP is a widely used computer algebra system designed for fast
computations in number theory (factorizations, algebraic number theory,
elliptic curves...), but also contains a large number of other useful
functions to compute with mathematical entities such as matrices,
polynomials, power series, algebraic numbers, etc., and a lot of
transcendental functions. PARI is also available as a C library to allow
for faster computations.

%package	data
Group:		Sciences/Mathematics
Summary:	Optional pari data packages
Requires:	%{name} > 2.2.10

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

%description -n %{lib_name}
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
%setup -q -a1 -a2 -a3 -a4 -a5
mv -f nftables data

%patch0	-p1
%patch1	-p1
%patch2	-p1
%patch3	-p1

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

make gp doc bench

# gp2c
cd gp2c-%{gp2c_version}
%configure	--datadir=%{pkgdatadir}			\
		--with-paricfg=../Olinux-%{_arch}/pari.cfg
make
cd ..

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post   -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/gprc
%{_bindir}/gp-2.4
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

%files	data
%defattr(-,root,root)
%dir %{pkgdatadir}/data
%{pkgdatadir}/data/*

%files	-n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files	-n %{lib_name}-devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/*.so
%dir %{_libdir}/%{name}-%{pari_version}
%dir %{_libdir}/%{name}-%{pari_version}/*

%files	-n gp2c
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/gp2c*
%doc gp2c-%{gp2c_version}/{AUTHORS,ChangeLog,NEWS,README,BUGS}
%{pkgdatadir}/gp2c
%{_mandir}/man1/gp2c*.1*

