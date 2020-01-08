from __future__ import print_function
"""
X-ray HAL
TODO: move to own repo
"""

import pycurl
import os
import time
from gxs700 import util


class XRay:
    def __init__(self):
        pass

    def fil_on(self):
        pass

    def fil_off(self):
        pass

    def beam_on(self):
        pass

    def beam_off(self):
        pass


def wps7_switch(n, on, host=None, user=None, password=None):
    host = os.getenv('WPS7_HOST', None) if host is None else host
    assert host
    user = os.getenv('WPS7_USER', 'admin') if user is None else user
    password = os.getenv('WPS7_PASS', '') if password is None else password
    state = 'ON' if on else 'OFF'
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://%s/outlet?%d=%s' % (host, n, state))
    c.setopt(c.WRITEDATA, open('/dev/null', 'wb'))
    #c.setopt(c.WRITEDATA, None)
    c.setopt(pycurl.USERPWD, '%s:%s' % (user, password))
    c.perform()
    c.close()


"""
GE1000 head
IIRC roughly 10% duty cycle at max power is safe
15 mA @ 80 kV = 1200 W
10 mA @ 90 kV = 900 W
"""


class WPS7XRay:
    def __init__(self, verbose=False):
        # Assume not fired
        self.fire_last = 0
        self.warm_tstart = None
        self.sw_fil = 1
        self.sw_hv = 2
        self.warm_time = 5
        self.verbose = verbose

        # Default WPS7 creds
        self.host = "energon"
        self.user = None
        self.password = None

    def switch(self, n, on):
        wps7_switch(
            n, on, host=self.host, user=self.user, password=self.password)

    def fil_on(self):
        self.switch(self.sw_fil, 1)
        if self.warm_tstart is None:
            self.warm_tstart = time.time()

    def fil_off(self):
        self.switch(self.sw_fil, 0)
        self.warm = None

    def warm(self, t=None):
        t = self.warm_time if t is None else t
        self.fil_on()
        time.sleep(t)
        assert self.iswarm()

    def iswarm(self):
        return self.warm_tstart and time.time(
        ) - self.warm_tstart >= self.warm_time

    def beam_on(self):
        self.switch(self.sw_hv, 1)

    def beam_off(self):
        self.switch(self.sw_hv, 0)

    def fire(self, t):
        try:
            assert self.iswarm()

            self.verbose and print('Waiting for head to cool...')
            # FIXME: assumes 3 sec fire time
            while time.time() - self.fire_last < 30:
                time.sleep(0.1)
            self.verbose and print('Head ready')

            self.verbose and print('X-RAY: BEAM ON')
            self.beam_on()
            self.fire_last = time.time()
            time.sleep(t)
        finally:
            self.beam_off()
            self.verbose and print('X-RAY: BEAM OFF')

    def get_json(self):
        return {
            "wps7": True,
            "host": self.host,
        }

    def write_json(self, outdir):
        util.json_write(os.path.join(outdir, "source.json"), self.get_json())
