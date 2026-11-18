# mobile_app_mock

fork of the Flutter StudyJam sample app `flutter_app` by Azhar Hussain (Jeddah, 29 March 2019), extended with a login screen as a mobile test target. his commits are kept in the git history.

## what it is

a tiny Flutter app that exists to be automated. it is the target of the mobile test repos, so nobody has to build or find an app to practice on. you do not need Flutter to use it: download a ready build from the release (below).

- package id on Android: `com.ted.ted_mobile_app_test` (launch activity `com.ted.ted_mobile_app_test.MainActivity`)
- bundle id on iOS: `net.ted.flutterApp`
- app name: `ted_mobile_app_test`, version `1.0.0+1`
- it is a **debug** build with the Flutter driver extension enabled (`enableFlutterDriverExtension()` in `lib/main.dart`), which is what lets Appium's Flutter driver find widgets by key.

### screens

home screen (title bar `Flutter Demo Home Page`):

- the text `You have pushed the button this many times:` and a counter, starting at `0`.
- a round `+` button (tooltip `Increment`) that adds 1.
- a `Login` button in the title bar (key `button_login`).

login screen (title `Login`): username field, password field, `Sign In` button, and an error text line.

after a successful login the app goes back to the home screen, and the title bar shows the user name (key `label_current_user`) and a `Logout` button (key `button_logout`). `Logout` brings back the `Login` button. the login is kept in memory only: closing the app logs out.

### login accounts (the ones tests use)

password for all: `secret_sauce`. the account names are the same as on https://www.saucedemo.com/.

| username | result |
| --- | --- |
| `standard_user`, `problem_user`, `performance_glitch_user`, `error_user`, `visual_user` | login succeeds, no behavioral difference in this app |
| `locked_out_user` | `Epic sadface: Sorry, this user has been locked out.` |
| empty username | `Epic sadface: Username is required` |
| empty password (username filled) | `Epic sadface: Password is required` |
| anything else, or a wrong password | `Epic sadface: Username and password do not match any user in this service` |

### widget keys (locators)

every interactive widget has a `Key` with a readable name, defined in `lib/main.dart`: `button_login`, `field_username`, `field_password`, `button_sign_in`, `text_login_error`, `label_current_user`, `button_logout`.

## when to use it

- as the app under test for Android or iOS automation practice with Appium or Katalon.
- to show how a Flutter app is automated (Flutter driver keys, or the accessibility tree).

when not to use it:

- you need a realistic app: this one has one counter and one login form.
- you want to practice web: use https://github.com/ClasherGeek77/saucedemo_clone.

repos that test it:

| repo | platform |
| --- | --- |
| https://github.com/ClasherGeek77/pytest_android_boilerplate | Android emulator, Appium + pytest |
| https://github.com/ClasherGeek77/pytest_ios_boilerplate | iOS simulator, Appium + pytest |
| https://github.com/ClasherGeek77/katalon_android_boilerplate | Android emulator, Katalon |
| https://github.com/ClasherGeek77/katalon_ios_boilerplate | iOS simulator, Katalon |

each of those has a `./fetch_app.sh` that downloads and verifies the files below for you into `apps/`. you only need this README to install the app by hand or to build it yourself.

## release assets

release: https://github.com/ClasherGeek77/mobile_app_mock/releases/tag/v1.0.0

| file | what | size |
| --- | --- | --- |
| `ted_mobile_app_test-v1.0.0-debug.apk` | Android app, package `com.ted.ted_mobile_app_test` | 61 MB |
| `a11y-enabler.apk` | Android accessibility service, package `net.ted.a11yenabler` (see below) | 9 KB |
| `ted_mobile_app_test-v1.0.0-ios-simulator.zip` | iOS simulator build, contains `Runner.app` (x86_64 simulator build), bundle `net.ted.flutterApp` | 25 MB |
| `SHA256SUMS.txt` | SHA-256 of the three files above | |

download and check (works on macOS and Linux; on Linux `shasum -a 256` may be missing, use `sha256sum -c SHA256SUMS.txt`):

