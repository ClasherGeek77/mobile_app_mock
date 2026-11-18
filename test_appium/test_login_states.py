#!/usr/bin/env python3
"""Appium login-state suite for ted_mobile_app_test — human-readable locators.

The locator contract (locator_id=<value>): every Flutter widget's ValueKey IS
the locator. locator_id('button_login') serializes to the ByValueKey finder
appium-flutter-driver speaks:

    loc = locator_id('button_login')
    f.tap('button_login')                              # flutter: clickElement
    f.wait_text('Epic sadface: Username is required')  # flutter: waitFor ByText

Keys in the app: button_login, field_username, field_password, button_sign_in,
text_login_error, label_current_user, button_logout.

Why execute_script and not find_element: appium-flutter-driver implements
Flutter ops only as `flutter: clickElement/waitFor/enterText/...` script
commands — there is no W3C find over the Dart VM protocol.

Stack: appium 3.9 + appium-flutter-driver@3.2 + Flutter 1.22.6 debug APK
(enableFlutterDriverExtension) on the Android 9 AVD (HVF, 1.5 GB).
"""
import base64
import json
import sys

from appium import webdriver
from appium.options.common import AppiumOptions

import os
SERVER = 'http://127.0.0.1:4723'
PKG = 'com.ted.ted_mobile_app_test'
ACT = 'com.ted.ted_mobile_app_test.MainActivity'
PLATFORM = os.environ.get('TARGET_PLATFORM', 'android')   # android | ios
IOS_APP = os.path.abspath(os.environ.get('IOS_APP', 'build/ios/iphonesimulator/Runner.app'))


def _b64(finder):
    return base64.b64encode(json.dumps(finder).encode()).decode()


def locator_id(value):
    """locator_id=<value> — the app's Key('<value>'), as a driver finder."""
    return _b64({'finderType': 'ByValueKey', 'keyValueString': value, 'keyValueType': 'String'})


def by_text(text):
    return _b64({'finderType': 'ByText', 'text': text})


class Flutter:
    def __init__(self, driver):
        self.d = driver

    def tap(self, key):
        self.d.execute_script('flutter: clickElement', locator_id(key), {})  # 3rd arg opts object REQUIRED by flutter-driver 2.1 (destructures it)

    def type(self, text):
        self.d.execute_script('flutter: enterText', text)

    def wait_key(self, key, ms=25000):
        self.d.execute_script('flutter: waitFor', locator_id(key), ms)

    def wait_text(self, text, ms=25000):
        self.d.execute_script('flutter: waitFor', by_text(text), ms)


def main():
    opts = AppiumOptions()
    if PLATFORM == 'ios':
        opts.load_capabilities({
            'platformName': 'iOS',
            'appium:automationName': 'Flutter',
            'appium:app': IOS_APP,
            'appium:simulatorOnly': True,
            'appium:udid': open('/tmp/simid').read().strip(),
            'appium:deviceName': 'iPhoneSE14',
            'appium:platformVersion': '14.4',
            'appium:newCommandTimeout': 180,
        })
    else:
        opts.load_capabilities({
            'platformName': 'Android',
            'appium:automationName': 'Flutter',
            'appium:appPackage': PKG,
            'appium:appActivity': ACT,
            'appium:newCommandTimeout': 180,
            'appium:forceAppLaunch': True,
        })
    d = webdriver.Remote(SERVER, options=opts)
    f = Flutter(d)
    results = []

    def step(name, fn):
        try:
            fn()
            results.append('PASS ' + name)
            print('PASS', name)
        except Exception as e:  # noqa: BLE001
            txt = ' '.join(str(e).splitlines()[:2])[:180]
            results.append('FAIL ' + name)
            print('FAIL', name, '->', txt)

    f.wait_key('button_login')
    step('login page reachable (locator_id=button_login)', lambda: f.tap('button_login'))
    step('empty username -> required', lambda: (f.tap('button_sign_in'),
         f.wait_text('Epic sadface: Username is required')))
    step('empty password -> required', lambda: (f.tap('field_username'), f.type('standard_user'),
         f.tap('button_sign_in'), f.wait_text('Epic sadface: Password is required')))
    step('mismatch', lambda: (f.tap('field_password'), f.type('wrong_pw'), f.tap('button_sign_in'),
         f.wait_text('Epic sadface: Username and password do not match any user in this service')))
    step('locked out', lambda: (f.tap('field_username'), f.type('locked_out_user'),
         f.tap('field_password'), f.type('secret_sauce'), f.tap('button_sign_in'),
         f.wait_text('Epic sadface: Sorry, this user has been locked out.')))
    step('standard_user success -> session label', lambda: (f.tap('field_username'),
         f.type('standard_user'), f.tap('field_password'), f.type('secret_sauce'),
         f.tap('button_sign_in'), f.wait_key('label_current_user'), f.wait_text('standard_user')))
    step('logout -> logged-out state', lambda: (f.tap('button_logout'), f.wait_key('button_login')))

    d.quit()
    n = sum(1 for r in results if r.startswith('PASS'))
    print('--- %d/%d passed ---' % (n, len(results)))
    return 0 if n == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
