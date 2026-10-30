# Resume

`sriram.yaml` is the single source of truth for the resume. Edit it, never the PDF.
`Damotharan-Sriram-Product-Designer.pdf` is generated from it and is kept in the repo as the public resume.

## Rebuild

```sh
./resume/build.sh
```

This renders the PDF with [RenderCV](https://docs.rendercv.com) and then runs `tools/check_resume_pdf.py` on it. A FAIL from the checker stops the build; a WARN does not.

To also see keyword coverage against a job description:

```sh
./resume/build.sh --jd path/to/job-description.md
```

### Requirements

- RenderCV 2.x, which needs Python 3.12 or newer. Any of these works:
  `uv tool install "rendercv[full]"`, `pipx install "rendercv[full]"`, or `python3.12 -m pip install "rendercv[full]"`.
  If none is installed but `uv` is, the script runs RenderCV through `uvx`.
- `pypdf` for the checker (`pdfplumber` is optional). If they are missing and `uv` is installed, the script fetches them for the run.
- Set `PYTHON=/path/to/python3.12` if the default `python3` is older.
- The first render downloads one Typst package (fontawesome) from packages.typst.org and caches it.

RenderCV writes an intermediate Typst file to `resume/rendercv_output/`, which is git-ignored.

## Editing rules

- Facts come only from `profile/designer-profile.md`, `profile/01-profile-and-icp.md` and the previous resume. Do not add anything else.
- Open questions are marked with comments in the YAML. The Turinglabs title is one: LinkedIn says "Product Designer", the old resume says "Senior Product Designer". It appears in one place only.
- Write year-only dates as bare numbers (`2014`), not quoted strings, or RenderCV prints them as "Jan 2014".
- Keep the layout single-column with company, title, dates and location on one line. Run the checker after any layout change.

## Checker

```sh
python3 tools/check_resume_pdf.py resume.pdf [--jd jd.txt] [--dump]
```

It reads the PDF's text layer the way an ATS does and reports PASS, WARN or FAIL for: broken words (such as "M otion" or "201 9") with a garbled-text percentage, contact details as plain text, section headings, date formats, and, with `--jd`, the job's keywords found and missing in the resume. `--dump` prints the extracted text. It makes no network calls.
