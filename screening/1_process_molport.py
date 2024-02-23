import rdkit
print(rdkit.__version__)
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole


import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdmolfiles
from rdkit.Chem.rdmolfiles import SmilesMolSupplier
from rdkit.Chem import SDMolSupplier
from rdkit.Chem import AllChem, PandasTools
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from rdkit.Chem import SaltRemover
import os



#from RingSystems.Preprocessing import src
from src import MoleculePreprocessor

from src.MoleculePreprocessorExtended import MoleculePreprocessorExtended
from rdkit import RDLogger


file_name = '/mdspace/sliu/SMILES/iissc_smiles-001-000-000--001-499-999.txt'

with open(file_name, "r") as ins:
    smiles = []
    for line in ins:
        smiles.append(line.split('\n')[0])


df = pd.DataFrame(smiles, columns=["col0"])
df[["SMILES", "SMILES_CANONICAL", "MOLPORTID", "STANDARD_INCHI", "INCHIKEY", "IUPAC", "PUBCHEM_EXT_SUBSTANCE_URL", "VERIFIED_AMOUNT_MG", "UNVERIFIED_AMOUNT_MGtIS_SC", "IS_BB", "COMPOUND_STATE", "QC_METHOD", "BEST_LEAD_TIME", "PRICERANGE_1MG", "PRICERANGE_5MG", "PRICERANGE_50MG", "PRICERANGE_100MG", "PRICERANGE_250MG", "PRICERANGE_1G"]] = df["col0"].str.split("\t", n=18, expand=True)
df = df.drop(index=0)

moleculesProcessed = MoleculePreprocessorExtended.init_with_smiles(list(df.SMILES_CANONICAL))
moleculesProcessed.csp_wash()
preprocessedSmilesDict = moleculesProcessed.get_rawsmiles_smiles_dict()
preprocessedSmiles_df = pd.DataFrame(list(preprocessedSmilesDict.items()), columns=['rawSmiles','preprocessedSmiles'])
preprocessed_df = pd.merge(df, preprocessedSmiles_df, 
                           left_on='SMILES_CANONICAL', right_on='rawSmiles')
preprocessed_df.dropna(subset=['preprocessedSmiles'],inplace=True) 
preprocessed_df = preprocessed_df[preprocessed_df['preprocessedSmiles']!='']
preprocessed_df.drop_duplicates('preprocessedSmiles',inplace=True)
preprocessed_df_useful = preprocessed_df[['preprocessedSmiles','MOLPORTID']]
preprocessed_df_useful.to_csv('Molport_preprocessed3.csv', index=False)

