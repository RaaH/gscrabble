# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:      GoldenScrabble
License:   Waqf
Group:     System Environment/Base
Version:   0.1.0
Release:   1
Summary:   crossword puzzle game.
URL:       http://sourceforge.net/projects/gscrabble/
#https://github.com/RaaH/arabic_scrabble
Source0:   http://garr.dl.sourceforge.net/project/gscrabble/%{name}-%{version}.tar.xz
BuildRequires:  gstreamer-devel pygobject3-devel python3-devel ImageMagick
Requires:  gstreamer pygobject3 python3
BuildRoot: %{_tmppath}/%{name}-%{version}-build  
BuildArch: noarch

%description  
لعبة كلمات متقاطعة مسلية ومفيدة.
crossword puzzle game is funny and useful.

%prep
%setup -q

%build
rm -rf %{buildroot}

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

%clean
rm -rf %{buildroot}  

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Sat Apr 06 2013 Ahmed Raghdi <asmaaarab@gmail.com> - 0.1.0-1
- Initial release
