# SaaS Vendor Negotiation Playbook

This playbook defines the standard positions for evaluating SaaS vendor contracts. Each entry specifies what to look for, whether it should be present or absent, and how to assess it.

## How to Use

For each entry:
- **expected: should_be_present** — The provision should exist in the vendor's documents. If found → pass. If absent → fail.
- **expected: should_be_absent** — The provision should NOT exist. If found → fail. If absent → pass.
- If partially addressed or ambiguous → review.

---

## Playbook Entries

### 1. Auto Renewal
- **key:** `auto_renewal`
- **expected:** `should_be_absent`
- **instruction:** The subscription or agreement should not automatically renew without clear notice and the ability to opt out. Look for language like "shall automatically renew," "will renew for successive periods," or "unless written notice of non-renewal is provided X days prior." Auto-renewal is unfavorable because it locks the customer into continued payment without active consent.

### 2. Liability Cap Adequacy
- **key:** `liability_cap_too_low`
- **expected:** `should_be_absent`
- **instruction:** Vendor's total liability must not be capped below 12 months of fees paid. Caps based on shorter periods (e.g., "fees paid in the prior month") or nominal amounts (e.g., "$100") are unacceptable. Look for language like "shall not exceed," "limited to," or "liability capped at." Acceptable range: 6-24 months of fees. Escalation trigger: uncapped liability or consequential damages inclusion.

### 3. Customer Logo / Trademark Use
- **key:** `vendor_logo_use_rights`
- **expected:** `should_be_absent`
- **instruction:** Vendor must not have the explicit, stated right to use Customer's name, logo, or trademarks for marketing, case studies, or press without Customer's prior written consent. Blanket grants buried in the ToS (e.g., "Customer grants Vendor the right to identify Customer as a user of the Services") are common and should be flagged. Acceptable: agreements that don't mention any right to use the customer's name or logo.

---

## Customization

To adapt this playbook for your organization:

- **Change thresholds**: e.g., require 24-month liability caps instead of 12
- **Add entries**: e.g., HIPAA BAA requirements, IP indemnification, data deletion guarantees, price escalation caps, unilateral modification rights, AI training restrictions
- **Remove entries**: e.g., if auto-renewal is acceptable to your company

Each entry follows the format:
```
### Title
- **key:** unique_identifier
- **expected:** should_be_present | should_be_absent
- **instruction:** What to look for and how to assess it
```
