package net.ted.a11yenabler;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;

// the whole job: exist, so the system has one enabled accessibility
// service, which makes engines like flutter build and bridge their
// semantics tree; nothing is read, stored or forwarded
public class Enabler extends AccessibilityService {
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
    }

    @Override
    public void onInterrupt() {
    }
}
