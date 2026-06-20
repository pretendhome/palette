#!/usr/bin/env python3
"""
Tax Document Extractor — reads PDFs from the Sup folder and produces
a filing guide: exactly what numbers go in which boxes.

Output goes to TAX_FILING_GUIDE_2025.md in the same folder.
All PII stays local — nothing leaves this machine.
"""

import re
import os
import subprocess
from pathlib import Path

SUP = Path.home() / "Desktop" / "Sup"
OUT = SUP / "TAX_FILING_GUIDE_2025.md"


def extract_text(pdf_path: Path) -> str:
    """Extract text from PDF using pdftotext (most reliable for IRS forms)."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout
    except Exception:
        return ""


def extract_w2_fields(text: str, label: str) -> dict:
    """Try to extract W-2 box values from text."""
    fields = {}

    # Common W-2 patterns
    patterns = {
        "employer_name": r"(?:employer.s name|employer name)[:\s]*([^\n]+)",
        "employee_name": r"(?:employee.s name|employee name)[:\s]*([^\n]+)",
        "box1_wages": r"(?:box\s*1|wages.?\s*tips|federal wages)[:\s]*\$?([\d,]+\.?\d*)",
        "box2_fed_withheld": r"(?:box\s*2|federal.*(?:tax|income).*withheld|fed.*withheld)[:\s]*\$?([\d,]+\.?\d*)",
        "box3_ss_wages": r"(?:box\s*3|social security wages)[:\s]*\$?([\d,]+\.?\d*)",
        "box4_ss_withheld": r"(?:box\s*4|social security.*withheld)[:\s]*\$?([\d,]+\.?\d*)",
        "box5_medicare_wages": r"(?:box\s*5|medicare wages)[:\s]*\$?([\d,]+\.?\d*)",
        "box6_medicare_withheld": r"(?:box\s*6|medicare.*withheld)[:\s]*\$?([\d,]+\.?\d*)",
        "box16_state_wages": r"(?:box\s*16|state wages)[:\s]*\$?([\d,]+\.?\d*)",
        "box17_state_tax": r"(?:box\s*17|state.*(?:tax|income).*withheld|state tax)[:\s]*\$?([\d,]+\.?\d*)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[key] = match.group(1).strip()

    # Also try to find dollar amounts in sequence (W-2s often have amounts in order)
    amounts = re.findall(r"\$?([\d]{1,3}(?:,\d{3})*\.\d{2})", text)
    if amounts and not fields.get("box1_wages"):
        fields["all_amounts_found"] = amounts

    return fields


def extract_transcript_info(text: str) -> dict:
    """Extract key info from IRS transcript."""
    info = {}

    # Look for income items
    income_patterns = [
        (r"wages.*?\$?([\d,]+\.?\d*)", "wages"),
        (r"interest.*?\$?([\d,]+\.?\d*)", "interest_income"),
        (r"dividend.*?\$?([\d,]+\.?\d*)", "dividend_income"),
        (r"adjusted gross income.*?\$?([\d,]+\.?\d*)", "agi"),
        (r"taxable income.*?\$?([\d,]+\.?\d*)", "taxable_income"),
        (r"total tax.*?\$?([\d,]+\.?\d*)", "total_tax"),
        (r"(?:refund|overpayment).*?\$?([\d,]+\.?\d*)", "refund"),
        (r"(?:amount owed|balance due).*?\$?([\d,]+\.?\d*)", "balance_due"),
    ]

    for pattern, key in income_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info[key] = match.group(1).strip()

    return info


def extract_prior_return(text: str) -> dict:
    """Extract key numbers from prior year return."""
    info = {}
    patterns = [
        (r"(?:line\s*11|adjusted gross income).*?\$?([\d,]+\.?\d*)", "agi"),
        (r"(?:line\s*15|total tax).*?\$?([\d,]+\.?\d*)", "total_tax"),
        (r"(?:line\s*24|total tax).*?\$?([\d,]+\.?\d*)", "total_tax_alt"),
        (r"(?:filing status).*?(\d)", "filing_status"),
        (r"(?:standard deduction|itemized).*?\$?([\d,]+\.?\d*)", "deduction"),
        (r"(?:refund|overpaid).*?\$?([\d,]+\.?\d*)", "refund"),
    ]
    for pattern, key in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info[key] = match.group(1).strip()
    return info


def main():
    md = []
    md.append("# 2025 Tax Filing Guide — Neill Family")
    md.append(f"\n**Generated**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md.append("**Status**: EXTRACT AND VERIFY — check every number against your paper documents")
    md.append("**⚠️ FILE TODAY** — you are 1 day past the April 15 deadline\n")
    md.append("---\n")

    # ── W-2s ──────────────────────────────────────────────────────────────
    md.append("## W-2 Income\n")
    md.append("Enter these into FreeTaxUSA under **Income → W-2**\n")

    w2_files = [
        ("Mical W-2 (1)", "neill-2025-w2.pdf"),
        ("Mical W-2 (2)", "W-2_Employee_Copies_20260325093013.pdf"),
        ("Claudia W-2", "Claudia_Canu_2025_W2 (1).pdf"),
    ]

    for label, filename in w2_files:
        path = SUP / filename
        if not path.exists():
            md.append(f"### {label}\n⚠️ File not found: {filename}\n")
            continue

        text = extract_text(path)
        fields = extract_w2_fields(text, label)

        md.append(f"### {label}")
        md.append(f"*Source: {filename}*\n")

        if fields.get("employer_name"):
            md.append(f"**Employer**: {fields['employer_name']}")
        if fields.get("employee_name"):
            md.append(f"**Employee**: {fields['employee_name']}")

        md.append("")
        md.append("| Box | Description | Value | FreeTaxUSA Field |")
        md.append("|-----|-------------|-------|-----------------|")

        box_map = [
            ("1", "Wages, tips, other compensation", "box1_wages", "Wages"),
            ("2", "Federal income tax withheld", "box2_fed_withheld", "Federal tax withheld"),
            ("3", "Social Security wages", "box3_ss_wages", "SS wages"),
            ("4", "Social Security tax withheld", "box4_ss_withheld", "SS tax withheld"),
            ("5", "Medicare wages and tips", "box5_medicare_wages", "Medicare wages"),
            ("6", "Medicare tax withheld", "box6_medicare_withheld", "Medicare tax withheld"),
            ("16", "State wages", "box16_state_wages", "State wages"),
            ("17", "State income tax", "box17_state_tax", "State tax withheld"),
        ]

        for box, desc, key, ftusa in box_map:
            val = fields.get(key, "⚠️ CHECK PDF")
            md.append(f"| {box} | {desc} | {val} | {ftusa} |")

        if fields.get("all_amounts_found"):
            md.append(f"\n*All dollar amounts found in document (verify order): {', '.join(fields['all_amounts_found'][:12])}*")

        md.append("\n**RAW TEXT (first 2000 chars — use to verify):**")
        md.append(f"```\n{text[:2000].strip()}\n```\n")

    # ── Wage & Income Transcript 2025 ─────────────────────────────────────
    md.append("---\n## IRS Wage & Income Transcript 2025\n")
    md.append("**This shows everything the IRS knows about your 2025 income.**")
    md.append("Compare every item here to your W-2s. If there are 1099s listed that you don't have, you still need to report them.\n")

    wit_path = SUP / "wage-and-income-2025.pdf"
    if wit_path.exists():
        text = extract_text(wit_path)
        md.append(f"```\n{text[:4000].strip()}\n```\n")
    else:
        md.append("⚠️ File not found\n")

    # ── 2025 Account Transcript ───────────────────────────────────────────
    md.append("---\n## IRS Account Transcript 2025\n")
    md.append("Shows if you have any balance due, payments made, or credits applied.\n")

    at_path = SUP / "2025-trascript.pdf"
    if at_path.exists():
        text = extract_text(at_path)
        info = extract_transcript_info(text)
        if info:
            for k, v in info.items():
                md.append(f"- **{k.replace('_', ' ').title()}**: ${v}")
        md.append(f"\n```\n{text[:3000].strip()}\n```\n")

    # ── Prior Year Return (2024) ──────────────────────────────────────────
    md.append("---\n## 2024 Return (for AGI and comparison)\n")
    md.append("You need your **2024 AGI (Line 11)** to e-file your 2025 return.\n")

    ret_path = SUP / "return-2024.pdf"
    if ret_path.exists():
        text = extract_text(ret_path)
        info = extract_prior_return(text)
        if info:
            for k, v in info.items():
                md.append(f"- **{k.replace('_', ' ').title()}**: {v}")
        md.append(f"\n```\n{text[:3000].strip()}\n```\n")

    # ── 1095-C ────────────────────────────────────────────────────────────
    md.append("---\n## Health Insurance (1095-C)\n")
    md.append("You do NOT need to enter this on your return. Just confirm you had coverage all 12 months.\n")

    hc_path = SUP / "Health Insurance Offer And Coverage Form 1095-C (1).pdf"
    if hc_path.exists():
        text = extract_text(hc_path)
        md.append(f"```\n{text[:1500].strip()}\n```\n")

    # ── Filing Instructions ───────────────────────────────────────────────
    md.append("---\n## FreeTaxUSA Step-by-Step\n")
    md.append("""
