from pathlib import Path

class SFDir :
    sf = '/var/genetics/ws/mahdimir/DropBox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF'
    sf = Path(sf)

    inp = sf / 'inp'
    med = sf / 'med'
    out = sf / 'out'

    o_dta = out / 'dta'
    o_fig = out / 'fig'

    dsg_by_info = med / 'dsg-by-info'
    hc_by_info = med / 'hc-by-info'

    fs_dsg_corr = o_dta / 'FS-dsg-corr'
    fs_hc_corr = o_dta / 'FS-hc-corr'
    po_dsg_corr = o_dta / 'PO-dsg-corr'
    po_hc_corr = o_dta / 'PO-hc-corr'

    fs_dsg_hist = o_fig / 'FS-dsg-hist'
    fs_hc_hist = o_fig / 'FS-hc-hist'
    po_dsg_hist = o_fig / 'PO-dsg-hist'
    po_hc_hist = o_fig / 'PO-hc-hist'

s = SFDir()
