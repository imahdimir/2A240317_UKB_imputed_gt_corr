"""


    """

import itertools
import pandas as pd

from lib.f import f
from lib.fp import fp
from lib.s import d
from lib.v import v

def merge_all_flt_snps() :
    fps = list(d.flt_snps.glob('*.txt'))
    df = pd.DataFrame()
    for _p in fps :
        print(_p)
        _df = pd.read_csv(_p , sep = '\t' , header = None)
        df = pd.concat([df , _df])
    df.to_parquet(f.flt_snps , index = False)

def ret_all_snps_in_info_range(info_range_start) :
    dfs = pd.read_parquet(f.flt_snps)
    sc = info_range_start
    msk = dfs[v.info_n_s].ge(sc)
    msk &= dfs[v.info_n_s].lt(sc + .01)
    df = dfs[msk]
    return df

def return_all_iids() :
    df = pd.read_csv(f.fs_po_ids_txt , sep = '\t' , header = None)
    df[v.iid] = df[1]
    df = df[[v.iid]]
    df = df.drop_duplicates()
    return df

def make_all_combinations_of_dsgs_n_hc() :
    gt = {
            fp.dsg_dta : fp.dsg_by_info ,
            fp.hc_dta  : fp.hc_by_info ,
            }

    info = [i / 100 for i in range(30 , 100 , 10)]
    info += [.99]

    prd = itertools.product(gt.items() , info)

    return prd

def merge_from_entire_genome(in_pat , out_pat , info_score) :
    df = return_all_iids()

    dfi = ret_all_snps_in_info_range(info_score)
    c2k0 = [v.iid] + list(dfi[v.rsid_n_s])

    for _i in range(1 , 22 + 1) :
        print(_i)
        _p = in_pat.as_posix().format(_i)
        print(_p)
        _df = pd.read_parquet(_p)

        c2k = _df.columns.intersection(c2k0)

        _df = _df[c2k]

        _df[v.iid] = _df[v.iid].astype('string')
        df[v.iid] = df[v.iid].astype('string')

        assert df.columns.intersection(_df.columns).difference([v.iid]).empty

        df = pd.merge(df , _df , how = 'left' , on = v.iid)

        print(df.shape)

    _p = out_pat.as_posix().format(int(info_score * 100))
    df.to_parquet(_p , index = False)

def merge_info_scores_from_entire_genome() :
    prd = make_all_combinations_of_dsgs_n_hc()

    for (in_pat , out_pat) , info_score in prd :
        merge_from_entire_genome(in_pat , out_pat , info_score)

def gat_pairs_ids_in_pairs(identifier) :
    df = pd.read_csv(f.rel , sep = '\s+' , dtype = 'string')
    msk = df['InfType'].eq(identifier)
    df = df[msk]
    df = df[['ID1' , 'ID2']]
    return df

def main() :
    pass

    ##
    merge_all_flt_snps()

    ##
    merge_info_scores_from_entire_genome()

    ##

    ##

def testing_area() :
    pass

    ##
    df = return_all_iids()

    ##
    df1 = df.drop_duplicates()

    ##
    dft = ret_all_snps_in_info_range(.9)

    ##
    merge_from_entire_genome(fp.dsg_dta , fp.dsg_by_info , .9)

    ##
    p = fp.dsg_by_info.as_posix().format(90)
    df = pd.read_parquet(p)

    ##
    df = df.drop_duplicates()

    ##
    df = df.drop_duplicates(subset = [v.iid])

    ##

    ##
