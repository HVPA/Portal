################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Revision: $Rev: 236 $
# Last Modified: $Date: 2010-08-02 13:49:10 +1000 (Mon, 02 Aug 2010) $ 
#
# === Description ===
#
#
################################################################################


from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Portal.hvp.models.search.Gene import Gene
from Portal.hvp.models.search.Variant import Variant
from Portal.search.parser import variant_parser
from Portal.search.parser import variant_validator
from Portal import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse

# Biopython
from Bio import SeqIO


import json


def getGenbank(gene):
    genbankFile = open("genbank_files/" + gene.GenBankName + "." + gene.GenBankVer + ".gb")
    genRecord = SeqIO.read(genbankFile, "genbank")
    genbankFile.close()

    return genRecord

def getRefseq(gene):
    refseqFile = open("genbank_files/" + gene.RefSeqName + "." + gene.RefSeqVer + ".gb")
    refRecord = SeqIO.read(refseqFile, "genbank")
    refseqFile.close()

    return refRecord

def getFeatures(genRecord, refRecord):
    geneRange = {}
    exons = []
    counter = 0
    for genFeature in genRecord.features:
        if genFeature.type == 'exon':
            number = genFeature.qualifiers["number"][0]
            refStart = 0
            refEnd = 0
            for refFeature in refRecord.features:
                if refFeature.type == 'exon' and refFeature.qualifiers["number"][0] == number:
                    refStart = int(refFeature.location.start.position)
                    refEnd = int(refFeature.location.end.position)

            exon = { 
                'genStart': int(genFeature.location.start.position) + 1, 
                'genEnd': int(genFeature.location.end.position) + 1,
                'refStart': refStart + 1,
                'refEnd': refEnd + 1,
                'counter': counter,
                'number': number }
            exons.append(exon)
            counter += 1

        elif genFeature.type == 'source':
            geneRange['genStart'] = int(genFeature.location.start.position) + 1
            geneRange['genEnd'] = int(genFeature.location.end.position)

    for refFeature in refRecord.features:
        if refFeature.type == 'source':
            geneRange['refStart'] = int(refFeature.location.start.position) + 1
            geneRange['refEnd'] = int(refFeature.location.end.position) + 1
            break

    return geneRange, exons

def getProtein(refRecord):
    protein = ""
    for feature in refRecord.features:
        if feature.type == 'CDS':
            if feature.qualifiers.has_key("translation"):
                protein = feature.qualifiers["translation"][0]


def getGenIndexFromRef(exons, pos, intron):
    pos = 0 if pos == '' else int(pos)
    intron = 0 if intron == '' else int(intron)

    result = 0

    # Test for position - 1 because biopython starts counting from zero
    posIndex = pos

    for exon in exons:
        if posIndex >= exon["refStart"] and posIndex <= exon["refEnd"]:
            indexFromRefExon = pos - exon["refStart"]
            result = exon["genStart"] + indexFromRefExon
            result += intron
            break

    return result


def applyRefIntronNotation(pos, intron):
    pos = 0 if pos == '' else int(pos)
    intron = 0 if intron == '' else int(intron)

    result = str(pos)
    if intron != 0:
        if intron > 0:
            result += '+'
        result += str(intron)

    return result




def gene_structure_view(request, geneID):
    if request.user.is_authenticated():
        gene = get_object_or_404(Gene, pk = geneID)

        genRecord = getGenbank(gene)
        refRecord = getRefseq(gene)
        geneRange, exons = getFeatures(genRecord, refRecord)
        protein = getProtein(refRecord)

        json_content = json.dumps({ 
            'GeneID': gene.ID,
            'GeneName': gene.GeneName,
            'Sequence': genRecord.seq.data,
            'Protein': protein,
            'GeneRange': geneRange,
            'Exons': exons })
 
        return HttpResponse(json_content, mimetype='application/javascript')
    else:
        return render_to_response('home/timeout.html')


def variant_list_view(request, geneID):
    if request.user.is_authenticated():
        gene = get_object_or_404(Gene, pk = geneID)

        genRecord = getGenbank(gene)
        refRecord = getRefseq(gene)
        geneRange, exons = getFeatures(genRecord, refRecord)

        results = Variant.objects.filter(Gene=gene)

        varList = []
        for var in results:
            genIndex = 0
            refIndex = 0
            genStart = 0
            genEnd = 0
            refStart = 0
            refEnd = 0

            # TODO: Hacks! Should really look at why there are negative positions like c.-19-10C>T in BRCA1 -- Alan 13-11-2010
            # NB: The validator has been updated to handle variants with negatives like c.-19-10c>t
            # TODO: Not sure whats suppose to happen if validation fails, need to replace continue -- Melvin 20/04/2011
            #if variant_parser.variant_validation(var.cDNA) == False:
            variantValidator = variant_validator.VariantValidator()
            if variantValidator.variant_validation(var.cDNA) == False:
                continue

            variant = variant_parser.parse_as_class(var.cDNA)
            
            if not variant.isRange():
                genIndex = getGenIndexFromRef(exons, variant.position, variant.position_intron)
                refIndex = applyRefIntronNotation(variant.position, variant.position_intron)
            else:
                genStart = getGenIndexFromRef(exons, variant.range_lower, variant.range_lower_intron)
                genEnd = getGenIndexFromRef(exons, variant.range_upper, variant.range_upper_intron)
                refStart = applyRefIntronNotation(variant.range_lower, variant.range_lower_intron)
                refEnd = applyRefIntronNotation(variant.range_upper, variant.range_upper_intron)

            newVar = {
                'genIndex': genIndex,
                'refIndex': refIndex,
                'genStart': genStart,
                'genEnd': genEnd,
                'refStart': refStart,
                'refEnd': refEnd,
                'isRange': variant.isRange(),
                'change_type': variant.change_type,
                'cDNA': var.cDNA }

            varList.append(newVar)

        json_content = json.dumps({
            'varList': varList,
            'count': len(varList) })

        return HttpResponse(json_content, mimetype='application/javascript')
    else:
        return render_to_response('home/timeout.html')