```bash
mkdir -p apps && cd apps
B=https://github.com/ClasherGeek77/mobile_app_mock/releases/download/v1.0.0
curl -fLO $B/ted_mobile_app_test-v1.0.0-debug.apk
curl -fLO $B/a11y-enabler.apk
curl -fLO $B/ted_mobile_app_test-v1.0.0-ios-simulator.zip
curl -fLO $B/SHA256SUMS.txt
shasum -a 256 -c SHA256SUMS.txt
```

you should see:

```
a11y-enabler.apk: OK
ted_mobile_app_test-v1.0.0-debug.apk: OK
ted_mobile_app_test-v1.0.0-ios-simulator.zip: OK
```

if a line says `FAILED`, delete that file and download it again. the iOS zip is only needed for iOS: `unzip ted_mobile_app_test-v1.0.0-ios-simulator.zip` gives `Runner.app/`.

## install on an Android emulator

you need the Android SDK `platform-tools` (`adb`) and a running emulator or device. this README does not start one for you. the test repos use an Android 9 x86_64 emulator; other versions were not checked.

```bash
adb devices                      # your emulator must be listed as "device"
adb install apps/ted_mobile_app_test-v1.0.0-debug.apk
adb install apps/a11y-enabler.apk
adb shell am start -n com.ted.ted_mobile_app_test/com.ted.ted_mobile_app_test.MainActivity
```

each `adb install` should print `Success`, and the app opens on the home screen with the counter at `0`.

to switch the enabler on (see the next section), then restart the app:

```bash
adb shell settings put secure enabled_accessibility_services net.ted.a11yenabler/.Enabler
adb shell settings put secure accessibility_enabled 1
adb shell am force-stop com.ted.ted_mobile_app_test
adb shell am start -n com.ted.ted_mobile_app_test/com.ted.ted_mobile_app_test.MainActivity
```

uninstall: `adb uninstall com.ted.ted_mobile_app_test`.

## install on an iOS simulator

macOS only, with Xcode and a simulator that is already booted (the test repos use an iPhone SE 2nd generation, iOS 14.4, named `iPhoneSE14`). the build is a simulator build: it does not install on a real iPhone.

```bash
xcrun simctl list devices booted      # one device must be listed as Booted
xcrun simctl install booted apps/Runner.app
xcrun simctl launch booted net.ted.flutterApp
```

`launch` prints the bundle id and a process id, and the app opens on the home screen. uninstall: `xcrun simctl uninstall booted net.ted.flutterApp`.

## the a11y-enabler (Android only)

what: a tiny Android accessibility service (`net.ted.a11yenabler/.Enabler`) that does nothing: no event is read, stored or forwarded.

why: Flutter draws the whole app in one canvas. as long as no accessibility service is running, Android sees one opaque view, and UiAutomator2 (the Appium Android engine) gets an empty element tree, so tests cannot find the buttons by text or content description. with any accessibility service enabled, Flutter publishes its widget tree as normal Android nodes. the enabler is that service. the app has to be (re)started after the service is on, because Flutter only connects to services that are running when it starts.

you need it for tests that use UiAutomator2 locators. you do not need it if you drive the app only through the Flutter driver (widget keys).

source and rebuild: `tools/a11y-enabler/` has a `build.sh`.

```bash
cd tools/a11y-enabler
./build.sh
```

you should see `BUILT a11y-enabler.apk`, and `tools/a11y-enabler/a11y-enabler.apk` is replaced. the script needs:

- Android SDK with `build-tools/28.0.3` and `platforms/android-28` (`ANDROID_HOME`, default `~/Library/Android/sdk`)
- a JDK 8 (`JAVA_HOME_8`; the built-in default is a path that exists on one particular Mac, so set the variable)
- no Gradle: it runs `javac`, `d8`, `aapt2`, `zip` and `apksigner`.

