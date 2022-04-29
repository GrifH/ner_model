from __future__ import unicode_literals, print_function

import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.training.example import Example
import pickle

abstract1 = "We analysed primary breast cancers by genomic DNA copy number arrays, DNA methylation, exome sequencing, messenger RNA arrays, microRNA sequencing and reverse-phase protein arrays. Our ability to integrate information across platforms provided key insights into previously defined gene expression subtypes and demonstrated the existence of four main breast cancer classes when combining data from five platforms, each of which shows significant molecular heterogeneity. Somatic mutations in only three genes (TP53, PIK3CA and GATA3) occurred at > 10% incidence across all breast cancers; however, there were numerous subtype-associated and novel gene mutations including the enrichment of specific mutations in GATA3, PIK3CA and MAP3K1 with the luminal A subtype. We identified two novel protein-expression-defined subgroups, possibly produced by stromal/microenvironmental elements, and integrated analyses identified specific signalling pathways dominant in each molecular subtype including a HER2/phosphorylated HER2/EGFR/phosphorylated EGFR signature within the HER2-enriched expression subtype. Comparison of basal-like breast tumours with high-grade serous ovarian tumours showed many molecular commonalities, indicating a related aetiology and similar therapeutic opportunities. The biological finding of the four main breast cancer subtypes caused by different subsets of genetic and epigenetic abnormalities raises the hypothesis that much of the clinically observable plasticity and heterogeneity occurs within, and not across, these major biological subtypes of breast cancer."

ent1 = {"entities": [(137,151,"Disease"), (488,501,"Disease"), (668,672,"Gene"), (692,699,"Gene"), (721,726,"Gene"), (784,798,"Disease"), (944,949,"Gene"), (969,975,"Gene"), (998,1004,"Gene"), (1033,1042,"Subtype"), (1377,1401,"Subtype"), (1497,1504,"Organ"), (1480,1486,"Organ"), (1547,1554,"Disease"), (1531,1538,"Disease"), (1995,2008,"Disease")]}

abstract2 = "We pooled data from more than 10,000 cases of invasive breast cancer from 12 studies that had collected information on hormone receptor status, human epidermal growth factor receptor-2 (HER2) status, and at least one basal marker (cytokeratin [CK]5/6 or epidermal growth factor receptor [EGFR]) together with survival time data. Tumours were classified as luminal and nonluminal tumours according to hormone receptor expression. These two groups were further subdivided according to expression of HER2, and finally, the luminal and nonluminal HER2-negative tumours were categorised according to expression of basal markers. Changes in mortality rates over time differed by subtype. In women with luminal HER2-negative subtypes, mortality rates were constant over time, whereas mortality rates associated with the luminal HER2-positive and nonluminal subtypes tended to peak within 5 y of diagnosis and then decline over time. In the first 5 y after diagnosis the nonluminal tumours were associated with a poorer prognosis, but over longer follow-up times the prognosis was poorer in the luminal subtypes, with the worst prognosis at 15 y being in the luminal HER2-positive tumours. Basal marker expression distinguished the HER2-negative luminal and nonluminal tumours into different subtypes. These patterns were independent of any systemic adjuvant therapy."

ent2 = {"entities":[(172,185,"Disease"),(494,501,"Subtype"),(527,537,"Subtype"),(700,707,"Subtype"),(733,757,"Subtype"),(917,939,"Subtype"),(1056,1077,"Subtype"),(1105,1115,"Subtype"),(1252,1262,"Subtype"),(1399,1406,"Subtype"),(1486,1507,"Subtype"),(1582,1595,"Subtype"),(1619,1626,"Subtype"),(1654,1664,"Subtype")]}

abstract3 = "Breast cancer is heterogeneous in prognoses and drug responses. To organize breast cancers by gene expression independent of statistical methodology, we identified the Breast Cancer Consensus Subtypes (BCCS) as the consensus groupings of six different subtyping methods. Our classification software identified seven BCCS subtypes in a study cohort of publicly available data (n = 5950) including METABRIC, TCGA-BRCA, and data assayed by Affymetrix arrays. All samples were fresh-frozen from primary tumors. The estrogen receptor-positive (ER+) BCCS subtypes were: PCS1 (18%) good prognosis, stromal infiltration; PCS2 (15%) poor prognosis, highly proliferative; PCS3 (13%) poor prognosis, highly proliferative, activated IFN-gamma signaling, cytotoxic lymphocyte infiltration, high tumor mutation burden; PCS4 (18%) good prognosis, hormone response genes highly expressed. The ER− BCCS subtypes were: NCS1 (11%) basal; NCS2 (10%) elevated androgen response; NCS3 (5%) cytotoxic lymphocyte infiltration; unclassified tumors (9%). HER2+ tumors were heterogeneous with respect to BCCS."

