Name:       augeas
Summary:    A library for changing configuration files
Version:    1.12.0
Release:    1
Group:      System/Libraries
License:    LGPLv2+
URL:        http://augeas.net/
Source0:    http://download.augeas.net/%{name}-%{version}.tar.gz
Patch0:     001-dont-git.patch
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  readline-devel
BuildRequires:  bison
BuildRequires:  flex

%description
A library for programmatically editing configuration files. Augeas parses
configuration files into a tree structure, which it exposes through its
public API. Changes made through the API are written back to the initially
read files.

The transformation works very hard to preserve comments and formatting
details. It is controlled by ``lens'' definitions that describe the file
format and the transformation into a tree.

%package libs
Summary:    Libraries for %{name}
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
The libraries for %{name}.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch0 -p1

%build

./autogen.sh --disable-static --prefix=%{_usr} \
        --libdir=%{_libdir} \
	--gnulib-srcdir=.gnulib
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} AUTHORS NEWS

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/augtool
%{_bindir}/augparse
%{_bindir}/augmatch
%{_bindir}/fadot
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim

%files libs
%defattr(-,root,root,-)
%license COPYING
%{_datadir}/augeas
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/*
%{_docdir}/%{name}-%{version}
