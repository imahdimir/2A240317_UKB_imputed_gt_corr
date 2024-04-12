from pathlib import Path

PROJ = 'imputed-genotype-corr-240317'

class GDir :
    imp_gts = Path('/disk/genetics/data/ukb/private/v3/raw/imputed')
    all_prj = Path('/var/genetics/ws/mahdimir/LOCAL/prj')

    prj = all_prj / PROJ

    inp = prj / 'inp'
    med = prj / 'med'

    unpkd_mfi = inp / 'unpckd_ukb_imp_mfi'

    dsg_dta = med / 'dsg_dta'
    hc_dta = med / 'hc_dta'

    flt_snps = med / 'flt_snps'
    plink_out = med / 'plink_out'

g = GDir()
