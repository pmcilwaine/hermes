Name:           hermes_ui
Version:        0.5.0
Release:        {IMAGE_VERSION}
Source0:        %{name}-%{version}-%{release}.tar.gz
Group:          Development/Libraries
BuildArch:      noarch
Url:            https://github.com/pmcilwaine/hermes
Summary:        Hermes UI
License:        BSD

%description
Hermes UI

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/%_var/www/%name
cp -R admin %{buildroot}/%_var/www/%name/
cp -R public %{buildroot}/%_var/www/%name/

%clean
rm -rf $RPM_BUILD_ROOT

%files
/%_var/www/%name