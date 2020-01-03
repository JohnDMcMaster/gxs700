# original  capture verified against remote capture
def setup_fpga1_sm(self):
    self.fpga_wv2(0x0400, "\x00\x00\x60\x00\x00\x00")
    self.fpga_wv2(0x0404, "\x00\xE5\xC0\x00\x00\x00")
    self.fpga_wv2(0x0408, "\x00\xF7\x20\x00\x00\x01")
    self.fpga_wv2(0x040C, "\x00\xE5\x80\x00\x00\x01")
    self.fpga_wv2(0x0410, "\x00\xF7\xE0\x00\x00\x01")
    self.fpga_wv2(0x0414, "\x00\xE5\xA0\x00\x00\x02")
    self.fpga_wv2(0x0418, "\x00\xC5\x20\x00\x00\x04")
    self.fpga_wv2(0x041C, "\x00\x05\x38\x00\x00\x04")
    self.fpga_wv2(0x0420, "\x00\x04\x98\x00\x00\x04")
    self.fpga_wv2(0x0424, "\x00\x00\xF8\x02\x00\x0C")
    self.fpga_wv2(0x0428, "\x08\x00\x3F\x00\x00\x00")
    self.fpga_wv2(0x042C, "\x08\x00\x42\x04\x00\x00")
    self.fpga_wv2(0x0430, "\x08\x04\x4B\x04\x00\x00")
    self.fpga_wv2(0x0434, "\x08\x06\x54\x04\x00\x00")
    self.fpga_wv2(0x0438, "\x08\x04\x5D\x04\x00\x00")
    self.fpga_wv2(0x043C, "\x08\x06\x66\x04\x00\x00")
    self.fpga_wv2(0x0440, "\x08\x04\x6F\x04\x00\x00")
    self.fpga_wv2(0x0444, "\x08\x00\x72\x04\x00\x00")
    self.fpga_wv2(0x0448, "\x08\x01\x78\x04\x00\x00")
    self.fpga_wv2(0x044C, "\x08\x03\x7E\x04\x00\x00")
    self.fpga_wv2(0x0450, "\x08\x01\x84\x04\x00\x00")
    self.fpga_wv2(0x0454, "\x08\xC3\x8A\x04\x00\x00")
    self.fpga_wv2(0x0458, "\x08\xC1\x90\x04\x00\x00")
    self.fpga_wv2(0x045C, "\x08\xC0\x96\x04\x00\x00")
    self.fpga_wv2(0x0460, "\x08\xC2\x9C\x04\x00\x00")
    self.fpga_wv2(0x0464, "\x08\xC0\xA2\x04\x00\x08")
    self.fpga_wv2(0x0468, "\x08\x42\x06\x04\x00\x00")
    self.fpga_wv2(0x046C, "\x08\x00\x0C\x04\x00\x00")
    self.fpga_wv2(0x0470, "\x08\x82\x12\x04\x00\x00")
    self.fpga_wv2(0x0474, "\x08\x00\x18\x04\x00\x08")
    self.fpga_wv2(0x0478, "\x0F\x42\x18\x04\x00\x00")
    self.fpga_wv2(0x047C, "\x0F\x02\x22\x04\x00\x00")
    self.fpga_wv2(0x0480, "\x0E\x02\x6A\x04\x00\x00")
    self.fpga_wv2(0x0484, "\x0A\x02\x6F\x04\x00\x00")
    self.fpga_wv2(0x0488, "\x0A\x82\x87\x04\x00\x00")
    self.fpga_wv2(0x048C, "\x0A\x02\xFF\x04\x00\x00")
    self.fpga_wv2(0x0490, "\x08\x02\x04\x04\x00\x09")
    self.fpga_wv2(0x0494, "\x08\x20\x09\x04\x00\x00")
    self.fpga_wv2(0x0498, "\x08\x30\x12\x04\x00\x00")
    self.fpga_wv2(0x049C, "\x08\x20\x1B\x04\x00\x00")
    self.fpga_wv2(0x04A0, "\x08\x30\x24\x04\x00\x00")
    self.fpga_wv2(0x04A4, "\x08\x20\x2D\x04\x00\x00")
    self.fpga_wv2(0x04A8, "\x08\x00\x36\x04\x00\x00")
    self.fpga_wv2(0x04AC, "\x08\x0A\x3F\x04\x00\x00")
    self.fpga_wv2(0x04B0, "\x08\x1A\x48\x04\x00\x00")
    self.fpga_wv2(0x04B4, "\x08\x0A\x51\x04\x00\x00")
    self.fpga_wv2(0x04B8, "\x08\x1A\x5A\x04\x00\x00")
    self.fpga_wv2(0x04BC, "\x08\x0A\x63\x04\x00\x00")
    self.fpga_wv2(0x04C0, "\x08\x00\x64\x04\x00\x00")
    self.fpga_wv2(0x04C4, "\x08\x10\x6C\x04\x00\x08")
    self.fpga_wv2(0x04C8, "\x08\x10\x04\x0C\x00\x00")
    self.fpga_wv2(0x04CC, "\x08\x00\x08\x0C\x00\x00")
    self.fpga_wv2(0x04D0, "\x08\x10\x0C\x0C\x00\x00")
    self.fpga_wv2(0x04D4, "\x08\x00\x10\x0C\x00\x08")
    self.fpga_wv2(0x04D8, "\x08\x10\x09\x1C\x00\x00")
    self.fpga_wv2(0x04DC, "\x08\x00\x12\x1C\x00\x00")
    self.fpga_wv2(0x04E0, "\x08\x10\x1B\x1C\x00\x00")
    self.fpga_wv2(0x04E4, "\x08\x00\x1C\x1C\x00\x00")
    self.fpga_wv2(0x04E8, "\x08\x00\x24\x1D\x00\x08")
    self.fpga_wv2(0x04EC, "\x08\x22\x3C\x0C\x00\x00")
    self.fpga_wv2(0x04F0, "\x08\x32\x78\x0C\x00\x00")
    self.fpga_wv2(0x04F4, "\x08\x22\xB4\x0C\x00\x00")
    self.fpga_wv2(0x04F8, "\x08\x32\xF0\x0C\x00\x00")
    self.fpga_wv2(0x04FC, "\x08\x22\x2C\x0C\x00\x01")
    self.fpga_wv2(0x0500, "\x08\x02\x35\x0C\x00\x01")
    self.fpga_wv2(0x0504, "\x08\x0A\x3E\x0C\x00\x01")
    self.fpga_wv2(0x0508, "\x08\x1A\x47\x0C\x00\x01")
    self.fpga_wv2(0x050C, "\x08\x0A\x4C\x0C\x00\x01")
    self.fpga_wv2(0x0510, "\x08\x1A\x50\x0C\x00\x01")
    self.fpga_wv2(0x0514, "\x08\x0A\x59\x0C\x00\x01")
    self.fpga_wv2(0x0518, "\x08\x02\x5E\x0C\x00\x01")
    self.fpga_wv2(0x051C, "\x08\x12\x66\x0C\x00\x01")
    self.fpga_wv2(0x0520, "\x08\x02\x67\x0C\x00\x01")
    self.fpga_wv2(0x0524, "\x08\x02\x6F\x0D\x00\x09")
    self.fpga_wv2(0x0528, "\x08\x00\x08\x0C\x00\x00")
    self.fpga_wv2(0x052C, "\x08\x00\x10\x04\x00\x00")
    self.fpga_wv2(0x0530, "\x08\x00\x18\x00\x00\x08")
    self.fpga_wv2(0x0534, "\x08\x10\x09\x0C\x00\x00")
    self.fpga_wv2(0x0538, "\x08\x00\x12\x0C\x00\x00")
    self.fpga_wv2(0x053C, "\x08\x10\x1B\x0C\x00\x00")
    self.fpga_wv2(0x0540, "\x08\x00\x1C\x0C\x00\x00")
    self.fpga_wv2(0x0544, "\x08\x00\x24\x0D\x00\x08")
    self.fpga_wv2(0x0548, "\x08\x00\x04\x04\x00\x08")
    self.fpga_wv2(0x054C, "\x08\x00\x18\x04\x00\x08")
    self.fpga_wv2(0x0550, "\x08\x45\x09\x80\x00\x00")
    self.fpga_wv2(0x0554, "\x08\xC5\x36\x80\x00\x00")
    self.fpga_wv2(0x0558, "\x08\x45\x3F\x80\x00\x00")
    self.fpga_wv2(0x055C, "\x08\x04\x48\x80\x00\x00")
    self.fpga_wv2(0x0560, "\x08\x00\x51\x80\x00\x08")
    self.fpga_wv2(0x0564, "\x08\x00\x04\x84\x00\x08")
    self.fpga_wv2(0x0568, "\x09\x24\x60\x04\x00\x00")
    self.fpga_wv2(0x056C, "\x09\x36\xC0\x04\x00\x00")
    self.fpga_wv2(0x0570, "\x09\x24\x20\x04\x00\x01")
    self.fpga_wv2(0x0574, "\x09\x36\x80\x04\x00\x01")
    self.fpga_wv2(0x0578, "\x09\x24\x40\x04\x00\x02")
    self.fpga_wv2(0x057C, "\x09\x00\xA0\x04\x00\x02")
    self.fpga_wv2(0x0580, "\x09\x01\x00\x04\x00\x03")
    self.fpga_wv2(0x0584, "\x09\x03\x60\x04\x00\x03")
    self.fpga_wv2(0x0588, "\x09\x01\xC0\x04\x00\x03")
    self.fpga_wv2(0x058C, "\x09\x03\x20\x04\x00\x04")
    self.fpga_wv2(0x0590, "\x09\x01\x80\x04\x00\x04")
    self.fpga_wv2(0x0594, "\x09\x00\x40\x04\x00\x0D")
    self.fpga_wv2(0x0598, "\x0F\x42\x18\x04\x00\x00")
    self.fpga_wv2(0x059C, "\x0F\x02\x22\x04\x00\x00")
    self.fpga_wv2(0x05A0, "\x0E\x02\x6A\x04\x00\x00")
    self.fpga_wv2(0x05A4, "\x0A\x00\x6F\x04\x00\x00")
    self.fpga_wv2(0x05A8, "\x0A\x80\x87\x04\x00\x00")
    self.fpga_wv2(0x05AC, "\x0A\x00\xFF\x04\x00\x00")
    self.fpga_wv2(0x05B0, "\x08\x00\x04\x04\x00\x09")


