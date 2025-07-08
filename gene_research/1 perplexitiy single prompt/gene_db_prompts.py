#/usr/bin/env python
# -*- coding: utf-8 -*-


# placeholders: 'locus_tag','product','protein_id','pseudo','Name_gene','gene_gene','gene_biotype','old_locus_tag']
prompt_for_single_prompt_perplexity_prochlorococcus = '''
Search for and review published studies related to the specified gene, focusing on its role in Prochlorococcus, cyanobacteria, or similar marine microorganisms. 

Search for and review published studies related to the specified gene, focusing on its role in Prochlorococcus, cyanobacteria, or similar marine microorganisms. 
if there is no data available on this gene in Prochlorococcus, search for studies in related cynobactria, like synechococcus or Synechocystis. 
And if even those are not available look for info on this gene in gram negative bacteria or in marine autotrophs.

You are a research assistant tasked with creating a comprehensive summary of a specific gene's function.
Your goal is to provide a detailed, fact-based summary using published scientific literature.

This summary will be used to analyze the transcriptome of a coculture of Prochlorococcus MED4 and Alteromonas under nitrogen limitation conditions. 

The gene you will be researching is:
<gene_name>
{gene_name_or_id}
</gene_name>


<locus_tag>
{locus_tag}
</locus_tag>

<product>
{product}
</product>

<protein_id>
{protein_id} 
</protein_id>

<old_locus_tag>
{old_locus_tag}
</old_locus_tag>


In your research summary, cover the following areas:
1. Gene function
2. Impact on physiological state
3. Involvement in stress response
4. Role in nutrient exchange (uptake and release)
5. Contribution to oxidative stress
6. Influence on bacterial interaction in coculture

Follow these steps to conduct your research and present your findings:

1. Search for and review published studies related to the specified gene, focusing on its role in Prochlorococcus, cyanobacteria, or similar marine microorganisms. 
if there is no data available on this gene in Prochlorococcus, search for studies in related cynobactria, like synechococcus or Synechocystis. 
And if even those are not available look for info on this gene in gram negative bacteria or in marine autotrophs.

2. For each area listed above, provide a summary of the gene's role or impact, based on factual data from scientific papers. Include multiple findings per category if available.


6. After completing your research, assess your confidence in the findings. Consider factors such as the number of relevant studies, consistency of results across studies, and the recency of the research. Provide a brief justification for your confidence assessment.

7. Based on your justification, assign a confidence score on a scale of 1 to 10, where 1 is the lowest confidence and 10 is the highest.

Format your response as follows:

<research_summary>
<gene_function>
[Summary of gene function with citations]
</gene_function>

<physiological_impact>
[Summary of impact on physiological state with citations]
</physiological_impact>

<stress_response>
[Summary of involvement in stress response with citations]
</stress_response>


<nutrient_exchange>
[Summary of role in nutrient exchange with citations]
</nutrient_exchange>

<nutrient_uptake>
[Summary of role in nutrient exchange with citations]
</nutrient_uptake>


<nutrient_release>
[Summary of role in nutrient exchange with citations]
</nutrient_release>

<oxidative_stress>
[Summary of contribution to dealing with oxidative stress with citations]
</oxidative_stress>

<bacterial_interaction>
[Summary of influence on bacterial interaction in coculture with citations]
</bacterial_interaction>


<confidence_assessment>
[Justification for confidence score]
</confidence_assessment>

<confidence_score>
[Numerical score between 1 and 10]
</confidence_score>
</research_summary>


Ensure that your summary is comprehensive, fact-based, and based on published literature.  
If there is insufficient information available for any section, state this clearly and explain why the information might be lacking.

'''


prompt_for_single_prompt_perplexity_prochlorococcus_with_citations = '''
You are a research assistant tasked with creating a comprehensive summary of a specific gene's function and its role in the coculture of Prochlorococcus and Alteromonas under nitrogen limitation conditions. Your goal is to provide a detailed, fact-based summary using published scientific literature.

The gene you will be researching is:
<gene_name>
{gene_name_or_id}
</gene_name>

<organism>
Prochlorococcus MED4
</organism>

<locus_tag>
{locus_tag}
</locus_tag>

<product>
{product}
</product>

<protein_id>
{protein_id} 
</protein_id>

<old_locus_tag>
{old_locus_tag}
</old_locus_tag>


In your research summary, cover the following areas:
1. Gene function
2. Impact on physiological state
3. Involvement in stress response
4. Role in nutrient exchange (uptake and release)
5. Contribution to oxidative stress
6. Influence on bacterial interaction in coculture

Follow these steps to conduct your research and present your findings:

1. Search for and review published studies related to the specified gene, focusing on its role in Prochlorococcus, cyanobacteria, or similar marine microorganisms.

2. For each area listed above, provide a summary of the gene's role or impact, based on factual data from scientific papers. Include multiple findings per category if available.

3. When discussing gene expression or protein abundances, provide interpretations of their significance in the context of the coculture and nitrogen limitation.

4. Cite all papers used in your research. Provide URL where available. Otherwise, use the following format for citations: (Author et al., Year). For example: (Smith et al., 2020).

6. After completing your research, assess your confidence in the findings. Consider factors such as the number of relevant studies, consistency of results across studies, and the recency of the research. Provide a brief justification for your confidence assessment.

7. Based on your justification, assign a confidence score on a scale of 1 to 10, where 1 is the lowest confidence and 10 is the highest.

Format your response as follows:

<research_summary>
<gene_function>
[Summary of gene function with citations]
</gene_function>

<physiological_impact>
[Summary of impact on physiological state with citations]
</physiological_impact>

<stress_response>
[Summary of involvement in stress response with citations]
</stress_response>


<nutrient_exchange>
[Summary of role in nutrient exchange with citations]
</nutrient_exchange>

<nutrient_uptake>
[Summary of role in nutrient exchange with citations]
</nutrient_uptake>


<nutrient_release>
[Summary of role in nutrient exchange with citations]
</nutrient_release>

<oxidative_stress>
[Summary of contribution to dealing with oxidative stress with citations]
</oxidative_stress>

<bacterial_interaction>
[Summary of influence on bacterial interaction in coculture with citations]
</bacterial_interaction>


<citations>
[list of papers cited throughout. Including title, authors, year and journal. Include url and DOI where available]
</citations>

<confidence_assessment>
[Justification for confidence score]
</confidence_assessment>

<confidence_score>
[Numerical score between 1 and 10]
</confidence_score>
</research_summary>


Ensure that your summary is comprehensive, fact-based, and properly cited. If there is insufficient information available for any section, state this clearly and explain why the information might be lacking.

'''



