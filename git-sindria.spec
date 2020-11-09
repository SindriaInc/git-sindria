Name:       git-sindria
Version:    1
Release:    1
Summary:    Git extension client for gitlab
License:    GPLv2

%description
Git extension client for gitlab.

%prep
# we have no source, so nothing here

%build
make /home/sindria/Projects/Sindria/devops/tools/git-sindria

%install
mkdir -p %{buildroot}/usr/bin/
install -m 755 /home/sindria/Projects/Sindria/devops/tools/git-sindria/__pycache__/*.pyc %{buildroot}/usr/bin/git-sindria

%files
/usr/bin/git-sindria

%changelog
# let's skip this for now
