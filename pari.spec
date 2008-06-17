%define	name		pari
%define	version	2.1.7
%define	gp2c_version	0.0.4pl3
%define	release		%mkrel 4
%define	lib_name_orig	lib%{name}
%define	lib_major	1
%define	lib_name	%mklibname %{name} %{lib_major}

Summary:	PARI/GP - Number Theory-oriented Computer Algebra System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sciences/Mathematics
Source0:	ftp://megrez.math.u-bordeaux.fr/pub/pari/unix/%{name}-%{version}.tar.bz2
Source1:	ftp://megrez.math.u-bordeaux.fr/pub/pari/galdata.tar.bz2
Source2:    ftp://megrez.math.u-bordeaux.fr/pub/pari/GP2C/gp2c-%{gp2c_version}.tar.bz2
URL:		http://pari.math.u-bordeaux.fr/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	perl-devel
BuildRequires:  libx11-devel
BuildRequires:	readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  tetex tetex-dvips

%description
PARI/GP is a widely used computer algebra system designed for fast
computations in number theory (factorizations, algebraic number theory,
elliptic curves...), but also contains a large number of other useful
functions to compute with mathematical entities such as matrices,
polynomials, power series, algebraic numbers, etc., and a lot of
transcendental functions. PARI is also available as a C library to allow
for faster computations.

%package -n	%{lib_name}
Group:          System/Libraries
Summary:        Shared PARI library
Provides:	    %{lib_name_orig} = %{version}-%{release}

%description -n %{lib_name}
This package contains the libraries needed to run pari.

%package -n	%{lib_name}-devel
Group:          System/Libraries
Summary:        Development files for PARI shared library
Requires:       %{lib_name} = %{version}-%{release}
Provides:	    %{lib_name_orig}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the header files needed to develop
applications using pari.

%package -n	gp2c
Summary:        PARI/GP to C translator
Version:        %{gp2c_version}
Group:          Development/C
Requires:       pari

%description -n	gp2c
PARI/GP to C translator. Use it to compile your own C
programs which use pari library, without necessarily being
a C programmer.
Note: use gp2c-run to run your programs inside the PARI/GP
environment.

%prep
%setup -q -T -b0 -a1 -a2
mkdir data && mv COS* RES* data

%build
%define _pkgdocdir	%{_docdir}/%{name}-%{version}
%define _pkgincludedir	%{_includedir}/%{name}-%{version}
%define _pkgdatadir	%{_datadir}/%{name}-%{version}

#  CFLAGS="${CFLAGS:--O2 -fomit-frame-pointer -pipe -march=i586 -mcpu=pentiumpro }" ; export CFLAGS ;
#  CXXFLAGS="${CXXFLAGS:--O2 -fomit-frame-pointer -pipe -march=i586 -mcpu=pentiumpro }" ; export CXXFLAGS ;
#  FFLAGS="${FFLAGS:--O2 -fomit-frame-pointer -pipe -march=i586 -mcpu=pentiumpro }" ; export FFLAGS ;
sed	-e 's;OPTFLAGS=-O3;OPTFLAGS="%{optflags}";g' \
	-e 's,hpux-\*)\ DLCFLAGS=-fPIC,hpux-\*\|linux-\*)\ DLCFLAGS=-fPIC,g' \
	Configure > Configure_
sh Configure_	\
        --prefix=%{_prefix}			\
	--includedir=%{_pkgincludedir}		\
	--miscdir=%{_pkgdatadir}		\
	--datadir=%{_pkgdatadir}/galdata	\
        --share-prefix=%{_datadir}		\
	--host=%{_arch}-%{_os}			\
	--graphic=X11

make gp doc bench

# Setup configuration file
sed	-e 's,/usr/local/,'%{_prefix}/',g'\
	-e 's,"[^"	 ]*/share/,"'%{_datadir}/',g'\
	-e 's,"[^"	 ]*/bin/,"'%{_bindir}/',g'\
	-e 's,"[^"	 ]*/gpalias","'%{_pkgdatadir}/misc/gpalias'",g'\
	-e 's,"[^"	 ]*/galdata","'%{_pkgdatadir}/galdata'",g'\
	-e '/^\\\\[	 ]*\(read "\|compatible =\|secure =\)/ s/^\\\\[	 ]*//'\
	misc/gprc.dft >gprc

# gp2c
cd gp2c-%{gp2c_version}
%configure	--datadir=%{_pkgdatadir} \
		--with-paricfg=../Olinux-%{_arch}/dft.Config.in
%make
cd ..

%install
rm -rf $RPM_BUILD_ROOT

# pari, libpari & libpari-devel
%makeinstall_std READMEDIR='$(DESTDIR)'%{_pkgdocdir} LIBDIR='$(DESTDIR)'%{_libdir}

# Create links to the interesting directories in the standard doc folder
# unless _pkgdocdir and _pkgdatadir are identical
for i in doc emacs examples misc; do
  if test ! -d "$RPM_BUILD_ROOT"%{_pkgdocdir}/"$i"; then
    ln -s %{_pkgdatadir}/"$i" "$RPM_BUILD_ROOT"%{_pkgdocdir}/"$i"
  fi
done

# libpari-static
#install Olinux-%{_target_cpu}/libpari.a $RPM_BUILD_ROOT%{_libdir}/libpari.a

# gp2c
cd gp2c-%{gp2c_version}
%makeinstall_std
cd ..


# Install global configuration file.
# /etc is hardcoded into gp, so do NOT use the _sysconfdir macro.
mkdir "$RPM_BUILD_ROOT"/etc
cp gprc "$RPM_BUILD_ROOT"/etc

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post   -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/gprc
%attr(755,root,root) %{_bindir}/gp-2.1
%attr(755,root,root) %{_bindir}/gp
%attr(755,root,root) %{_bindir}/gphelp
%attr(755,root,root) %{_bindir}/tex2mail
%{_mandir}/man1/[^g]*.1*
%{_mandir}/man1/gp.1*
%{_mandir}/man1/gphelp.1*
%doc %{_pkgdocdir}
%{_pkgdatadir}

%files -n %{lib_name}
%defattr(644,root,root,755)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
#%{_includedir}/%{name}-%{version}
%{_libdir}/*.so

%files -n gp2c
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gp2c*
%doc gp2c-%{gp2c_version}/{AUTHORS,ChangeLog,NEWS,README,BUGS,doc/gp2c.dvi,doc/html/*}
%{_pkgdatadir}/gp2c
%{_mandir}/man1/gp2c*.1*

