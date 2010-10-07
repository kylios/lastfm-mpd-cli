# Maintainer: morendi <kracette at gmail dot com>

pkgname=lastfm-mpd-cli
pkgver=0.01
pkgrel=1
pkgdesc="A simple command-line utility for interfacing with MPD and Last.fm"
arch=(any)
url="http://morendi.github.com/lastfm-mpd-cli/"
license=('GPL')
depends=('python' 'pylast' 'mpc' 'baker')
source=(http://morendi.github.com/lastfm-mpd-cli/$pkgname-$pkgver.tar.gz)
md5sums=('d7aa1186dbf5ca83bdbcc13df50cfa5d')

build() {
    cd $srcdir/
    mkdir -p usr/bin/
    mv $pkgname.py usr/bin/$pkgname
    cp -R usr $pkgdir/
}


