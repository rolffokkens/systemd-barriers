%global gitcommit 133bd376

Summary: Systemd barriers that force proper strict ordering for some services
Name: systemd-barriers
Version: 0.0
Release: 0.0.%{gitcommit}_git%{?dist}
Group: Applications/System
# COMMIT=133bd376; git archive --format=tar --prefix=systemd-barriers-$COMMIT/ $COMMIT | gzip > ../systemd-barriers-$COMMIT.tar.gz
Source0: systemd-barriers-%{gitcommit}.tar.gz
License: GPL
Buildrequires: systemd-devel
BuildArch: noarch
Requires: systemd

%description
Systemd barriers that force proper ordering for services that otherwise may start in the wrong order. This should be a temporary solution, because this should eventually be fixed in the service packages themselves.

%prep
%setup -q -n systemd-barriers-%{gitcommit}

%build

%install
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_presetdir}
for i in *.target
do
    cp $i %{buildroot}%{_unitdir}/sb-$i
done
echo "enable sb-*.target" > %{buildroot}%{_presetdir}/95-systemd-barriers.presets

%files
%attr(0644,root,root) %{_unitdir}/sb-*.target
%attr(0644,root,root) %{_presetdir}/95-systemd-barriers.presets

%post
for i in %{_unitdir}/sb-*.target
do
    %systemd_post `basename $i`
done

%preun
for i in %{_unitdir}/sb-*.target
do
    %systemd_preun `basename $i` 
done

%postun
for i in %{_unitdir}/sb-*.target
do
    %systemd_postun `basename $i`
done

%changelog
* Mon Jan 05 2015 Rolf Fokkens <rolf@rolffokkens.nl> 0.0-0
- built package

