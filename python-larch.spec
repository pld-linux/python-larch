#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	larch
Summary:	Python B-tree library
Name:		python-%{module}
Version:	1.20130808
Release:	2
License:	GPL v3+
Group:		Libraries/Python
Source0:	http://code.liw.fi/debian/pool/main/p/python-%{module}/%{name}_%{version}.orig.tar.gz
# Source0-md5:	9132c891a508d836c39d2ac3a6b7c2f6
URL:		http://liw.fi/larch/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
# build-time only
BuildRequires:	cmdtest
BuildRequires:	python-Sphinx
BuildRequires:	python-coverage-test-runner
# build- and run-time
BuildRequires:	python-cliapp
BuildRequires:	python-tracing
BuildRequires:	python-ttystatus
Requires:	python-cliapp
Requires:	python-tracing
Requires:	python-ttystatus
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an implementation of particular kind of B-tree, based on
research by Ohad Rodeh. See "B-trees, Shadowing, and Clones" (copied
here with permission of author) for details on the data structure.
This is the same data structure that btrfs uses. Note that my
implementation is independent from the btrfs one, and might differ
from what the paper describes.

The distinctive feature of this B-tree is that a node is never
modified (sort-of). Instead, all updates are done by copy-on-write.
Among other things, this makes it easy to clone a tree, and modify
only the clone, while other processes access the original tree. This
is utterly wonderful for my backup application, and that's the reason
I wrote larch in the first place.

I have tried to keep the implementation generic and flexible, so that
you may use it in a variety of situations. For example, the tree
itself does not decide where its nodes are stored: you provide a class
that does that for it. I have two implementations of the NodeStore
class, one for in-memory and one for on-disk storage.

The tree attempts to guarantee this: all modifications you make will
be safely stored in the node store when the larch.Forest.commit method
is called. After that, unless you actually modify the committed tree
yourself, it will be safe from further modifications. (You need to
take care to create a new tree for further modifications, though.)

%package doc
Summary:	Documentation for %{module}
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains the documentation for %{module}, a Python
framework for Unix command line programs.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with tests}
# CoverageTestRunner trips up on build directory;
# remove it first
rm -rf build
%{__make} check
%endif

%py_build

# Build documentation
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%py_install

# drop internal tests
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/larch/*_tests.py*

%py_postclean

# manpage not installed automatically yet
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p fsck-larch.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/fsck-larch
%{_mandir}/man1/fsck-larch.1*
%{py_sitescriptdir}/larch-%{version}-py*.egg-info
%dir %{py_sitescriptdir}/larch
%{py_sitescriptdir}/larch/*.py[co]

%files doc
%defattr(644,root,root,755)
%doc doc/_build/html/*