it signs with the committed `debug.keystore` (a throwaway debug key, password `android`). a rebuilt APK is not guaranteed to be byte-identical to the release one, so its checksum may differ from `SHA256SUMS.txt`. not re-run for this README; the committed `a11y-enabler.apk` matches the release checksum.

## build from source (optional)

only needed if you change the app. the ready builds above are enough for testing.

versions: the project is old. `.metadata` pins the Flutter revision `8661d8aecd626f7f57ccbcb735553edc05a2e713` (stable channel), and the release builds were made with **Flutter 1.22.6** (`pubspec.yaml` requires `sdk: ">=2.1.0 <3.0.0"`, the Dart 2 line). a current Flutter will not build it without porting the code (for example `FlatButton`, `display1` and `Key key` are removed or changed). get that Flutter from the archive at https://docs.flutter.dev/release/archive (look for 1.22.6, stable).

```bash
git clone https://github.com/ClasherGeek77/mobile_app_mock.git
cd mobile_app_mock
flutter --version                       # should say Flutter 1.22.6
flutter pub get
flutter build apk --debug               # Android
flutter build ios --debug --simulator   # iOS simulator, macOS with Xcode only
```

outputs: `build/app/outputs/flutter-apk/app-debug.apk` (its checksum equals the release APK) and `build/ios/iphonesimulator/Runner.app` (the path `test_appium/` expects). the exact `--simulator` flag was not re-run for this README.

Android side: Gradle 4.10.2 and Android Gradle plugin 3.2.1 (from `android/`), `compileSdkVersion 28`, `minSdkVersion 16`, so install Android SDK platform 28 and use a JDK 8. iOS side: the simulator build was made on macOS with Xcode 12.4 and is x86_64; other Xcode versions and Apple Silicon were not checked.

`test/widget_test.dart` is the unchanged Flutter template test (a counter smoke test); the app has since gained a login page, so treat it as a placeholder.

## how to read the code

- `lib/main.dart`: the whole app (home page with counter and login button, `LoginPage`, the account list `kSauceUsers` and password `kSaucePassword`).
- `android/`, `ios/`: the generated platform projects (package id and bundle id live here).
- `tools/a11y-enabler/`: the enabler service (`src/`, `AndroidManifest.xml`, `res/xml/accessibility_config.xml`, `build.sh`).
- `test_appium/test_login_states.py`: the first single-file Appium script for the login states (7 steps). kept as a reference; it assumes a local Appium server on port 4723 and reads the iOS app path from `IOS_APP` (default `build/ios/iphonesimulator/Runner.app`), so for real use take the pytest repos above.
- `BACKLOG-iOS.md`: working notes of the iOS port, not documentation.

## if it breaks

| symptom | cause | fix |
| --- | --- | --- |
| `adb: no devices/emulators found` | no emulator running | start your emulator, wait until `adb devices` shows `device` |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | an older build with another signature is installed | `adb uninstall com.ted.ted_mobile_app_test`, install again |
| `INSTALL_FAILED_NO_MATCHING_ABIS` | the emulator image does not match the app's CPU types | use an x86_64 image (the test repos use Android 9 x86_64) |
| app opens but UiAutomator2 sees no elements | enabler not installed or not enabled, or app not restarted | install and enable it, force-stop and start the app (see above) |
| `shasum` prints `FAILED` | incomplete download | delete the file, download again |
| `xcrun simctl install` fails with an "invalid device state" style error | no simulator is booted | boot one, then check with `xcrun simctl list devices booted` |
| the iOS app does not install on a real iPhone | the iOS zip is a simulator build | use a simulator |
| `flutter build` fails with Dart errors | Flutter is too new | use Flutter 1.22.6 |

## next

- Appium + pytest, Android: https://github.com/ClasherGeek77/pytest_android_boilerplate
- Appium + pytest, iOS: https://github.com/ClasherGeek77/pytest_ios_boilerplate
- Katalon, Android: https://github.com/ClasherGeek77/katalon_android_boilerplate
- Katalon, iOS: https://github.com/ClasherGeek77/katalon_ios_boilerplate
