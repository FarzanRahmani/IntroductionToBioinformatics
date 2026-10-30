# Introduction to Bioinformatics

Homework, classroom algorithms, and project material from the first semester of my M.Sc. in Computer Engineering at Sharif University of Technology, taught by Dr. Ali Sharifi-Zarchi. Author: Farzan Rahmani.

The repository spans sequence algorithms, sequencing-file analysis, statistical tests, locality-sensitive hashing, and biological-data analysis.

## Repository Guide

| Path | Contents |
| --- | --- |
| `class_works/1/` | Origin-of-replication finder notebook |
| `class_works/2/` | Shift-Or, trie matching, and suffix-array matching examples |
| `HWs/HW1/` | Sequence/alignment scripts and written work |
| `HWs/HW2/` | Sequencing-file analysis notebooks and algorithm exercises |
| `HWs/HW3/` | Statistical-testing notebooks and submission |
| `HWs/HW4/` | LSH exercises, an AlphaFold2 notebook, and other practical material |
| `project/` | Dataset-specific notebooks, combined analysis, paper material, reports, and presentation slides |
| `exam/`, `sample_exams/`, `quizes/` | Exam and quiz resources |

## Project Material

`project/codes/` includes notebooks named after GEO accessions such as `GSE3807`, `GSE29105`, `GSE28974`, `GSE165870`, and `GSE113033`, alongside a merged-five-dataset analysis and a paper-implementation notebook. Start with the project report and `project/links.txt` for context and original sources, then inspect the appropriate notebook.

## Using the Code

Use Python for standalone algorithm scripts and Jupyter or Google Colab for notebooks. There is no single dependency lockfile or repository-wide entry point. Check the imports, installation cells, and kernel metadata in the selected notebook, including any non-Python analysis steps.

1. Read the corresponding assignment or project report.
2. Confirm sequence formats, vertex/index conventions, scoring parameters, or statistical assumptions relevant to that exercise.
3. Obtain external sequencing files, GEO data, or model resources when required, and configure the notebook's input paths.
4. Run cells in order and interpret results using the accompanying written analysis.

Small algorithm scripts can usually be studied without the larger datasets. AlphaFold-related and other compute-heavy notebooks have separate runtime and hardware requirements. Historical outputs and example implementations should be checked independently before reuse.

## License

See [LICENSE](LICENSE) for repository license terms. Papers, datasets, and supplied teaching material retain their original terms and attribution.
