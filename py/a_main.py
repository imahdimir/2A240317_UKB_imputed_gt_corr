"""


    """

import itertools
import numpy as np
import pandas as pd
from bgen_reader import open_bgen
from pathlib import Path
from braceexpand import braceexpand

from pv.d import d , PROJ
from pv.f import f
from pv.v import v
from pv.fp import fp

class MfiCols :
    n_maf = 5
    n_info = 7
    n_rsid = 1

    maf = 'MAF'
    info = 'INFO'
    rsid = 'rsid'

mc = MfiCols()

class Vars :
    msk = 'msk'
    ms1 = 'ms1'
    bin = 'bin'
    chr = 'chr'

    inftype = 'InfType'

v = Vars()

bins = {
        0 : .3 ,
        1 : .4 ,
        2 : .5 ,
        3 : .6 ,
        4 : .7 ,
        5 : .8 ,
        6 : .9 ,
        7 : .99 ,
        }

##
def merge_all_chromosoms_snps() :
    """ """

    ##
    df = pd.DataFrame()
    for i in range(1 , 22 + 1) :
        print(i)
        snps_fp = dyr.unpkd_mfi / f'ukb_mfi_chr{i}_v3.txt'
        _df = pd.read_csv(snps_fp , sep = '\s+' , header = None)
        _df[v.chr] = i
        df = pd.concat([df , _df])

    ##
    ren_cols = {
            mc.n_rsid : mc.rsid ,
            mc.n_maf  : mc.maf ,
            mc.n_info : mc.info ,
            }

    df = df.rename(columns = ren_cols)

    ##
    df.to_parquet(fp.snps , index = False)

##
def save_subdf_to_txt(df , cn) :
    """ """
    print(cn)
    df = df.iloc[: , :8]
    print(len(df))
    _fp = fpt.snps.format(cn)
    df.to_csv(_fp , sep = '\t' , index = False , header = False)

##
def filter_snps() :
    """    """

    ##
    df0 = pd.read_parquet(fp.snps)
    _df = df0.head()

    ##
    # to not reading again from disk for subsequent runs
    df = df0.copy()

    ##
    # keep snps with maf > 1%
    msk = df[mc.maf].gt(.01)
    df1 = df[msk]

    ##
    df = df1.copy()

    ##
    df[v.msk] = False

    for b in bins.values() :
        df[v.ms1] = df[mc.info].ge(b) & df[mc.info].lt(b + .01)
        _df = df[df[v.ms1]]
        if len(_df) > 1000 :
            _df = _df.sample(1000)

        df.loc[_df.index , v.msk] = True

    ##
    df = df[df[v.msk]]

    ##
    df = df.drop(columns = [v.msk , v.ms1])
    df.columns = list(range(8)) + [v.chr]

    ##
    gps = df.groupby([v.chr])
    gps.apply(lambda x : save_subdf_to_txt(x , x.name))

    ##

##
def separate_snps_by_chr() :
    """ """

    ##
    for i in range(1 , 22 + 1) :
        snps_fp = dyr.unpkd_mfi / f'ukb_mfi_chr{i}_v3.txt'

    ##
    df = pd.read_csv(fp.flt_snps_txt , sep = '\t' , header = None)

    ##
    for i in range(1 , 22 + 1) :
        msk = df[0].str.split(':').str[0]

        print(msk)
        # _df = df[msk]
        # _df.to_csv(dyr.med / f'snps_chr{i}.txt' ,
        #            sep = '\t' ,
        #            index = False ,
        #            header = False)
        break

##
def filter_snps_second_approach() :
    """ this approach is for using with bgen files manually, didn't work """

    ##
    df0 = pd.read_parquet(fp.snps)
    _df = df0.head()

    ##
    # to not reading again from disk for subsequent runs
    df = df0.copy()

    ##
    # keep snps with maf > 1%
    msk = df[mc.maf].gt(.01)
    df = df[msk]

    ##
    df[v.msk] = False

    for b in bins.values() :
        df[v.ms1] = df[mc.info].gt(b) & df[mc.info].le(b + .01)
        _df = df[df[v.ms1]]
        if len(_df) > 1000 :
            _df = _df.sample(1000)

        df.loc[_df.index , v.msk] = True

    ##
    df = df[df[v.msk]]

    ##
    for b in bins.values() :
        msk = df[mc.info].gt(b) & df[mc.info].le(b + .01)
        df.loc[msk , v.bin] = b

    ##
    df.to_parquet(fp.flt_snps_1 , index = False)

##
def filter_fs_and_po() :
    """ """

    ##
    df = pd.read_csv(fp.rel , sep = '\s+' , dtype = 'string')

    ##
    types = {
            'full_sibs'        : 'FS' ,
            'parent_offspring' : 'PO'
            }

    msk = df[v.inftype].isin(types.values())

    df = df[msk]

    ##
    df1 = df[['FID1' , 'ID1']]
    df2 = df[['FID2' , 'ID2']]

    df1.columns = ['FID' , 'ID']
    df2.columns = ['FID' , 'ID']

    df = pd.concat([df1 , df2])
    df = df.iloc[: , :2]

    ##
    df.to_csv(fp.fs_po_ids_txt , index = False , header = False , sep = '\t')

