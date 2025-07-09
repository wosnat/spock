#/usr/bin/env python
# -*- coding: utf-8 -*-


# run the first step of building gene db - review from perplexity
# # Single prompt from perplexity
# 
# This notebook implements creating a simple DB using a single prompt from perplexity, using the builtin web search in the model. Not using any of the complex reasoning model as this is the first attempt - but using the sonar-pro model and the relatively high context to improve the result.
# 
# Because perplexity does not support structured outputs, the result undergo a second transformation by chatgpt-4o-mini which change the format to the DB format.

import os
import json
import pandas as pd
import numpy as np
import gffpandas.gffpandas as gffpd
import asyncio
import aiofiles
from dotenv import load_dotenv

# pip install -qU "langchain-perplexity"
from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.prompts import ChatPromptTemplate


import gene_db_classes 
import gene_db_prompts 


# # Load MED4 genes
def get_genes_from_gff():
    med4_genome_dpath = '../../genomes/MED4'

    annotation = gffpd.read_gff3(os.path.join(med4_genome_dpath, 'genomic.gff'))
    gff_cds_df = annotation.filter_feature_of_type(['CDS']).attributes_to_columns()
    gff_gene_df = annotation.filter_feature_of_type(['gene']).attributes_to_columns()

    gff_df = pd.merge(gff_cds_df, gff_gene_df, on='locus_tag', suffixes=('_cds', '_gene'), how='left')

    gff_columns = [
        #'seq_id_cds', 'source_cds', 'type_cds', 'start_cds', 'end_cds',
        #'score_cds', 'strand_cds', 'phase_cds', 'attributes_cds', 'Dbxref',
        #'ID_cds', 
        #'Name_cds', #'Note', 'Parent', 'end_range', 'exception',
        #'gbkey_cds', 
        #'gene_cds', #'inference', 
        'locus_tag', #'partial', 
        'product',
        'protein_id', 'pseudo', #'transl_table', 'seq_id_gene', 'source_gene',
        #'type_gene', 'start_gene', 'end_gene', 'score_gene', 'strand_gene',
        #'phase_gene', 'attributes_gene', 'ID_gene', 
        'Name_gene', #'gbkey_gene',
        'gene_gene', 
        'gene_biotype', 'old_locus_tag'
    ]

    # These are different types of gene biotypes from NCBI's GFF (General Feature Format) annotation files, each representing a distinct functional category of genes:
    # * protein_coding: Genes that encode proteins - these are transcribed into mRNA and then translated into amino acid sequences to form functional proteins. This represents the majority of genes in most genomes.
    # * tmRNA: Transfer-messenger RNA genes that encode a unique type of RNA molecule found in bacteria. tmRNA rescues ribosomes that become stalled during translation by acting as both a tRNA and an mRNA, allowing the ribosome to complete translation and tag the incomplete protein for degradation.
    # * tRNA: Transfer RNA genes that produce tRNA molecules responsible for bringing amino acids to the ribosome during protein synthesis. Each tRNA recognizes specific codons in the mRNA and carries the corresponding amino acid.
    # * rRNA: Ribosomal RNA genes that encode the RNA components of ribosomes. These are essential structural and catalytic components of the protein synthesis machinery, including the 16S, 23S, and 5S rRNAs in bacteria.
    # * ncRNA: Non-coding RNA genes that produce functional RNA molecules that are not translated into proteins. This is a broad category that includes various regulatory RNAs like microRNAs, long non-coding RNAs, and small interfering RNAs.
    # * SRP_RNA: Signal Recognition Particle RNA genes that encode the RNA component of the signal recognition particle. This ribonucleoprotein complex recognizes signal sequences on newly synthesized proteins and directs them to the endoplasmic reticulum for proper cellular localization.
    # * RNase_P_RNA: Ribonuclease P RNA genes that encode the catalytic RNA subunit of RNase P, an enzyme responsible for processing the 5' end of precursor tRNA molecules during tRNA maturation.
    # These biotype classifications help researchers understand the functional diversity of genes beyond just protein-coding sequences, highlighting the important roles that various RNA molecules play in cellular processes.


    # focus on protein coding genes
    # to start with, we will only use protein coding genes that are not pseudogenes

    gff_df_filter = gff_df[gff_df.gene_biotype.isin(['protein_coding']) & gff_df.pseudo.isna() & ~gff_df.gene_gene.isna()][gff_columns]
    # rename to the name used in the template
    gff_df_filter = gff_df_filter.rename(columns={'Name_gene':'gene_name_or_id'})

    #gff_df_filter.to_csv(os.path.join(out_dpath, 'MED4_genes_filter.csv'), index=False)

    return gff_df_filter





