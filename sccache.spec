Summary:	sccache is ccache with cloud storage
Name:		sccache
Version:	0.2.15
Release:	0.1
License:	Apache v2.0
Group:		Development/Tools
Source0:	https://github.com/mozilla/sccache/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	dcb0cf6686c334df82f0a2b41eae19ab
# cd sccache-%{version}
# cargo vendor
# cd ..
# tar -cJf sccache-crates-%{version}.tar.xz sccache-%{version}/{vendor,Cargo.lock}
# ./dropin sccache-crates-%{version}.tar.xz
Source1:	%{name}-crates-%{version}.tar.xz
# Source1-md5:	cac0034c691ba28b575bb955fce1159d
Patch0:		openssl.patch
URL:		https://github.com/mozilla/sccache
BuildRequires:	openssl-devel
BuildRequires:	rust >= 1.43.0
BuildRequires:	cargo
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExcludeArch:	s390 s390x ppc ppc64 ppc64le
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# TODO: this should not be needed
%define		_debugsource_packages	0

%description
Sccache is a ccache-like tool. It is used as a compiler wrapper and
avoids compilation when possible, storing a cache in a remote storage
using the Amazon Simple Cloud Storage Service (S3) API, Redis or the
Google Cloud Storage (GCS) API.

%prep
%setup -q -b1
%patch0 -p1

install -d .cargo
cat >.cargo/config <<'EOF'

[source.crates-io]
replace-with = "vendored-sources"

[source."https://github.com/saresend/selenium-rs.git"]
git = "https://github.com/saresend/selenium-rs.git"
rev = "0314a2420da78cce7454a980d862995750771722"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

cargo -v build \
%ifarch x32
	--target x86_64-unknown-linux-gnux32 \
%endif
	--release \
	--offline

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

cargo -vv \
	install \
	--frozen \
	--path . \
	--root $RPM_BUILD_ROOT%{_prefix}

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates.toml
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates2.json

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/sccache
