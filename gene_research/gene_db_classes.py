#/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List

from pydantic import BaseModel, Field

from enum import Enum

class EvidenceType(str, Enum):
    EXPERIMENTAL = "experimental"
    OBSERVATIONAL = "observational"
    CORRELATIVE = "correlative"
    ANECDOTAL = "anecdotal"
    META_ANALYTIC = "meta_analytic"
    EXPERT_OPINION = "expert_opinion"
    THEORETICAL = "theoretical"

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    INSUFFICIENT = "insufficient"

class EvidenceStrength(str, Enum):
    DEFINITIVE = "definitive"
    STRONG = "strong"
    SUGGESTIVE = "suggestive"
    WEAK = "weak"
    SPECULATIVE = "speculative"


class Reference(BaseModel):
    """Reference to the literature supporting a finding"""
    title: str = Field(description="Title of the research paper")
    authors: str = Field(description="Authors of the research paper")
    journal: str = Field(description="Journal where the research was published")
    year: int = Field(description="Year of publication")
    doi: Optional[str] = Field(default=None, description="DOI of the research paper, if available")
    url: Optional[str] = Field(default=None, description="URL to access the research paper, if available")



class ResearchSummary(BaseModel):
    """ Description of the research process and findings related to a specific finding on a specific gene"""
    reference: Reference = Field(description="Reference to the literature supporting this finding")
    evidence: str = Field(description="Evidence supporting this gene's role in the research literature cited in the reference field")
    evidence_type: EvidenceType = Field(description="Type of evidence supporting this finding, e.g. 'experimental', 'observational', 'correlative', 'anecdotal', 'meta-analytic', 'expert opinion', 'theoretical'")
    phylogenetic_conservation: str = Field(description="Phylogenetic conservation of this finding, e.g. 'conserved in all Prochlorococcus species' or 'conserved in all cyanobacteria' or 'conserved in all bacteria' or 'not conserved'")
    organism: str = Field(description="Organism where the finding is studied in the cited literature")
    experimental_approach: str = Field(description="Experimental approach used to study the finding in the cited literature")
    confidence_level: ConfidenceLevel = Field(description="Confidence level of the evidence supporting the finding")
    degree_of_confidence: EvidenceStrength = Field(description="Degree of confidence in the evidence supporting the finding")
    additional_notes: str = Field(description="Any additional notes or comments about the finding")
    confidence_score: Optional[int] = Field(
        default=None, description="A numerical score representing the confidence in the evidence, from 1 to 10"
    )


class StressResponse(BaseModel):
    """line item in a gene entry research on this gene involvement in coping with stress condition"""
    description: str = Field(description="Description of this gene role in coping with this specific stress response")
    type_of_stress: str = Field(description="Type of stress this gene helps to cope with, e.g., 'high light', 'low light', 'high temperature', 'low temperature', 'high salinity', 'low salinity', 'high CO2', 'low CO2', 'nitrogen limitation', 'phosphorus limitation', 'iron limitation'")
    #pathways: List[str] = Field(description="list of Pathways this gene belongs to that are involved in the stress response process, e.g., 'MAPK signaling', 'calcium signaling'")
    research_summaries: list[ResearchSummary] = Field(description="List of research summaries related to this stress response on this gene")

class NutrientUptake(BaseModel):
    """Nutrient uptake related to a specific gene"""
    nutrient: str = Field(description="Nutrient being taken up. e.g., 'nitrogen', 'phosphorus', 'iron'")
    description: str = Field(description="Description of this gene role in the uptake process related to this nutrient")
    #pathways: List[str] = Field(description="list of Pathways this gene belongs to that are involved in the nutrient uptake process, e.g., 'nitrate assimilation', 'phosphate uptake', 'iron transport'")
    research_summaries: list[ResearchSummary] = Field(description="List of research summaries related to this nutrient uptake on this gene")

class NutrientExudation(BaseModel):
    """Nutrient exudation related to a specific gene"""
    nutrient: str = Field(description="Nutrient being exuded. e.g., 'nitrogen', 'phosphorus', 'iron'")
    description: str = Field(description="Description of this gene role in the exudation process related to this nutrient")
    #pathways: List[str] = Field(description="list of Pathways this gene belongs to that are involved in the nutrient exudation process, e.g., 'nitrate exudation', 'phosphate exudation', 'iron exudation'")
    research_summaries: list[ResearchSummary] = Field(description="List of research summaries related to this nutrient exudation on this gene")


class RoleInCoculture(BaseModel):
    """Role of a specific gene in coculture conditions with heterotrophic bacteria"""
    interaction_type: str = Field(description="Type of interaction, e.g., 'mutualism', 'commensalism', 'parasitism'")
    description: str = Field(description="Description of this gene role in coculture conditions with heterotrophic bacteria")
    involved_bacteria: List[str] = Field(description="List of bacteria involved in the interaction")
    #pathways: List[str] = Field(description="list of Pathways this gene belongs to that are involved in the interaction process, e.g., 'nitrate assimilation', 'phosphate uptake', 'iron transport'")
    research_summaries: list[ResearchSummary] = Field(description="List of research summaries related to this coculture role on this gene")


class GeneResearchEntry(BaseModel):
    """Research on a specific gene's involvement in coping with stress conditions"""
    gene_protein_id: str = Field(description="Identifier for the gene product, e.g., UniProt ID")
    gene_refseq_id: str = Field(description="RefSeq ID for the gene")
    gene_name: str = Field(description="Name of the gene being studied")
    gene_function: str = Field(description="Function of the gene")
    gene_function_description: str = Field(description="Detailed description of the gene's function")
    go_terms: list[str] = Field(description="Gene Ontology (GO) terms associated with the gene")
    COGs: list[str] = Field(description="Clusters of Orthologous Groups (COGs) associated with the gene")
    KEGG_pathways: list[str] = Field(description="KEGG pathways associated with the gene")
    pfam_domains: list[str] = Field(description="Pfam domains associated with the gene")
    physiological_contribution: str = Field(description="How this gene contributes to the overall physiological state of the organism")
    stress_responses: list[StressResponse] = Field(description="List of stress responses associated with this gene, can be empty if none found")
    nutrient_uptake: list[NutrientUptake] = Field(description="List of nutrient uptake processes associated with this gene, can be empty if none found")
    nutrient_exudation: list[NutrientExudation] = Field(description="List of nutrient exudation processes associated with this gene, can be empty if none found")
    role_in_coculture: list[RoleInCoculture] = Field(description="List of coculture processes associated with this gene, can be empty if none found")

