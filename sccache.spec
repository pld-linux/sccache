Summary:	sccache is ccache with cloud storage
Name:		sccache
Version:	0.2.13
Release:	0.1
License:	Apache v2.0
Group:		Development/Tools
Source0:	https://github.com/mozilla/sccache/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	acc81e9b1c7097d4119ad31cd6a845a9
#Source1:	vendor.tar.gz
URL:		https://github.com/mozilla/sccache
BuildRequires:	openssl-devel
BuildRequires:	rust-packaging
ExcludeArch:	s390 s390x ppc ppc64 ppc64le
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sccache is a ccache-like tool. It is used as a compiler wrapper and
avoids compilation when possible, storing a cache in a remote storage
using the Amazon Simple Cloud Storage Service (S3) API, Redis or the
Google Cloud Storage (GCS) API.

%prep
%setup -q

install -d .cargo
cat >.cargo/config <<EOF

[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'
[source.vendored-sources]
directory = './vendor'
[install]
root = '$RPM_BUILD_ROOT%{_prefix}'
[term]
verbose = true

EOF

%build
%cargo_build

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%cargo_install

find $RPM_BUILD_ROOT -name .crates2.json -delete
rm -rf $RPM_BUILD_ROOT%{_datadir}/cargo/registry

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/sccache