second_prompt_for_single_prompt_perplexity_prochlorococcus = '''
I have the following information about the gene {gene_name_or_id} in Prochlorococcus MED4:


# REVIEW text to be reformatted:
{review_text}


# list of citations in the review (in bibtex format):
{citations}



# TASK AND INSTRUCTIONS
Your primary goal is to populate a JSON object that strictly adheres to the `GeneResearchSummarySimple` schema based on the review above and published literature.
Your task is to search the web for relevant scientific literature related to the gene `{gene_name_or_id}` and synthesize the findings into a structured JSON object.


1.  **Gene Function:** First, determine and concisely state the primary function of the gene `{gene_name_or_id}`.
2.  **Identify Findings:** Scour the literature for specific experimental findings related to the **Key Biological Processes of Interest** mentioned above.
3.  **Populate ResearchFindingSimple:** For each distinct finding, create a `ResearchFindingSimple` object.
    - **finding_category/finding_type:** Use one of the key process terms (e.g., 'nutrient uptake', 'stress response', 'coculture role').
    - **finding_description:** Be specific. Instead of "involved in N metabolism," write "Shown to be upregulated under nitrogen starvation, facilitating the uptake of ammonium."
    - **finding_evidence:** Extract the experimental method, e.g., 'gene expression analysis (RNA-seq)', 'proteomic analysis (mass spectrometry)', 'knockout mutant phenotype'.
    - **organism:** Names of the organisms used in the study
    - **Phylogenetic Distance:** This is crucial. Assess the organism used in the study:
        - 'Direct': The study was done in Prochlorococcus.
        - 'Close': The study was in another cyanobacterium (e.g., Synechococcus, Synechocystis).
        - 'Relevant': The study was in another marine bacterium (e.g., Alteromonas itself, Vibrio).
        - 'Distant': The study was in a model organism like E. coli or yeast, but the function is highly conserved.
    - **Confidence Score (1-10):** Assign a score based on the evidence's relevance and directness.
        - **10:** Direct experimental evidence (e.g., knockout) in the exact Prochlorococcus strain of interest showing the effect.
        - **8-9:** Direct evidence (transcriptome/proteome) in Prochlorococcus or a very close relative under nitrogen limitation.
        - **6-7:** Strong evidence in a related cyanobacterium or clear homology-based inference.
        - **3-5:** Inferred function based on studies in distant organisms (e.g., E. coli) or purely correlational data.
        - **1-2:** Highly speculative connection.
4.  **Final Output:** Your final output must be **only the JSON object** that can be parsed directly. Do not include any explanatory text before or after the JSON.


Ensure that the JSON object strictly adheres to the `GeneResearchSummarySimple` schema. The schema requires the following fields:
```python
class ResearchFindingSimple(BaseModel):
    """ Description of the research process and findings related to a specific finding on a specific gene"""
    finding_category: str = Field(description="Category of the finding, e.g. 'physiological', 'gene function', 'stress response', 'nutrient uptake', 'nutrient exudation', 'coculture role'")
    finding_sub_category: str = Field(description="sub category of the finding, e.g. 'high light stress' for stress response, nutrient name/type for nutrient exchange")
    finding_description: str = Field(description="Description of the finding related to the gene")
    finding_evidence: str = Field(description="Evidence supporting this finding, e.g. 'gene knockout experiments', 'gene expression analysis', 'protein interaction studies'")
    finding_type: str = Field(description="Type of finding, e.g. 'gene function', 'stress response', 'nutrient uptake', 'nutrient exudation', 'coculture role'")
    url: str = Field(description="URL to access the research paper supporting this finding")
    title: str = Field(description="Title of the research paper supporting this finding")
    citation: str = Field(description="Citation for the research paper supporting this finding (use APA format)")
    organism: str = Field(description="Organism where the finding is studied in the cited literature")
    phylogenetic_distance: str = Field(description="Phylogenetic distance between this research and Prochlorococcus")
    additional_notes: str = Field(description="Any additional notes or comments about the finding")
    confidence_score: Optional[int] = Field(
        le=10, ge=1,  # Confidence score must be between 1 and 10
        default=None, description="A numerical score representing the confidence in the evidence, from 1 to 10"
    )



class GeneResearchSummarySimple(BaseModel):
    """Research on a specific gene's involvement in coping with stress conditions"""  
    gene_name: str = Field(description="Name of the gene being studied")
    gene_function: str = Field(description="Function of the gene") 
    research_findings: List[ResearchFindingSimple] = Field(description="List of research findings related to this gene, can be empty if none found")

```


In addition, assign citations for each entry based on urls in the `urls for the citations` list  (if applicable). All citations should correspond to valid papers cited correctly. Ensure that each citation is correctly formatted and corresponds to the findings in the review text. If no cication is available, return 'No Paper Found'.


'''

