"""


    """

import pandas as pd

from proj.v import v
from proj.fp import fp
from proj.f import f

def make_all_combinations() :
    """  """

    ##
    info = [i / 100 for i in range(30 , 100 , 10)]
    info += [.99]

    ##
    gt = {
            0 : ('FS' , fp.dsg_by_info , fp.fs_dsg_corr) ,
            1 : ('FS' , fp.hc_by_info , fp.fs_hc_corr) ,
            2 : ('PO' , fp.dsg_by_info , fp.po_dsg_corr) ,
            3 : ('PO' , fp.hc_by_info , fp.po_hc_corr) ,
            }

    df1 = pd.DataFrame.from_dict(data = gt , orient = 'index')
    df2 = pd.DataFrame(data = info , columns = [v.info_score])

    ##
    df3 = pd.merge(df1 , df2 , how = 'cross')

    ##
    def format_file_path(row , cn) :
        return row[cn].as_posix().format(int(row[v.info_score] * 100))

    for cn in [1 , 2] :
        df3[cn] = df3.apply(lambda r : format_file_path(r , cn) , axis = 1)

    ##
    return df3

def gat_pairs_ids_in_pairs(identifier) :
    df = pd.read_csv(f.rel , sep = '\s+' , dtype = 'string')
    msk = df['InfType'].eq(identifier)
    df = df[msk]
    df = df[['ID1' , 'ID2']]
    return df

def make_pairs_gts_dfs(df_gts , df_pairs_ids) :
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

    dfa = dfa.drop(columns = ['ID1'])
    dfb = dfb.drop(columns = ['ID2'])

    return dfa , dfb

def save_corr(pr , ip , op , iscore) :
    """ """

    def test() :
        pass

        ##
        pr = 'PO'
        iscore = .4
        ip = fp.dsg_by_info.as_posix().format(int(iscore * 100))
        op = fp.fs_dsg_corr.as_posix().format(int(iscore * 100))

    ##
    df = gat_pairs_ids_in_pairs(pr)

    ##
    df_gts = pd.read_parquet(ip)

    ##
    dfa , dfb = make_pairs_gts_dfs(df_gts , df)

    ##
    # reorder columns to make sure both pairs have the same order of snps
    dfb = dfb[dfa.columns]

    ##
    gts1 = dfa.iloc[: , 1 :]
    gts2 = dfb.iloc[: , 1 :]

    ##
    df_cors = gts1.corrwith(gts2 , method = 'pearson')

    ##
    df_cors.to_excel(op)
    print(op)

def main() :
    pass

    ##
    df3 = make_all_combinations()

    ##
    for pr , ip , op , iscore in df3.itertuples(index = False) :
        print(pr , ip , op , iscore)
        save_corr(pr , ip , op , iscore)

    ##

def testing_area() :
    pass

    ##
    info_score = 0.9
    ps = 'FS'

    ##
    df_cors.iloc[890 :1000]

    ##
    df_cors.isna().any()

    ##
    msk = df_cors.isna()
    df1 = df_cors[msk]

    ##
    g1 = gts1['rs6057425']
    g2 = gts2['rs6057425']

    ##
    g1.isna().any()
    g2.isna().any()

    ##

    ##
