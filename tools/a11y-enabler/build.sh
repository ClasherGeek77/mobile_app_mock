#!/bin/bash
# builds a11y-enabler.apk, stdlib SDK tools only, no gradle:
# javac -> d8 -> aapt2 link -> zip dex -> apksigner (debug key, regenerated)
set -e
cd "$(dirname "$0")"

SDK="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
BT="$SDK/build-tools/28.0.3"
PLATFORM="$SDK/platforms/android-28/android.jar"
JAVA="${JAVA_HOME_8:-$HOME/Library/Java/jdk8u512-b09/Contents/Home}/bin"

rm -rf build && mkdir -p build/classes build/tmp

"$JAVA/javac" -source 1.8 -target 1.8 -bootclasspath "$PLATFORM" \
    -d build/classes src/net/ted/a11yenabler/Enabler.java 2>/dev/null

"$BT/d8" --output build/tmp build/classes/net/ted/a11yenabler/Enabler.class

"$BT/aapt2" compile --dir res -o build/res.zip
"$BT/aapt2" link -o build/base.apk -I "$PLATFORM" --manifest AndroidManifest.xml build/res.zip

(cd build/tmp && zip -q ../base.apk classes.dex)

# the keystore lives OUTSIDE build/, so rebuilds keep one signature
KEY=debug.keystore
[ -f "$KEY" ] || "$JAVA/keytool" -genkeypair -keystore "$KEY" -alias d \
    -storepass android -keypass android -dname "CN=debug" \
    -keyalg RSA -keysize 2048 -validity 10000 >/dev/null 2>&1

"$BT/apksigner" sign --ks "$KEY" --ks-pass pass:android --key-pass pass:android \
    --out a11y-enabler.apk build/base.apk
echo "BUILT a11y-enabler.apk"
