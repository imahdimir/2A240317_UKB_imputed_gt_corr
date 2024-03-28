from pv.d import d

class FilePatterns :
    hc_dta = d.hc_dta / 'chr{}.prq'
    dsg_dta = d.dsg_dta / 'chr{}.prq'

    hc_by_info = d.hc_dta_by_info / 'i{}.prq'
    dsg_by_info = d.dsg_dta_by_info / 'i{}.prq'

    fs_dsg_corr = d.fs_dsg / 'i{}.xlsx'
    fs_hc_corr = d.fs_hc / 'i{}.xlsx'
    po_dsg_corr = d.po_dsg / 'i{}.xlsx'
    po_hc_corr = d.po_hc / 'i{}.xlsx'

fp = FilePatterns()
