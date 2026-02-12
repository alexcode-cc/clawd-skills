---
name: lobster-use
description: |
  Analyze biological data using Lobster AI — single-cell RNA-seq, bulk RNA-seq,
  literature mining, dataset discovery, quality control, and visualization.
  
  USE THIS SKILL WHEN:
  - Analyzing single-cell or bulk RNA-seq data
  - Searching PubMed/GEO for papers or datasets
  - Running quality control on biological data
  - Clustering cells, finding markers, differential expression
  - Creating publication-quality visualizations
  - Working with H5AD, CSV, 10X, GEO/SRA accessions
  
  TRIGGER PHRASES: "analyze cells", "search PubMed", "download GEO", "run QC",
  "cluster", "find markers", "differential expression", "UMAP", "volcano plot",
  "single-cell", "RNA-seq", "bioinformatics"
  
  ASSUMES: Lobster is installed and configured. For setup issues, tell user to
  run `lobster config-test` and fix any errors before proceeding.
---

# Lobster AI Usage Guide

Lobster AI is a multi-agent bioinformatics platform. You interact via natural language
or slash commands — Lobster routes to specialist agents automatically.

## Quick Reference

| Task | Reference |
|------|-----------|
| **CLI commands** | [references/cli-commands.md](references/cli-commands.md) |
| **Single-cell analysis** | [references/single-cell-workflow.md](references/single-cell-workflow.md) |
| **Bulk RNA-seq analysis** | [references/bulk-rnaseq-workflow.md](references/bulk-rnaseq-workflow.md) |
| **Literature & datasets** | [references/research-workflow.md](references/research-workflow.md) |
| **Visualization** | [references/visualization.md](references/visualization.md) |
| **Available agents** | [references/agents.md](references/agents.md) |

## Interaction Modes

### Interactive Chat
```bash
lobster chat                          # Start interactive session
lobster chat --workspace ./myproject  # Custom workspace
lobster chat --reasoning              # Enable detailed reasoning
```

### Single Query
```bash
lobster query "Your request"
lobster query --session-id latest "Follow-up request"
```

## Core Patterns

### Natural Language (Primary)
Just describe what you want:
```
"Download GSE109564 and run quality control"
"Cluster the cells and find marker genes"
"Compare hepatocytes vs stellate cells"
```

### Slash Commands (System Operations)
```
/data                    # Show loaded data info
/files                   # List workspace files
/workspace list          # List available datasets
/workspace load 1        # Load dataset by index
/plots                   # Show generated visualizations
/save                    # Save current session
/status                  # Show system status
/help                    # All commands
```

### Session Continuity
```bash
# Start named session
lobster query --session-id "my_analysis" "Load GSE109564"

# Continue with context
lobster query --session-id latest "Now cluster the cells"
lobster query --session-id latest "Find markers for cluster 3"
```

## Agent System

Lobster routes to specialist agents automatically:

| Agent | Handles |
|-------|---------|
| **Supervisor** | Routes queries, coordinates agents |
| **Research Agent** | PubMed search, GEO discovery, paper extraction |
| **Data Expert** | File loading, format conversion, downloads |
| **Transcriptomics Expert** | scRNA-seq: QC, clustering, markers |
| **DE Analysis Expert** | Differential expression, statistical testing |
| **Annotation Expert** | Cell type annotation, gene set enrichment |
| **Visualization Expert** | UMAP, heatmaps, volcano plots |
| **Proteomics Expert** | Mass spec analysis [premium] |
| **Genomics Expert** | VCF, GWAS, variant analysis [premium] |
| **ML Expert** | Embeddings, classification [premium] |

## Workspace & Outputs

**Default workspace**: `.lobster_workspace/`

**Output files**:
| Extension | Content |
|-----------|---------|
| `.h5ad` | Processed AnnData objects |
| `.html` | Interactive visualizations |
| `.png` | Publication-ready plots |
| `.csv` | Exported tables |
| `.json` | Metadata, provenance |

**Managing outputs**:
```
/files              # List all outputs
/plots              # View visualizations
/open results.html  # Open in browser
/read summary.csv   # Preview file contents
```

## Typical Workflow

```bash
# 1. Start session
lobster chat --workspace ./my_analysis

# 2. Load or download data
"Download GSE109564 from GEO"
# or
/workspace load my_data.h5ad

# 3. Quality control
"Run quality control and show me the metrics"

# 4. Analysis
"Filter low-quality cells, normalize, and cluster"

# 5. Interpretation
"Identify cell types and find marker genes"

# 6. Visualization
"Create UMAP colored by cell type"
/plots

# 7. Export
"Export marker genes to CSV"
/save
```

## Troubleshooting Quick Reference

| Issue | Check |
|-------|-------|
| Lobster not responding | `lobster config-test` |
| No data loaded | `/data` to verify, `/workspace list` to see available |
| Analysis fails | Try with `--reasoning` flag |
| Missing outputs | Check `/files` and workspace directory |

## Documentation

Online docs: **docs.omics-os.com**

Key sections:
- Guides → CLI Commands
- Guides → Data Analysis Workflows
- Tutorials → Single-Cell RNA-seq
- Agents → Package documentation
