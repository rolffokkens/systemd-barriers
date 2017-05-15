%global gitcommit 8b2febb

%if 0%{?fedora} || 0%{?rhel} >= 7
%global units       aiccu cron postfix sssd keepalived httpd xinetd sshd haproxy openvpn@
%global start_units aiccu cron postfix sssd keepalived httpd xinetd sshd haproxy
%endif

Summary: Systemd barriers that force proper strict ordering for some services
Name: systemd-barriers
Version: 0.0
Release: 0.10.%{gitcommit}_git%{?dist}
Group: Applications/System
# git clone https://github.com/rolffokkens/systemd-barriers.git
# cd systemd-barriers
# COMMIT=133bd376; git archive --format=tar --prefix=systemd-barriers-$COMMIT/ $COMMIT | gzip > ../systemd-barriers-$COMMIT.tar.gz
Source0: systemd-barriers-%{gitcommit}.tar.gz
License: GPL
BuildArch: noarch
%if 0%{?units:1} 
%{?systemd_requires: %systemd_requires}
Buildrequires: systemd
Requires: systemd
%endif
Conflicts: th-tools < 1:0.2-23

%description
Systemd barriers that force proper ordering for services that otherwise may start in the wrong order. This should be a temporary solution, because this should eventually be fixed in the service packages themselves.

%prep
%setup -q -n systemd-barriers-%{gitcommit}

%build

%install
%if 0%{?units:1} 
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_presetdir}
for i in %{units}
do
    cp $i.target %{buildroot}%{_unitdir}/sb-$i.target
done
%endif

%post
%if 0%{?start_units:1} 
for i in %{start_units}
do
    # Initial installation
    /bin/systemctl --no-reload enable sb-$i.target >/dev/null 2>&1 || :
done
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

%preun
%if 0%{?start_units:1} 
for i in %{start_units}
do
    %systemd_preun sb-$i.target
done
%endif

%postun
%if 0%{?units:1} 
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

%files
%if 0%{?units:1} 
%attr(0644,root,root) %{_unitdir}/sb-*.target
%endif

%changelog
* Mon Jan 05 2015 Rolf Fokkens <rolf@rolffokkens.nl> 0.0-0
- built package

