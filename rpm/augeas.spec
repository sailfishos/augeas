Name:       augeas
Summary:    A library for changing configuration files
Version:    1.14.1
Release:    1
License:    LGPLv2+
URL:        https://github.com/sailfishos/augeas
Source0:    %{name}-%{version}.tar.gz
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
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
The libraries for %{name}.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build

./autogen.sh --disable-static --prefix=%{_usr} \
        --libdir=%{_libdir} \
        --gnulib-srcdir=.gnulib
%make_build

%install

%make_install

# The tests/ subdirectory contains lenses used only for testing, and
# so it shouldn't be packaged.
rm -r $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/dist/tests

find %{buildroot} -name '*.la' -exec rm -f {} ';'

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} AUTHORS NEWS

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/augmatch
%{_bindir}/augparse
%{_bindir}/augprint
%{_bindir}/augtool
%{_bindir}/fadot
%{_datadir}/vim/vimfiles/syntax/augeas.vim
%{_datadir}/vim/vimfiles/ftdetect/augeas.vim
%{_datadir}/bash-completion/completions/augmatch
%{_datadir}/bash-completion/completions/augprint
%{_datadir}/bash-completion/completions/augtool

%files libs
%license COPYING
%{_datadir}/augeas
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/augeas.pc

%files doc
%{_mandir}/man1/*
%{_docdir}/%{name}-%{version}