1. Go to **freetaxusa.com** → Start 2025 Return
2. **Filing Status**: Married Filing Jointly
3. **Personal Info**: Enter your and Claudia's names, SSNs, DOBs
4. **Dependents**: Add Rafael and Nora (names, SSNs, DOBs, relationship: son/daughter)
5. **Income → W-2**: Enter each W-2 above (boxes 1-17)
6. **Income → 1099s**: Check the wage-and-income transcript above for any 1099s
7. **Deductions**: Choose Standard Deduction ($30,000 for MFJ 2025)
8. **Credits → Child Tax Credit**: Should auto-calculate ($2,000 × 2 = $4,000)
9. **Credits → Child Care**: Enter La Scuola expenses if applicable (need school EIN + amount paid for care)
10. **Review**: Compare total tax and refund/owed to your 2024 return
11. **E-file**: Enter 2024 AGI from above for identity verification
12. **Pay/Refund**: Direct deposit or payment info
13. **California**: Add CA return ($14.99) — auto-extends to Oct 15 but pay any amount owed now

**IMPORTANT**: Verify every number in this guide against your actual PDF documents. This extraction is automated and may have errors.
""")

    # ── Write output ──────────────────────────────────────────────────────
    OUT.write_text("\n".join(md))
    print(f"✅ Filing guide written to: {OUT}")
    print(f"   {len(md)} lines")


if __name__ == "__main__":
    main()
