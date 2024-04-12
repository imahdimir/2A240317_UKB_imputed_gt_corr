from prj.s import s
from prj.g import g

class FilePatterns :
    dsg_dta = g.dsg_dta / 'chr{}.prq'
    hc_dta = g.hc_dta / 'chr{}.prq'

    dsg_by_info = s.dsg_by_info / 'i{}.prq'
    hc_by_info = s.hc_by_info / 'i{}.prq'

    fs_dsg_corr = s.fs_dsg_corr / 'i{}.xlsx'
    fs_hc_corr = s.fs_hc_corr / 'i{}.xlsx'
    po_dsg_corr = s.po_dsg_corr / 'i{}.xlsx'
    po_hc_corr = s.po_hc_corr / 'i{}.xlsx'

fp = FilePatterns()
