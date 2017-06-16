Name:       augeas
Summary:    A library for changing configuration files
Version:    1.6.0
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

%prep
%setup -q -n %{name}-%{version}/upstream
%patch0 -p1

%build

./autogen.sh --disable-static --prefix=%{_usr} \
	--gnulib-srcdir=.gnulib
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/augtool
%{_bindir}/augparse
%{_bindir}/fadot
%doc %{_mandir}/man1/*
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim

%files libs
%defattr(-,root,root,-)
%{_datadir}/augeas
%{_libdir}/*.so.*
%doc AUTHORS COPYING NEWS

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc
