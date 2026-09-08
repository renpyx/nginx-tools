#!/bin/bash

PKG_DIR="nxtool-build"
rm -rf $PKG_DIR
mkdir -p $PKG_DIR/DEBIAN
mkdir -p $PKG_DIR/usr/bin
mkdir -p $PKG_DIR/usr/lib/nxtool
mkdir -p $PKG_DIR/etc/bash_completion.d

cat <<EOF > $PKG_DIR/DEBIAN/control
Package: nxtool
Version: 0.1.0-Alpha-dev
Section: utils
Priority: optional
Architecture: all
Maintainer: Dein Name
Depends: python3, python3-argcomplete, nginx
Description: Nginx Site Management Wrapper
EOF

cp -r src/* $PKG_DIR/usr/lib/nxtool/

cat <<EOF > $PKG_DIR/usr/bin/nxtool
#!/bin/bash
export PYTHONPATH=\$PYTHONPATH:/usr/lib/nxtool
python3 /usr/lib/nxtool/app.py "\$@"
EOF

./venv/bin/register-python-argcomplete --no-defaults nxtool > $PKG_DIR/etc/bash_completion.d/nxtool

chmod 755 $PKG_DIR/usr/bin/nxtool
chmod -R 755 $PKG_DIR/DEBIAN
dpkg-deb --build $PKG_DIR nxtool_0.1.0-Alpha-dev_all.deb