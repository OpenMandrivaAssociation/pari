%define	pari_version	2.5.2
%define	gp2c_version	0.0.7pl3
%define	lib_name_orig	lib%{name}
%define	lib_major	2
%define	lib_name	%mklibname %{name} %{lib_major}

Summary:	PARI/GP - Number Theory-oriented Computer Algebra System
Name:		pari
Version:	%{pari_version}
Release:	1
License:	GPL
Group:		Sciences/Mathematics
Source0:	http://pari.math.u-bordeaux.fr/pub/pari/unix/pari-%{pari_version}.tar.gz
Source1:	http://pari.math.u-bordeaux.fr/pub/pari/packages/elldata.tgz
Source2:	http://pari.math.u-bordeaux.fr/pub/pari/packages/galdata.tgz
Source3:	http://pari.math.u-bordeaux.fr/pub/pari/packages/seadata.tgz
Source4:	http://pari.math.u-bordeaux.fr/pub/pari/packages/nftables.tgz
Source5:	http://pari.math.u-bordeaux.fr/pub/pari/packages/galpol.tgz
Source6:	http://pari.math.u-bordeaux.fr/pub/pari/GP2C/gp2c-%{gp2c_version}.tar.gz
URL:		http://pari.math.u-bordeaux.fr/

Patch0:		pari-arch.patch
Patch1:		pari-gphelp.patch
Patch2:		pari-runpath.patch
# from sagemath
Patch3:		mp.c.patch

BuildRequires:	perl-devel
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(x11)
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

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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


%changelog
* Fri Aug 17 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.5.2-1
+ Revision: 815198
- Update to latest upstream release.

* Thu Jun 14 2012 Andrey Bondrov <abondrov@mandriva.org> 2.5.1-2
+ Revision: 805709
- Bump release

  + Alexander Khrukin <akhrukin@mandriva.org>
    - version update 2.5.1

* Tue Jan 24 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.5.0-1
+ Revision: 767462
- Update to latest upstream release

* Fri Mar 04 2011 Paulo Andrade <pcpa@mandriva.com.br> 2.4.3.alpha-2
+ Revision: 641867
- Add latest sagemath patches

* Thu Nov 11 2010 Paulo Andrade <pcpa@mandriva.com.br> 2.4.3.alpha-1mdv2011.0
+ Revision: 595897
- Update to pari 2.4.3-alpha

* Tue Jul 27 2010 Paulo Andrade <pcpa@mandriva.com.br> 2.3.5-8mdv2011.0
+ Revision: 560893
- Use xdg-open in gphelp instead of xdvi

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 2.3.5-7mdv2010.1
+ Revision: 503562
- New version 2.3.5

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 2.3.4-6mdv2010.1
+ Revision: 503558
- rebuild for new gmp

* Wed Feb 03 2010 Paulo Andrade <pcpa@mandriva.com.br> 2.3.4-5mdv2010.1
+ Revision: 499828
- Update to gpc-0.0.5pl9
- Change from requires to suggests of xdvi

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Feb 25 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.4-3mdv2009.1
+ Revision: 344843
- rebuild against new readline

* Fri Feb 20 2009 Paulo Andrade <pcpa@mandriva.com.br> 2.3.4-2mdv2009.1
+ Revision: 343068
- Use gmp instead of builtin math library.
  gmp is significantly faster for calculations with large numbers.
  Correct gphelp, that was expecting to find documentation outside
  %%{_docdir}.
  xdvi is now required, as it is used to view documentation.
  xdvi cannot be installed due to bug #48029; as an alternative, temporary
  solution, it is possible to either use patch in #38016, or set the
  GPXDVI environment variable (a good option is the okular program).

* Wed Feb 18 2009 Paulo Andrade <pcpa@mandriva.com.br> 2.3.4-1mdv2009.1
+ Revision: 342731
- Update to latest upstream release, version 2.3.4
  o gp2c updated to 0.0.5pl7.
  o Corrected spec bug that set pari version to gp2c one.
  o Added extra optional pari data packages to the -data rpm.
  o Added missing BuildRequires and Requires.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - parallel build is broken
    - BuildRequires tetex tetex-dvips
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

