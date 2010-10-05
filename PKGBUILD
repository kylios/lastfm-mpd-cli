# Maintainer: morendi <kracette at gmail dot com>

pkgname=lastfm-mpd-cli
pkgver=0.01
pkgrel=1
pkgdesc="A simple command-line utility for interfacing with MPD and Last.fm"
arch=('any')
url="http://github.com/morendi/mpdlastctl"
license=('GPL')
depends=('python>=2.6' 'pylast>=0.4' 'mpc>=0.19-1')
makedepends=('easy_install>=2.6')
install=
source=("github somethnig')
md5sums=()

build() {
    cd $srcdir/$pkgname-$pkgver
    make
}

package() {
    cd $srcdir/$pkgname-$pkgver
    make DESTDIR=$pkgdir install
}

