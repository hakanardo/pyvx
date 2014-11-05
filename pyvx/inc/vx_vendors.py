cdef = '''
enum vx_vendor_id_e {
    VX_ID_KHRONOS   = 0x000, 
    VX_ID_TI        = 0x001, 
    VX_ID_QUALCOMM  = 0x002, 
    VX_ID_NVIDIA    = 0x003, 
    VX_ID_ARM       = 0x004, 
    VX_ID_BDTI      = 0x005, 
    VX_ID_RENESAS   = 0x006, 
    VX_ID_VIVANTE   = 0x007, 
    VX_ID_XILINX    = 0x008, 
    VX_ID_AXIS      = 0x009, 
    VX_ID_MOVIDIUS  = 0x00A, 
    VX_ID_SAMSUNG   = 0x00B, 
    VX_ID_FREESCALE = 0x00C, 
    VX_ID_AMD       = 0x00D, 
    VX_ID_BROADCOM  = 0x00E, 
    VX_ID_INTEL     = 0x00F, 
    VX_ID_MARVELL   = 0x010, 
    VX_ID_MEDIATEK  = 0x011, 
    VX_ID_ST        = 0x012, 
    VX_ID_CEVA      = 0x013, 
    VX_ID_ITSEEZ    = 0x014, 
    VX_ID_IMAGINATION=0x015, 
    VX_ID_COGNIVUE  = 0x016, 
    VX_ID_VIDEANTIS = 0x017, 
    /* Add new vendor code above this line */

    VX_ID_MAX       = 0xFFF,
    VX_ID_DEFAULT = VX_ID_MAX,
};
'''