# Define the main async function
async def run_agent(perplexity_llm, extra_body_perplexity, list_of_dicts, prompts, out_dpath):


    # Process with abatch_as_completed
    async for i, result in perplexity_llm.abatch_as_completed(prompts):
        param_dict = list_of_dicts[i].copy()
        
        # add to the result 
        #print(sample_result.additional_kwargs['citations'])
        param_dict['content'] = result.content if hasattr(result, 'content') else str(result)
        if hasattr(result, 'additional_kwargs') and 'citations' in result.additional_kwargs:
            param_dict['citations'] = result.additional_kwargs['citations'] 
        else:
            param_dict['citations'] = ['citations not found']



        
        # Save to individual file
        fpath = os.path.join(out_dpath, f'{param_dict["locus_tag"]}_first_query.json')
        
        async with aiofiles.open(fpath, 'w') as f:
            await f.write(json.dumps(param_dict, indent=2))
        



# Run the agent using asyncio
if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser('run perplexity to get initial gene reviews')
    parser.add_argument("--outdpath", help="output dir", default='batch_results/first_pass')
    parser.add_argument("--langsmith_prefix", help="langsmith project name", default='pplx_first_run')
    parser.add_argument("--genes_csv", help="csv file with genes to run", default='batch_results/first_pass/MED4_genes_filter.csv')
    parser.add_argument("--reload_gff", help="reload gene list from the gff",
                    action="store_true")

    args = parser.parse_args()

    load_dotenv(override=True)

    
    out_dpath = args.outdpath
    os.makedirs(out_dpath, exist_ok=True)


    
    # update langchain project
    from datetime import datetime
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    langsmith_project = f'{args.langsmith_prefix}_{current_time}'
    os.environ["LANGSMITH_PROJECT"] = langsmith_project
    print('Setting LANGSMITH_PROJECT =', langsmith_project)

    # load the list of genes
    if args.reload_gff:
        gff_df_filter = get_genes_from_gff()
    else:
        gff_df_filter = pd.read_csv(args.genes_csv)


    # # Initialize the models and create templates
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.833,  # 50 requests per minute
        check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
        max_bucket_size=50,  # Controls the maximum burst size.
    )
    modelname = 'sonar-reasoning-pro'
    perplexity_llm = init_chat_model(modelname, model_provider="perplexity", temperature=0, max_tokens=3000, rate_limiter=rate_limiter)

    # perlexity additional parameters
    extra_body_perplexity = dict(search_mode="academic", web_search_options=dict(search_context_size="high"))

    prompt_template = ChatPromptTemplate([
        #("system", gene_db_prompts.system_prompt_from_gemini_without_literature_placeholder),
        ("user", gene_db_prompts.prompt_for_single_prompt_perplexity_prochlorococcus)
    ])
    # no structured output for tier 1 models in perplexity
    #structured_llm = llm.with_structured_output(gene_db_classes.GeneResearchSummarySimple)


    # get the prompts
    list_of_dicts = list(gff_df_filter.T.to_dict().values())
    prompts = prompt_template.batch(list_of_dicts)

    # finally, run the agent
    asyncio.run(run_agent(perplexity_llm, extra_body_perplexity, list_of_dicts, prompts, out_dpath ))
