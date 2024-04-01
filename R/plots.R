#!/usr/bin/env Rscript

install.packages("data.table")
install.packages("dplyr")
install.packages("glue")
install.packages("readxl")

library("data.table")
library("dplyr")
library("plinkFile")
library("genio")
library("ggplot2")
library("glue")
library('readxl')



plot_corr <- function(dta_fp, pair_name, gtype_name, info_score, fpo) 
  {
  df <- read_excel(dta_fp, col_names = T)
  names(df) = c('snp', 'corr')
  df <- na.omit(df)
  
  n_snps <- nrow(df)
  dn = info_score / 100
  
  ggplot(data.frame(df), aes(x = corr)) +
    geom_histogram(binwidth = 0.02, fill = "#56B4E9", colour = "#56B4E9", alpha = 0.5) +
    labs(title = glue('{pair_name}, {gtype_name}, SNPS with INFO = {dn} - {dn+0.01} (n = {n_snps})'),
         x = "Genotype Correlation",
         y = "Count") +
    geom_vline(xintercept=0.5, linetype="dotted") +
    geom_vline(xintercept=mean(df$corr), linetype="dashed", color = 'red') +
    theme_classic() +
    theme(legend.position="none")
  
  ggsave(fpo)
  }

info <- c(30, 40, 50, 60, 70, 80, 90, 99)

out_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/fig/FS-dsg-hist'
dta_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/dta/FS-dsg-corr'

prd <- expand.grid(out_dir, dta_dir, 'Full Sibs', 'Dosages', info)

out_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/fig/FS-hc-hist'
dta_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/dta/FS-hc-corr'

prd1 <- expand.grid(out_dir, dta_dir, 'Full Sibs', 'Hard-Call', info)

prd <- rbind(prd, prd1)

out_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/fig/PO-dsg-hist'
dta_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/dta/PO-dsg-corr'

prd1 <- expand.grid(out_dir, dta_dir, 'Parent-Offspring', 'Dosages', info)

prd <- rbind(prd, prd1)


out_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/fig/PO-hc-hist'
dta_dir <- '/Users/mmir/Library/CloudStorage/Dropbox/C1-P-G/A1-Git-SF/imputed-genotype-corr-240317-SF/out/dta/PO-hc-corr'

prd1 <- expand.grid(out_dir, dta_dir, 'Parent-Offspring', 'Hard-Call', info)

prd <- rbind(prd, prd1)

for (x in 1:nrow(prd))
  {
  pair_name = prd[x, 'Var3']
  gtype_name = prd[x, 'Var4']
  info_score = prd[x, 'Var5']
  dta_fp = glue("{prd[x, 'Var2']}/i{info_score}.xlsx")
  fpo = glue("{prd[x, 'Var1']}/i{info_score}.png")
  
  plot_corr(dta_fp,pair_name,gtype_name,info_score, fpo)
  }

