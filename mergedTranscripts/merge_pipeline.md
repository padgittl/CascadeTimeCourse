# Merge transcript assemblies with cuffmerge
```bash
cuffmerge -g hopCascadeAugustusGeneModels.gff -s genome.fasta -p 8 -o mergedAssembliesWithRef samplelist.txt
```

# Retrieve transcript sequences with gffread
```bash
gffread mergedAssembliesWithRef/merged.gtf -g genome.fasta -w mergedTranscripts.fasta
```

# Convert GTF to GFF with gffread
```bash
gffread -E mergedAssemblies/merged.gtf -o- > mergedTranscripts.gff
```

# Create GFF and FASTA containing only the longest transcripts per gene
```bash
python getLongestTranscriptPerGene.py mergedTranscripts.fasta mergedTranscripts.gff withRef
```
