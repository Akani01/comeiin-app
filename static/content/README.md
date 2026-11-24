# Comeiin Works catalogue and image records

Source: Copy of Comeiin Works Product Review.xlsx, read without changing the original.

Selection: include client-approved Launch first rows and any additional non-removed rows with client-added technical details or images. Existing description, Request quote, On request and inherited Website reference links do not count as new client detail. No additional non-launch rows meet that criterion. Remove takes precedence over Launch first (CW-016); CW-027 is also removed. CW-032 Laboratory Safety Gear remains because the client separately approved it.

21 source groups produce 22 catalogue entries. CW-001-SLIDES is derived from J6/K6 and kept separate from microscopes. CW-017, CW-023 and CW-033 use the product details supplied within their original group rows. Original names, listing types and exact values remain in review-source.json. Categories are navigation groupings assigned during implementation, not client-supplied classifications. No prices, brands, model numbers or missing technical specifications are invented.

The embedded image spans P37:P39 but visually shows a fridge/freezer thermometer. It is associated with CW-033 (row 38) based on its subject. It is client supplied; the workbook does not separately record final image approval.

image-register.json records each catalogue image's stable ID, file, origin, source row, version, dimensions, SHA-256, prompt, generation date and approval fields. generated-images.json preserves full prompts and original generation paths. Blank approval fields mean approval has not been recorded. The browser review is image-register.html; it is a review display, not an approval database.

Existing mismatched links are replaced: CW-029 previously used syringes; CW-030 used collection tubes; CW-031 used mixers; CW-033 used balances; CW-034 used plasticware. CW-023 receives a swab-specific illustration. CW-001-SLIDES gets its own illustration. Similar client-approved groups retain distinct references even where they share a source mockup.

For image replacements, retain the previous file, create a v2 filename, update the catalogue path and append the prior record to image-history.json before regenerating the register. Keep generation prompts with the version they created. Never mark an image approved merely because it was generated or placed on the site.

Product images are illustrative except the client photo. Final specifications, models, pricing and availability still require confirmation. Source review notes and image approval details are kept out of the customer catalogue.

The quote list lasts for the current browser session and includes capacity choices and box quantities. Email submission opens a draft; it does not send an enquiry automatically. This remains a local preview with indexing disabled.

Dynamic catalogue update: expandable category navigation, combined category/search/listing-type filters, alphabetical sorting and removable filter chips. Filter state is encoded in the catalogue URL. Quick view retains specifications and capacity selection. The quote drawer confirms additions and supports continuing browsing. Related items use explicit companion links first, then the same category. Subtle product reveals, hover transitions and panel animations respect reduced-motion preferences. No additional product, stock, pricing or image claims were introduced.


Approved catalogue batch 01 (15 November 2026): 20 images now serve 17 individual
listings, including 15 new entries and two replacements. The browser catalogue
now has 37 entries. See docs/product-images/batch-01.txt for provenance, mapping,
checks and the focused database import command. Batch images are approved;
approval statuses for other images remain unchanged. catalogue.json is now the
current source for the generated js/catalogue.js; run scripts/build_catalogue.py
after changes. Additional views belong to individual products, not new SKUs.

Approved catalogue batch 02 (15 November 2026): 20 approved images serve 20 new
individual listings, bringing the catalogue to 57 entries. All 37 earlier entries
remain unchanged. See docs/product-images/batch-02.txt for source details,
image audit limitations, validation and deployment commands. The focused import
now accepts batches 1 and 2; the initial seed applies both. Batches 03-06 still
await client review. Approval of the displayed images does not verify unreadable
fine print; listing specifications come from the catalogue text and layout.
