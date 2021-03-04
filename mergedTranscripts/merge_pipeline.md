# Merge transcript assemblies with cuffmerge
```bash
cuffmerge -g denovoHopCascadeTranscripts.gff -s genome.fasta -p 8 -o allDenovoTranscriptGuidedAssembly samplelist.txt
```

# Retrieve transcript sequences with gffread
```bash
gffread allDenovoTranscriptGuidedAssembly/merged.gtf -g genome.fasta -w mergedTranscripts.fasta
```

# Convert GTF to GFF with gffread
```bash
gffread -E allDenovoTranscriptGuidedAssembly/merged.gtf -o- > mergedTranscripts.gff
```