ent3 = {"entities":[(117,130,"Disease"),(214,228,"Disease"),(674,700,"Subtype"),(723,726,"Subtype"),(769,774,"Subtype"),(839,843,"Subtype"),(909,913,"Subtype"),(1073,1077,"Subtype"),(1194,1198,"Subtype"),(1235,1239,"Subtype"),(1297,1301,"Subtype"),(1391,1397,"Subtype")]}

abstract4 = "Breast cancer is the most frequently found cancer in women and the one most often subjected to genetic analysis. Nonetheless, it has been causing the largest number of women's cancer-related deaths. PAM50, the intrinsic subtype assay for breast cancer, is beneficial for diagnosis but does not explain each subtype’s mechanism. Deep learning can predict the subtypes from genetic information more accurately than conventional statistical methods. However, the previous studies did not directly use deep learning to examine which genes associate with the subtypes. To reveal the mechanisms embedded in the PAM50 subtypes, we developed an explainable deep learning model called a point-wise linear model, which uses meta-learning to generate a custom-made logistic regression for each sample. We developed an explainable deep learning model called a point-wise linear model, which uses meta-learning to generate a custom-made logistic regression for each sample. Logistic regression is familiar to physicians, and we can use it to analyze which genes are important for prediction. The custom-made logistic regression models generated by the point-wise linear model used the specific genes selected in other subtypes compared to the conventional logistic regression model: the overlap ratio is less than twenty percent. Analyzing the point-wise linear model’s inner state, we found that the point-wise linear model used genes relevant to the cell cycle-related pathways."

ent4 =  {"entities":[(117,130,"Disease"),(181,187,"Disease"),(335,341,"Disease")]}

abstract5 = "The Androgen Receptor (AR) is a potential prognostic marker and therapeutic target in breast cancer. We evaluated AR protein expression in high-risk breast cancer treated in the adjuvant setting. Tumors were subtyped into luminal (ER+/PgR±/AR±), molecular apocrine (MAC, [ER−/PgR−/AR+]) and hormone receptor negative carcinomas (HR-negative, [ER−/PgR−/AR−]). Subtyping was evaluated with respect to prognosis and to taxane therapy. High histologic grade (p < 0.001) and increased proliferation (p = 0.001) more often appeared in MAC and HR-negative than in luminal tumors. Patients with MAC had outcome comparable to the luminal group, while patients with HR-negative disease had increased risk for relapse and death. MAC outcome was favorable upon taxane-containing treatment; this remained significant upon multivariate analysis for overall survival (HR 0.31, 95%CI 0.13–0.74, interaction p = 0.035) and as a trend for time to relapse (p = 0.15). In conclusion, AR-related subtyping of breast cancer may be prognostic and serve for selecting optimal treatment combinations."

ent5 = {"entities":[(266,279,"Disease"),(360,367,"Subtype"),(390,393,"Subtype"),(415,420,"Subtype"),(442,446,"Subtype"),(470,489,"Subtype"),(511,514,"Subtype"),(538,543,"Subtype"),(565,571,"Subtype"),(593,596,"Subtype"),(624,660,"Subtype"),(683,694,"Subtype"),(718,723,"Subtype"),(745,751,"Subtype"),(773,778,"Subtype"),(973,976,"Subtype"),(1002,1014,"Subtype"),(1045,1052,"Subtype"),(1098,1101,"Subtype"),(1155,1162,"Subtype"),(1213,1224,"Subtype"),(1298,1301,"Subtype"),(1614,1627,"Disease")]}

abstract6 = "Extracellular vesicles (EVs) are a potential source of disease-associated biomarkers for diagnosis. In breast cancer, comprehensive analyses of EVs could yield robust and reliable subtype-specific biomarkers that are still critically needed to improve diagnostic routines and clinical outcome. Here, we show that proteome profiles of EVs secreted by different breast cancer cell lines are highly indicative of their respective molecular subtypes, even more so than the proteome changes within the cancer cells. Moreover, we detected molecular evidence for subtype-specific biological processes and molecular pathways, hyperphosphorylated receptors and kinases in connection with the disease, and compiled a set of protein signatures that closely reflect the associated clinical pathophysiology. These unique features revealed in our work, replicated in clinical material, collectively demonstrate the potential of secreted EVs to differentiate between breast cancer subtypes and show the prospect of their use as non-invasive liquid biopsies for diagnosis and management of breast cancer patients."

