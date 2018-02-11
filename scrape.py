from uvscada.util import str2hex

import re
import sys
import ast
import json
import binascii
import subprocess
import struct

prefix = ' ' * 8
indent = ''
resets = 0
reset_filters = [0]
RESET_FILTER = 2
def line(s):
    # Don't print until firmware loaded (2 stage)
    if resets < RESET_FILTER:
        reset_filters[0] += 1
        return
    #if s == '# None (0xB0)':
    #    raise Exception()
    print '%s%s' % (indent, s)
def indentP():
    global indent
    indent += '    '
def indentN():
    global indent
    indent = indent[4:]

def is_rst_release(p):
    #if resets > -1 and 'data' in p:
    #    print p, binascii.hexlify(p['data'])
    # controlWrite(0x40, 0xA0, 0xE600, 0x0000, "\x00")
    return p['type'] == 'controlWrite' and \
        p['reqt'] == 0x40 and p['req'] == 0xA0 and p['val'] == 0xE600 and p['ind'] == 0x00 and \
        p['data'] == '00'

def dump(fin):
    global resets

    j = json.load(open(fin))
    pi = 0
    ps = j['data']

    line('# Generated from scrape.py')
    
    def peekp():
        return nextp()[1]

    def nextp():
        ppi = pi + 1
        while True:
            if ppi >= len(ps):
                raise Exception("Out of packets")
            p = ps[ppi]
            if p['type'] != 'comment':
                return ppi, p
            ppi = ppi + 1
    
    line('def replay(dev):')
    indentP()

    def mk_i2c_w(addr, buff):
        return ('controlWrite', 0x40, 0xB0, 0x0A, addr, buff)
    
    def dec_wh_w(p):
        data = binascii.unhexlify(p['data'])
        w, h = struct.unpack('>HH', data)
        return 'gxs.img_wh_w(%d, %d)' % (w, h)

    def pyd(p):
        data = binascii.unhexlify(p['data'])
        return str2hex(data)

    def pdat(p):
        return binascii.unhexlify(p['data'])

    xlates = {
        ('controlWrite', 0x40, 0xB0, 0x2E, 0, '\x00'):  lambda p: 'gxs.hw_trig_arm()',
        ('controlWrite', 0x40, 0xB0, 0x2F, 0, None):    lambda p: 'gxs.hw_trig_disarm()',
        ('controlRead',  0xC0, 0xB0, 0x0B, None, None): lambda p: 'gxs.eeprom_r(...)',
        ('controlWrite', 0x40, 0xB0, 0x0C, None, None): lambda p: 'gxs.eeprom_w(...)',
        ('controlRead',  0xC0, 0xB0, 0x10, None, None): lambda p: 'gxs.flash_r(0x%04X, 0x%04X)' % (p['ind'], p['len']),
        ('controlWrite', 0x40, 0xB0, 0x11, None, None): lambda p: 'gxs.flash_erase(...)',
        ('controlWrite', 0x40, 0xB0, 0x0F, None, None): lambda p: 'gxs.flash_w(...)',
        ('controlRead',  0xC0, 0xB0, 0x03, None, None): lambda p: 'gxs.fpga_rv(0x%04x, %d)'  % (p['ind'], p['len'] / 2),
        ('controlRead',  0xC0, 0xB0, 0x04, 0, 2):       lambda p: 'gxs.fpga_rsig()',
        ('controlWrite', 0x40, 0xB0, 0x02, None, None): lambda p: 'gxs.fpga_wv2(0x%04X, %s)' % (p['ind'], pyd(p)),
        ('controlRead',  0xC0, 0xB0, 0x25, 0, 6):       lambda p: 'gxs.trig_param_r()',
        ('controlRead',  0xC0, 0xB0, 0x0A, None, None): lambda p: 'gxs.i2c_r()',
        ('controlWrite', 0x40, 0xB0, 0x0A, None, None): lambda p: 'gxs.i2c_w(...)',
        ('controlWrite', 0x40, 0xB0, 0xe600, None, None): lambda p: 'gxs.fx2_w(...)',
        (mk_i2c_w(0x82, '\x03\x00')): lambda p: 'gxs.fpga_off__1()',
        (mk_i2c_w(0x82, '\x01\x0E')): lambda p: 'gxs.fpga_off__2()',
        ('controlRead',  0xC0, 0xB0, 0x51, 0, 0x1C):    lambda p: 'gxs.versions()',
        ('controlRead',  0xC0, 0xB0, 0x40, 0, 8):       lambda p: 'gxs.img_ctr_r()',
        ('controlRead',  0xC0, 0xB0, 0x23, 0, 4):       lambda p: 'gxs.img_wh()',
        ('controlWrite', 0x40, 0xB0, 0x22, 0, None):    dec_wh_w,
        ('controlWrite', 0x40, 0xB0, 0x2C, 0, None):    lambda p: 'gxs.int_t_w(0x%04X)' % (struct.unpack('>H', pdat(p))[0]),
        ('controlRead',  0xC0, 0xB0, 0x2D, 0, 4):       lambda p: 'gxs.int_time()',
        ('controlWrite', 0x40, 0xB0, 0x41, 0, '\x00'):  lambda p: 'gxs.img_ctr_rst()',
        ('controlWrite', 0x40, 0xB0, 0x0E, None, ''):   lambda p: 'gxs.set_act_sec(%d)' % p['ind'],
        ('controlWrite', 0x40, 0xB0, 0x21, None, '\x00'): lambda p: 'gxs.cap_mode_w(...)',
        ('controlWrite', 0x40, 0xB0, 0x24, 0, None):    lambda p: 'gxs.trig_param_w(...)',
        ('controlWrite', 0x40, 0xB0, 0x2b, 0, '\x00'):  lambda p: 'gxs.sw_trig(...)',
        ('controlRead',  0xC0, 0xB0, 0x20, 0, 1):       lambda p: 'gxs.state()',
        ('controlRead',  0xC0, 0xB0, 0x80, 0, 1):       lambda p: 'gxs.error()',
        }

    def run_xlate(p):
        data = None
        if 'data' in p:
            data = binascii.unhexlify(p['data'])
        for xlate, xf in xlates.iteritems():
            xtype, xreqt, xreq, xval, xind, xdata = xlate
            #print 'xlate', xlate
            #print 'p', p
            if p['type'] != xtype:
                continue
            if xreqt is not None and p['reqt'] != xreqt:
                continue
            if xval is not None and p['val'] != xval:
                continue
            if xind is not None and p['ind'] != xind:
                continue
            if xtype == 'controlWrite':
                if xdata is not None and data != xdata:
                    continue
            line('# ' + xf(p))
            break

    while pi < len(ps):
        p = ps[pi]
        try:
            run_xlate(p)
    
            data = None
            if 'data' in p:
                data = binascii.unhexlify(p['data'])
    
            if p['type'] == 'comment':
                line('# %s' % p['v'])
                pass
            elif p['type'] == 'controlRead':
                line('buff = controlRead(0x%02X, 0x%02X, 0x%04X, 0x%04X, %d)' % (
                        p['reqt'], p['req'], p['val'], p['ind'], p['len']))
                line('# Req: %d, got: %d' % (p['len'], len(data)))
                line('validate_read(%s, buff, "packet %s/%s")' % (
                        str2hex(data, prefix=prefix), p['packn'][0], p['packn'][1]))
            elif p['type'] == 'controlWrite':
                line('buff = controlWrite(0x%02X, 0x%02X, 0x%04X, 0x%04X, %s)' % (
                        p['reqt'], p['req'], p['val'], p['ind'], str2hex(data, prefix=prefix)))
            elif p['type'] == 'bulkRead':
                pass
            elif p['type'] == 'bulkWrite':
                pass
            else:
                raise Exception("Unknown type: %s" % p['type'])
            if is_rst_release(p):
                resets += 1
                if resets == 2:
                    line('# Filtered %d FW load packets' % reset_filters[0])
            pi += 1
        except:
            print 'Error on packet %s' % (p['packn'],)
            raise

    indentN()

    print

if __name__ == "__main__":
    import argparse 
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--usbrply', default='usbrply')
    # Original capture was per USB port, making sense to count resets and assume all packets are for device
    # New set is full system, so instead filter by device ID
    # maybe they used a hub
    parser.add_argument('--device', type=int, default=None, help='Only keep packets for given device')
    parser.add_argument('fin')
    args = parser.parse_args()
    args.big_thresh = 256

    if args.fin.find('.cap') >= 0 or args.fin.find('.pcap') >= 0 or args.fin.find('.pcapng') >= 0:
        fin_j = '/tmp/scrape.json'
        #print 'Generating json'
        device_arg = ''
        if args.device:
            device_arg = '--device %s' % args.device
            # since we are throwing away firmware load, don't filter
            RESET_FILTER = 0
        cmd = '%s --packet-numbers --no-setup --comment --fx2 -j %s %s >%s' % (args.usbrply, device_arg, args.fin, fin_j)
        print cmd
        subprocess.check_call(cmd, shell=True)
    else:
        fin_j = args.fin
    
    dump(fin_j)
