# Maintainer: morendi <kracette at gmail dot com>

pkgname=lastfm-mpd-cli
pkgver=0.02
pkgrel=1
pkgdesc="A simple command-line utility for interfacing with MPD and Last.fm"
arch=(any)
url="http://morendi.github.com/lastfm-mpd-cli/"
license=('GPL')
depends=('python' 'pylast' 'mpc' 'baker')
source=(http://morendi.github.com/lastfm-mpd-cli/$pkgname-$pkgver.tar.gz)
md5sums=('275349b33195e053f4bc63fc3ac187e2')

build() {
    cd $srcdir/
    mkdir -p usr/bin/
    mkdir -p etc/
    mv $pkgname.py usr/bin/$pkgname
    mv $pkgname.rc etc/$pkgname.rc
    cp -R usr $pkgdir/
    cp -R etc $pkgdir/
}