##
def filter_fs() :
    """ """

    ##
    df = pd.read_csv(fp.rel , sep = '\s+' , dtype = 'string')

    ##
    types = {
            'full_sibs' : 'FS' ,
            }

    msk = df[v.inftype].isin(types.values())

    df = df[msk]

    ##
    df1 = df[['FID1' , 'ID1']]
    df2 = df[['FID2' , 'ID2']]

    df1.columns = ['FID' , 'ID']
    df2.columns = ['FID' , 'ID']

    df = pd.concat([df1 , df2])
    df = df.iloc[: , :2]

    ##
    df.to_csv(fp.sibs_ids_txt , index = False , header = False , sep = '\t')

##
def make_df_of_iids_from_bgen_open_obj(bg_opn) :
    """ """

    ##
    bg_opn_s = list(bg_opn.samples)
    df = pd.DataFrame({
            'IID' : bg_opn_s
            })

    # get the IID from FID_IID
    df['IID'] = df['IID'].str.split('_').str[1]

    ##
    return df

##
def open_bgen_ret_iid_df_and_prob_arr(bgen_fp) :
    """ """

    ##
    bg_opn = open_bgen(bgen_fp)

    ##
    df_id = make_df_of_iids_from_bgen_open_obj(bg_opn)

    ##
    nd_p = bg_opn.read()

    ##
    return df_id , nd_p

##
def save_dosages_of_all_vars_from_bgen(bgen_fp: Path) :
    """ """

    ##
    df_id , nd_p = open_bgen_ret_iid_df_and_prob_arr(bgen_fp)

    ##
    nd_d = nd_p[: , : , 1] + 2 * nd_p[: , : , 2]

    ##
    df1 = pd.DataFrame(nd_d)

    ##
    df_d = pd.concat([df_id , df1] , axis = 1)

    ##
    _fp = dyr.med / f'dosages_{bgen_fp.stem}.prq'
    df_d.to_parquet(_fp , index = False)

##
def save_hard_calls_of_all_vars_from_bgen(bgen_fp) :
    """ """

    ##
    df_id , nd_p = open_bgen_ret_iid_df_and_prob_arr(bgen_fp)

    ##
    nd_h = np.argmax(nd_p , axis = 2)

    ##
    df1 = pd.DataFrame(nd_h)

    ##
    df_h = pd.concat([df_id , df1] , axis = 1)

    ##
    _fp = dyr.med / f'hard_calls_{bgen_fp.stem}.prq'
    df_h.to_parquet(_fp , index = False)

##
def gat_pairs_ids_in_pairs(identifier) :
    """ """

    df = pd.read_csv(fp.rel , sep = '\s+' , dtype = 'string')

    msk = df['InfType'].eq(identifier)

    df = df[msk]

    df = df[['ID1' , 'ID2']]

    return df

##
def make_prq_fp(gts_type , info_score , pair_suf) :
    """ """
    prq_fp = dyr.med / f'{gts_type}_snps_{info_score}{pair_suf}.prq'
    return prq_fp

##
def make_pairs_gts_dfs(df_gts , df_pairs_ids) :
    """ """

    ##
    dfa = pd.merge(df_pairs_ids[['ID1']] ,
                   df_gts ,
                   left_on = 'ID1' ,
                   right_on = 'IID' ,
                   how = 'left')
    dfb = pd.merge(df_pairs_ids[['ID2']] ,
                   df_gts ,
                   left_on = 'ID2' ,
                   right_on = 'IID' ,
                   how = 'left')

    ##
    dfa = dfa.drop(columns = ['ID1'])
    dfb = dfb.drop(columns = ['ID2'])

    ##
    return dfa , dfb

##
def save_corr_of_sib_pairs_with_gts_df(pair_identifier ,
                                       gts_type ,
                                       info_score ,
                                       pair_type ,
                                       pair_suf
                                       ) :
    """ """

    ##
    df_pairs_ids = gat_pairs_ids_in_pairs(pair_identifier)

    ##
    prq_fp = make_prq_fp(gts_type , info_score , pair_suf)
    df_gts = pd.read_parquet(prq_fp)

    ##
    dfa , dfb = make_pairs_gts_dfs(df_gts , df_pairs_ids)

    ##
    gts1 = dfa.iloc[: , 1 :]
    gts2 = dfb.iloc[: , 1 :]

    ##
    df_cors = gts1.corrwith(gts2 , method = 'pearson')

    ##
    out_fp = dyr.out_dta / f'corr_{pair_type}_{gts_type}_{info_score}.xlsx'
    df_cors.to_excel(out_fp , index = False , header = False)
    print(out_fp)

##
def main() :
    pass

    ##
    info_scores = {
            0 : 30 ,
            1 : 99 ,
            }

    pairs = {
            'sibs'             : ('' , 'FS') ,
            'parent_offspring' : ('_po' , 'PO') ,
            }

    gts_types = {
            0 : 'dosages' ,
            1 : 'hard_calls'
            }

    ##
    prd = itertools.product(info_scores.values() , pairs.values())

    for info , pair in prd :
        print(info , pair)
        fp = dyr.plink_out / f'snps_{info}{pair[0]}.bgen'
        print(fp)

        save_dosages_of_all_vars_from_bgen(fp)

        save_hard_calls_of_all_vars_from_bgen(fp)

    ##
    prd = itertools.product(info_scores.values() ,
                            pairs.keys() ,
                            gts_types.values())

    for info , pair_type , gm in prd :
        pair_iden = pairs[pair_type][1]
        print(info , pair_type , gm)
        pair_suf = pairs[pair_type][0]
        save_corr_of_sib_pairs_with_gts_df(pair_iden ,
                                           gm ,
                                           info ,
                                           pair_type ,
                                           pair_suf)

    ##

    ##

    ##

    ##