def setup_fpga2_sm(self):
    self.fpga_wv2(0x1000, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x1008, "\x00\x02\x00\x00\x00\x00\x90\x00\x00\x00")
    self.fpga_wv2(0x1010, "\x00\x03\x00\x00\x00\x00\x90\x00\x00\x0A")
    self.fpga_wv2(0x1018, "\x04\x03\xAA\x00\x00\x00\x90\x00\x00\x1A")
    self.fpga_wv2(0x1020, "\x00\x05\x00\x00\x00\x00\x90\x00\x00\x1E")
    self.fpga_wv2(0x1028, "\x00\x06\x00\x00\x00\x00\x00\x00\x00\x25")
    self.fpga_wv2(0x1030, "\x07\x06\x63\x00\x00\x00\x00\x00\x00\x32")
    self.fpga_wv2(0x1038, "\x08\x07\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1040, "\x09\x08\xA8\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1048, "\x0A\x09\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1050, "\x0B\x0A\xA8\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1058, "\x0C\x0B\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1060, "\x0D\x0C\xA8\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1068, "\x0E\x0D\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1070, "\x0F\x0E\xA8\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1078, "\x10\x0F\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1080, "\x11\x10\x0A\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1088, "\x03\x11\x0A\x12\x00\x70\x00\x00\x00\x32")
    self.fpga_wv2(0x1090, "\x02\x12\xC8\x13\xFF\xF0\x90\x00\x00\x1A")
    self.fpga_wv2(0x1098, "\x00\x14\x00\x00\x00\x00\x90\x00\x00\x54")
    self.fpga_wv2(0x10A0, "\x15\x14\xFF\x00\x00\x0F\x00\x00\x00\x59")
    self.fpga_wv2(0x10A8, "\x00\x16\x00\x00\x00\x00\x90\x00\x00\x5A")
    self.fpga_wv2(0x10B0, "\x00\x17\x00\x00\x00\x00\x90\x00\x00\x66")
    self.fpga_wv2(0x10B8, "\x00\x18\x00\x00\x00\x00\x00\x00\x00\x3B")
    self.fpga_wv2(0x10C0, "\x19\x18\x0F\x00\x00\x04\x00\x00\x00\x4D")
    self.fpga_wv2(0x10C8, "\x1A\x19\xFF\x00\x00\x0F\x00\x00\x00\x53")
    self.fpga_wv2(0x10D0, "\x01\x16\x0F\x00\x00\x06\x00\x00\x00\x52")
    self.fpga_wv2(0x10D8, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10E0, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10E8, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10F0, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10F8, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")


def setup_fpga1_lg(self):
    self.fpga_wv2(0x0400, "\x00\x00\x60\x00\x00\x00")
    self.fpga_wv2(0x0404, "\x00\xE5\xC0\x00\x00\x00")
    self.fpga_wv2(0x0408, "\x00\xF7\x20\x00\x00\x01")
    self.fpga_wv2(0x040C, "\x00\xE5\x80\x00\x00\x01")
    self.fpga_wv2(0x0410, "\x00\xF7\xE0\x00\x00\x01")
    self.fpga_wv2(0x0414, "\x00\xE5\xA0\x00\x00\x02")
    self.fpga_wv2(0x0418, "\x00\xC5\x20\x00\x00\x04")
    self.fpga_wv2(0x041C, "\x00\x05\x38\x00\x00\x04")
    self.fpga_wv2(0x0420, "\x00\x04\x98\x00\x00\x04")
    self.fpga_wv2(0x0424, "\x00\x00\xF8\x02\x00\x0C")
    self.fpga_wv2(0x0428, "\x08\x00\x3F\x00\x00\x00")
    self.fpga_wv2(0x042C, "\x08\x00\x42\x04\x00\x00")
    self.fpga_wv2(0x0430, "\x08\x04\x4B\x04\x00\x00")
    self.fpga_wv2(0x0434, "\x08\x06\x54\x04\x00\x00")
    self.fpga_wv2(0x0438, "\x08\x04\x5D\x04\x00\x00")
    self.fpga_wv2(0x043C, "\x08\x06\x66\x04\x00\x00")
    self.fpga_wv2(0x0440, "\x08\x04\x6F\x04\x00\x00")
    self.fpga_wv2(0x0444, "\x08\x00\x72\x04\x00\x00")
    self.fpga_wv2(0x0448, "\x08\x01\x78\x04\x00\x00")
    self.fpga_wv2(0x044C, "\x08\x03\x7E\x04\x00\x00")
    self.fpga_wv2(0x0450, "\x08\x01\x84\x04\x00\x00")
    self.fpga_wv2(0x0454, "\x08\xC3\x8A\x04\x00\x00")
    self.fpga_wv2(0x0458, "\x08\xC1\x90\x04\x00\x00")
    self.fpga_wv2(0x045C, "\x08\xC0\x96\x04\x00\x00")
    self.fpga_wv2(0x0460, "\x08\xC2\x9C\x04\x00\x00")
    self.fpga_wv2(0x0464, "\x08\xC0\xA2\x04\x00\x08")
    self.fpga_wv2(0x0468, "\x08\x42\x06\x04\x00\x00")
    self.fpga_wv2(0x046C, "\x08\x00\x0C\x04\x00\x00")
    self.fpga_wv2(0x0470, "\x08\x82\x12\x04\x00\x00")
    self.fpga_wv2(0x0474, "\x08\x00\x18\x04\x00\x08")
    self.fpga_wv2(0x0478, "\x0F\x42\x18\x04\x00\x00")
    self.fpga_wv2(0x047C, "\x0F\x02\x22\x04\x00\x00")
    self.fpga_wv2(0x0480, "\x0E\x02\x6A\x04\x00\x00")
    self.fpga_wv2(0x0484, "\x0A\x02\x6F\x04\x00\x00")
    self.fpga_wv2(0x0488, "\x0A\x82\x87\x04\x00\x00")
    self.fpga_wv2(0x048C, "\x0A\x02\xFF\x04\x00\x00")
    self.fpga_wv2(0x0490, "\x08\x02\x04\x04\x00\x09")
    self.fpga_wv2(0x0494, "\x08\x20\x09\x04\x00\x00")
    self.fpga_wv2(0x0498, "\x08\x30\x12\x04\x00\x00")
    self.fpga_wv2(0x049C, "\x08\x20\x1B\x04\x00\x00")
    self.fpga_wv2(0x04A0, "\x08\x30\x24\x04\x00\x00")
    self.fpga_wv2(0x04A4, "\x08\x20\x2D\x04\x00\x00")
    self.fpga_wv2(0x04A8, "\x08\x00\x36\x04\x00\x00")
    self.fpga_wv2(0x04AC, "\x08\x0A\x3F\x04\x00\x00")
    self.fpga_wv2(0x04B0, "\x08\x1A\x48\x04\x00\x00")
    self.fpga_wv2(0x04B4, "\x08\x0A\x51\x04\x00\x00")
    self.fpga_wv2(0x04B8, "\x08\x1A\x5A\x04\x00\x00")
    self.fpga_wv2(0x04BC, "\x08\x0A\x63\x04\x00\x00")
    self.fpga_wv2(0x04C0, "\x08\x00\x64\x04\x00\x00")
    self.fpga_wv2(0x04C4, "\x08\x10\x6C\x04\x00\x08")
    self.fpga_wv2(0x04C8, "\x08\x10\x04\x0C\x00\x00")
    self.fpga_wv2(0x04CC, "\x08\x00\x08\x0C\x00\x00")
    self.fpga_wv2(0x04D0, "\x08\x10\x0C\x0C\x00\x00")
    self.fpga_wv2(0x04D4, "\x08\x00\x10\x0C\x00\x08")
    self.fpga_wv2(0x04D8, "\x08\x10\x09\x1C\x00\x00")
    self.fpga_wv2(0x04DC, "\x08\x00\x12\x1C\x00\x00")
    self.fpga_wv2(0x04E0, "\x08\x10\x1B\x1C\x00\x00")
    self.fpga_wv2(0x04E4, "\x08\x00\x1C\x1C\x00\x00")
    self.fpga_wv2(0x04E8, "\x08\x00\x24\x1D\x00\x08")
    self.fpga_wv2(0x04EC, "\x08\x22\x3C\x00\x00\x00")
    self.fpga_wv2(0x04F0, "\x08\x32\x78\x00\x00\x00")
    self.fpga_wv2(0x04F4, "\x08\x22\xB4\x00\x00\x00")
    self.fpga_wv2(0x04F8, "\x08\x32\xF0\x00\x00\x00")
    self.fpga_wv2(0x04FC, "\x08\x22\x2C\x00\x00\x01")
    self.fpga_wv2(0x0500, "\x08\x02\x35\x00\x00\x01")
    self.fpga_wv2(0x0504, "\x08\x0A\x3E\x00\x00\x01")
    self.fpga_wv2(0x0508, "\x08\x1A\x47\x00\x00\x01")
    self.fpga_wv2(0x050C, "\x08\x0A\x4C\x00\x00\x01")
    self.fpga_wv2(0x0510, "\x08\x1A\x50\x00\x00\x01")
    self.fpga_wv2(0x0514, "\x08\x0A\x59\x00\x00\x01")
    self.fpga_wv2(0x0518, "\x08\x02\x5E\x00\x00\x01")
    self.fpga_wv2(0x051C, "\x08\x12\x66\x00\x00\x01")
    self.fpga_wv2(0x0520, "\x08\x02\x67\x00\x00\x01")
    self.fpga_wv2(0x0524, "\x08\x02\x6F\x01\x00\x09")
    self.fpga_wv2(0x0528, "\x08\x00\x08\x0C\x00\x00")
    self.fpga_wv2(0x052C, "\x08\x00\x10\x04\x00\x00")
    self.fpga_wv2(0x0530, "\x08\x00\x18\x00\x00\x08")
    self.fpga_wv2(0x0534, "\x08\x10\x09\x00\x00\x00")
    self.fpga_wv2(0x0538, "\x08\x00\x12\x00\x00\x00")
    self.fpga_wv2(0x053C, "\x08\x10\x1B\x00\x00\x00")
    self.fpga_wv2(0x0540, "\x08\x00\x1C\x00\x00\x00")
    self.fpga_wv2(0x0544, "\x08\x00\x24\x01\x00\x08")
    self.fpga_wv2(0x0548, "\x08\x10\x09\x1C\x00\x00")
    self.fpga_wv2(0x054C, "\x08\x00\x12\x1C\x00\x00")
    self.fpga_wv2(0x0550, "\x08\x10\x1B\x1C\x00\x00")
    self.fpga_wv2(0x0554, "\x08\x00\x1C\x1C\x00\x00")
    self.fpga_wv2(0x0558, "\x08\x00\x24\x1D\x00\x08")
    self.fpga_wv2(0x055C, "\x08\xC2\x06\x00\x00\x00")
    self.fpga_wv2(0x0560, "\x08\xC0\x0C\x00\x00\x00")
    self.fpga_wv2(0x0564, "\x08\xC2\x12\x00\x00\x00")
    self.fpga_wv2(0x0568, "\x08\xC0\x18\x00\x00\x08")
    self.fpga_wv2(0x056C, "\x08\x45\x09\x80\x00\x00")
    self.fpga_wv2(0x0570, "\x08\xC5\x36\x80\x00\x00")
    self.fpga_wv2(0x0574, "\x08\x45\x3F\x80\x00\x00")
    self.fpga_wv2(0x0578, "\x08\x04\x48\x80\x00\x00")
    self.fpga_wv2(0x057C, "\x08\x00\x51\x80\x00\x08")
    self.fpga_wv2(0x0580, "\x08\x00\x04\x80\x00\x08")
    self.fpga_wv2(0x0584, "\x09\x24\x60\x00\x00\x00")
    self.fpga_wv2(0x0588, "\x09\x36\xC0\x00\x00\x00")
    self.fpga_wv2(0x058C, "\x09\x24\x20\x00\x00\x01")
    self.fpga_wv2(0x0590, "\x09\x36\x80\x00\x00\x01")
    self.fpga_wv2(0x0594, "\x09\x24\x40\x00\x00\x02")
    self.fpga_wv2(0x0598, "\x09\x00\xA0\x00\x00\x02")
    self.fpga_wv2(0x059C, "\x09\x01\x00\x00\x00\x03")
    self.fpga_wv2(0x05A0, "\x09\x03\x60\x00\x00\x03")
    self.fpga_wv2(0x05A4, "\x09\x01\xC0\x00\x00\x03")
    self.fpga_wv2(0x05A8, "\x09\x03\x20\x00\x00\x04")
    self.fpga_wv2(0x05AC, "\x09\x01\x80\x00\x00\x04")
    self.fpga_wv2(0x05B0, "\x09\x00\x40\x00\x00\x0D")
    self.fpga_wv2(0x05B4, "\x0F\x42\x18\x00\x00\x00")
    self.fpga_wv2(0x05B8, "\x0F\x02\x22\x00\x00\x00")
    self.fpga_wv2(0x05BC, "\x0E\x02\x6A\x00\x00\x00")
    self.fpga_wv2(0x05C0, "\x0A\x00\x6F\x00\x00\x00")
    self.fpga_wv2(0x05C4, "\x0A\x80\x87\x00\x00\x00")
    self.fpga_wv2(0x05C8, "\x0A\x00\xFF\x00\x00\x00")
    self.fpga_wv2(0x05CC, "\x08\x00\x04\x00\x00\x09")


def setup_fpga2_lg(self):
    self.fpga_wv2(0x1000, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x1008, "\x00\x02\x00\x00\x00\x00\x90\x00\x00\x00")
    self.fpga_wv2(0x1010, "\x00\x03\x00\x00\x00\x00\x90\x00\x00\x0A")
    self.fpga_wv2(0x1018, "\x04\x03\xCC\x00\x00\x00\x90\x00\x00\x1A")
    self.fpga_wv2(0x1020, "\x00\x05\x00\x00\x00\x00\x90\x00\x00\x1E")
    self.fpga_wv2(0x1028, "\x00\x06\x00\x00\x00\x00\x00\x00\x00\x25")
    self.fpga_wv2(0x1030, "\x07\x06\x63\x00\x00\x00\x00\x00\x00\x32")
    self.fpga_wv2(0x1038, "\x08\x07\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1040, "\x09\x08\xF5\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1048, "\x0A\x09\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1050, "\x0B\x0A\xF5\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1058, "\x0C\x0B\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1060, "\x0D\x0C\xF5\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1068, "\x0E\x0D\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1070, "\x0F\x0E\xF5\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1078, "\x10\x0F\x20\x00\x00\x00\x00\x00\x00\x36")
    self.fpga_wv2(0x1080, "\x11\x10\x0A\x13\xFF\xF0\x00\x00\x00\x32")
    self.fpga_wv2(0x1088, "\x03\x11\x0A\x12\x00\x70\x00\x00\x00\x32")
    self.fpga_wv2(0x1090, "\x02\x12\xDC\x13\xFF\xF0\x90\x00\x00\x1A")
    self.fpga_wv2(0x1098, "\x00\x14\x00\x00\x00\x00\x90\x00\x00\x5B")
    self.fpga_wv2(0x10A0, "\x15\x14\xFF\x00\x00\x0F\x00\x00\x00\x60")
    self.fpga_wv2(0x10A8, "\x00\x16\x00\x00\x00\x00\x90\x00\x00\x61")
    self.fpga_wv2(0x10B0, "\x00\x17\x00\x00\x00\x00\x90\x00\x00\x6D")
    self.fpga_wv2(0x10B8, "\x00\x18\x00\x00\x00\x00\x00\x00\x00\x3B")
    self.fpga_wv2(0x10C0, "\x16\x18\x3E\x01\x73\x95\x00\x00\x00\x4D")
    self.fpga_wv2(0x10C8, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10D0, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10D8, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10E0, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10E8, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10F0, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    self.fpga_wv2(0x10F8, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
