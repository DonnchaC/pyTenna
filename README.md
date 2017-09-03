Reversing the goTenna protocol
==============================

The goTenna is a nice device which allows peer-to-peer communication over radio, and without needing any other communications infrastructue. Currently the only interface to the device is via a mobile application for Android and iOS.

The lack of an open protocol specification and implemenation make it difficult to repurpuse the goTenna for other use-cases such as machine-to-machine communication

In this repository I'll record my goTenna research and will hopefully end up with a working implementation in Python.

The `scripts/` directory contains some tools for working with goTenna firmware images and the data files created by the Android application.


TODO
----

- [ ] Create a working protocol implementation in Python
- [ ] Create a Wireshark plugin for decoding the OTA data protocol.
- [ ] Investigate the Mesh protcol (does it do store and forward?).
