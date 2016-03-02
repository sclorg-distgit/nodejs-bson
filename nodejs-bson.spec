%{?scl:%scl_package nodejs-%{npm_name}}
%{!?scl:%global pkg_name %{name}}

%global npm_name bson
# Although there are tests
# the dependencies aren't in Fedora yet
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Summary:        A bson parser for node.js and the browser
Name:           %{?scl_prefix}nodejs-%{npm_name}
Version:        0.4.21
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://github.com/mongodb/js-bson
Source0:        http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz

%if 0%{?enable_tests}
## To get the tests (Source1), do the following
# git clone https://github.com/mongodb/js-bson.git
# cd js-bson/
# tar cfz nodejs-bson-test-0.4.21.tar.gz test/
Source1:        nodejs-bson-test-0.4.21.tar.gz
%endif

BuildRequires:  %{?scl_prefix}node-gyp
BuildRequires:  %{?scl_prefix}nodejs-devel
BuildRequires:  %{?scl_prefix}nodejs-nan

%if 0%{?enable_tests}
BuildRequires:  %{?scl_prefix}npm(gleak)
BuildRequires:  %{?scl_prefix}npm(nodeunit)
BuildRequires:  %{?scl_prefix}npm(one)
%endif

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch

%description
A JS/C++ Bson parser for node, used in the MongoDB Native driver.

%prep
%setup -q -n package

%build
#nothing to do

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr alternate_parsers tools lib deserializer_bak.js bower.json package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}

%nodejs_symlink_deps

%if 0%{?enable_tests}
%check
tar xfz %{SOURCE1}
nodeunit ./test/node && TEST_NATIVE=TRUE nodeunit ./test/node
%endif

%files
%doc README.md
%license LICENSE
%{nodejs_sitelib}/%{npm_name}

%changelog
* Mon Feb 29 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 0.4.21-2
- Add ExclusiveArch and BuildArch
- properly disable tests

* Wed Feb 17 2016 Tomas Hrcka <thrcka@redhat.com> - 0.4.21-1
- Rebase to latest upstream release
- This package is no longer native module

* Tue Mar 04 2014 Tomas Hrcka <thrcka@redhat.com> - 0.2.3-3.3
- Add missing nodejs_symlink_deps macro 

* Tue Jan 14 2014 Tomas Hrcka <thrcka@redhat.com> - 0.2.3-3.2
- Invoke provides requires macro

* Thu Jan 09 2014 Tomas Hrcka <thrcka@redhat.com> - 0.2.3-3.1
- enable scl support

* Tue Dec 03 2013 Troy Dawson <tdawson@redhat.com> - 0.2.3-3
- Fixed permission on bson.node

* Sat Nov 16 2013 Troy Dawson <tdawson@redhat.com> - 0.2.3-2
- Updated source

* Tue Oct 08 2013 Troy Dawson <tdawson@redhat.com> - 0.2.3-1
- Updated to 0.2.3
- Updated BuildRequires and added NODE_PATH
- Added testing, though set to false until packages are made.

* Tue Oct 08 2013 Troy Dawson <tdawson@redhat.com> - 0.2.2-1
- Updated to 0.2.2
- Updated spec file to Fedora guidelines

* Wed Apr 17 2013 Haibo Lin <hlin@redhat.com> - 0.1.8-1
- Initial build
