from prj.s import s
from prj.g import g

class Files :
    rel = '/disk/genetics/ukb/alextisyoung/haplotypes/relatives/bedfiles/hap.kin0'

    fs_po_ids_txt = g.med / 'fs_po_ids.txt'
    flt_snps = g.med / 'flt_snps.prq'

    corrs = s.o_dta / 'corrs.xlsx'

f = Files()
