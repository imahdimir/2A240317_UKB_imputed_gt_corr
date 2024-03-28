from pathlib import Path

PROJ = 'imputed-genotype-corr-240317'

class Dirs :
    g_all_proj = Path('/var/genetics/ws/mahdimir/LOCAL/proj')
    g_proj = g_all_proj / PROJ
    g_proj_in = g_proj / 'in'
    g_med = g_proj / 'med'

    unpkd_mfi = g_proj_in / 'unpckd_ukb_imp_mfi'

    dsg_dta = g_med / 'dsg_dta'
    hc_dta = g_med / 'hc_dta'

    dsg_dta_by_info = g_med / 'dsg_dta_by_info'
    hc_dta_by_info = g_med / 'hc_dta_by_info'

    imp_gts = Path('/disk/genetics/data/ukb/private/v3/raw/imputed')

    flt_snps = g_med / 'flt_snps'
    plink_out = g_med / 'plink_out'

    fs_dsg = g_med / 'fs-dsg'
    fs_hc = g_med / 'fs-hc'
    po_dsg = g_med / 'po-dsg'
    po_hc = g_med / 'po-hc'

d = Dirs()