ent6 = {"entities":[(220,233,"Disease"),(498,511,"Disease"),(656,662,"Disease"),(1132,1145,"Disease"),(1277,1290,"Disease")]}

abstract7 = "Many methodologies have been used in research to identify the intrinsic subtypes of breast cancer commonly known as Luminal A, Luminal B, HER2-Enriched (HER2-E) and Basal-like. The PAM50 gene set is often used for gene expression-based subtyping; however, surrogate subtyping using panels of immunohistochemical (IHC) markers are still widely used clinically. Discrepancies between these methods may lead to different treatment decisions. We used the PAM50 RT-qPCR assay to expression profile 814 tumors from the GEICAM/9906 phase III clinical trial that enrolled women with locally advanced primary invasive breast cancer. All samples were scored at a single site by IHC for estrogen receptor (ER), progesterone receptor (PR), and Her2/neu (HER2) protein expression. Equivocal HER2 cases were confirmed by chromogenic in situ hybridization (CISH). Single gene scores by IHC/CISH were compared with RT-qPCR continuous gene expression values and “intrinsic” subtype assignment by the PAM50. High, medium, and low expression for ESR1, PGR, ERBB2, and proliferation were selected using quartile cut-points from the continuous RT-qPCR data across the PAM50 subtype assignments. ESR1, PGR, and ERBB2 gene expression had high agreement with established binary IHC cut-points (area under the curve (AUC) ≥ 0.9). Estrogen receptor positivity by IHC was strongly associated with Luminal (A and B) subtypes (92%), but only 75% of ER negative tumors were classified into the HER2-E and Basal-like subtypes. Luminal A tumors more frequently expressed PR than Luminal B (94% vs 74%) and Luminal A tumors were less likely to have high proliferation (11% vs 77%). Seventy-seven percent (30/39) of ER-/HER2+ tumors by IHC were classified as the HER2-E subtype. Triple negative tumors were mainly comprised of Basal-like (57%) and HER2-E (30%) subtypes. Single gene scoring for ESR1, PGR, and ERBB2 was more prognostic than the corresponding IHC markers as shown in a multivariate analysis. The standard immunohistochemical panel for breast cancer (ER, PR, and HER2) does not adequately identify the PAM50 gene expression subtypes. Although there is high agreement between biomarker scoring by protein immunohistochemistry and gene expression, the gene expression determinations for ESR1 and ERBB2 status was more prognostic."

ent7 = {"entities":[(201,214,"Disease"),(254,263,"Subtype"),(286,295,"Subtype"),(318,331,"Subtype"),(354,360,"Subtype"),(387,397,"Subtype"),(852,865,"Disease"),(1851,1858,"Subtype"),(1901,1912,"Subtype"),(1945,1951,"Subtype"),(1956,1966,"Subtype"),(1977,1986,"Subtype"),(2028,2037,"Subtype"),(2055,2065,"Subtype"),(2163,2166,"Subtype"),(2167,2172,"Subtype"),(0,0,"Subtype"),(2227,2233,"Subtype"),(2314,2324,"Subtype"),(2358,2364,"Subtype"),(1588,1592,"Gene"),(1614,1617,"Gene"),(1639,1644,"Gene"),(1795,1799,"Gene"),(1821,1824,"Gene"),(2548,2552,"Gene"),(2574,2577,"Gene"),(2603,2608,"Gene"),(3013,3017,"Gene"),(3042,3047,"Gene")]}

abstracts = [(abstract1, ent1), (abstract2,ent2), (abstract3, ent3), (abstract4, ent4), (abstract5, ent5), (abstract6, ent6), (abstract7, ent7)]

from annotations import training
from annotations import testing

abstracts = training

model = None
output_dir=Path("output/")
n_iter=100

#load the model

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')
    print("Created blank 'en' model")

if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in abstracts:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])
example = []
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(abstracts)
        losses = {}
        for text, annotations in tqdm(abstracts):
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update(
                [example],
                drop=0.5,
                sgd=optimizer,
                losses=losses)
        print(losses)
if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)
pickle.dump(nlp, open( "education nlp.pkl", "wb" ))

for temp in testing:
    print(temp[0])
    print("-----")
    print(temp[1])
    print("-----")

    doc=nlp(temp[0])
    for ent in doc.ents:
        print(ent.label_+ '  ------>   ' + ent.text)
    print()
    print("-----")
    print()
