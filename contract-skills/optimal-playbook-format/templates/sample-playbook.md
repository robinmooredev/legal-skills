# [Company Name] Contract Review Playbook

**Version:** 1.0
**Last updated:** [date]
**Contract types covered:** Vendor agreements, NDAs, Contractor agreements

## Introduction

This playbook defines [Company Name]'s review criteria for the contracts our team handles most frequently. Use it with the Review Contract with Playbook skill to review any new agreement. Each entry describes what to look for and provides draft language to use when pushing back.

---

## Vendor Agreements

### Auto Renewal

**key:** `auto_renewal`
**Expected:** should_be_absent

**What to look for:**
Check whether the contract automatically renews at the end of the initial term. Look for language like "shall automatically renew," "successive renewal terms," or "unless either party provides written notice of non-renewal." Auto-renewal clauses are typically in the Term section. Also check the order form — it may override the MSA's renewal terms.

**Suggested language:**
"Notwithstanding anything to the contrary in the Agreement, this Agreement shall not automatically renew. Any renewal shall require mutual written agreement of both parties."

---

## NDAs

### Non-Solicitation

**key:** `non_solicitation`
**Expected:** should_be_absent

**What to look for:**
Check whether the NDA includes a non-solicitation or non-hire clause that restricts either party from soliciting or hiring the other's employees. These are sometimes buried in "Additional Obligations" or "Restrictive Covenants" and may extend beyond the confidentiality term. Non-solicitation in a pre-sales NDA is unusual and disproportionate.

**Suggested language:**
"Nothing in this Agreement shall restrict either party from soliciting, hiring, or engaging any employee or contractor of the other party."

---

## Contractor Agreements

### IP Assignment

**key:** `ip_assignment`
**Expected:** should_be_present

**What to look for:**
Confirm the agreement includes a clear assignment of all intellectual property created during the engagement to the company. Look for "work made for hire" language and a present-tense assignment ("hereby assigns") covering inventions, copyrights, and other IP. Watch for carve-outs that are overly broad — the contractor should retain rights to pre-existing IP, but everything created for the engagement should be assigned.

**Suggested language:**
"Contractor hereby irrevocably assigns to Company all right, title, and interest in and to all Work Product, including all intellectual property rights therein. 'Work Product' means all inventions, works of authorship, designs, code, and other materials created by Contractor in the course of performing services under this Agreement. Contractor retains all rights to Contractor's pre-existing intellectual property, and grants Company a non-exclusive, perpetual license to use such pre-existing IP solely as incorporated in the Work Product."
