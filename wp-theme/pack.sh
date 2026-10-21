#!/bin/sh
#
# Assemble the theme and zip it for upload to WordPress.
#
# Run from wp-theme/. Everything this script copies or generates is kept out of
# git: the pictures, the brochure and the shared stylesheet already live in the
# repository once, under assets/, and a second copy inside the theme would only
# drift. Clone the repository, run this, and the zip is whole again.
#
#   ./pack.sh            -> ndop.zip, ready for Appearance -> Themes -> Upload

set -e
cd "$(dirname "$0")"

OUT="${1:-ndop.zip}"

# 1. The words and the pictures, as block markup plus the generated PHP.
python3 build.py

# 2. What the theme shares with the static build, copied in verbatim.
mkdir -p ndop/assets/css ndop/assets/js ndop/assets/img ndop/assets/docs ndop/pages
cp ../assets/css/style.css ndop/assets/css/style.css
cp ../assets/js/main.js    ndop/assets/js/main.js
cp ../assets/img/*.jpg ../assets/img/*.png ../assets/img/*.svg ndop/assets/img/
cp ../assets/docs/*.pdf ndop/assets/docs/
cp pages/*.html ndop/pages/

# 3. The zip. A theme folder at the top level is what WordPress expects.
rm -f "$OUT"
zip -rq "$OUT" ndop -x '*.DS_Store'

echo
echo "  $OUT  —  $(du -h "$OUT" | cut -f1)"
echo "  style.css $(md5 -q ndop/assets/css/style.css | cut -c1-8)   wp.css $(md5 -q ndop/assets/css/wp.css | cut -c1-8)"
echo "  $(find ndop -type f | wc -l | tr -d ' ') files"
