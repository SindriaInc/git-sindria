Name:       git-sindria
Version:    1.0.0
Release:    1
Summary:    Git extension client for gitlab
License:    GPLv2

%description
Git extension client for gitlab.

%prep
# we have no source, so nothing here

%build
git clone https://github.com/SindriaInc/git-sindria.git
cd git-sindria
rm -Rf .git
make

%install
mkdir -p %{buildroot}/usr/local/bin
mkdir -p %{buildroot}/opt/
mkdir -p %{buildroot}/opt/git-sindria
install -m 755 git-sindria/__pycache__/*.pyc %{buildroot}/opt/git-sindria/git-sindria.pyc
install -m 755 git-sindria/git-sindria.sh %{buildroot}/opt/git-sindria/git-sindria.sh
install -m 755 git-sindria/git-sindria.sh %{buildroot}/usr/local/bin/git-sindria
#ln -s /opt/git-sindria/git-sindria.sh /usr/local/bin/git-sindria

%files
/opt/git-sindria/git-sindria.pyc
/opt/git-sindria/git-sindria.sh
/usr/local/bin/git-sindria

%changelog
# let's skip this for now
