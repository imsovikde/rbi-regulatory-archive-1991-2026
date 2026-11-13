---
doc_id: "Circulars_2009_RBI_2008-2009_499_DPSS_CO_RTGS_No_2246_04_04_002_2008_-_2009"
title: "RTGS Transactions"
category: "Circulars"
year: 2009
source_rbi_url: "https://rbidocs.rbi.org.in/rdocs/Notification/PDFs/RTGS160609.PDF"
pdf_sha256: "b103c2f77fb4be507617a7a30c5beee8932107e41b9786409f1d4de7ef3ac32d"
md_sha256: "6df1c1cd55c831d2ca7d42f9213aa4fdd032e73ba536ea8712fa1d21a7e8fae5"
total_pages: 2
native_pages: 2
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T08:10:20Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Circulars/2009/2009-06-16_Circular_RBI-2008-2009-499%20DPSS%20%28CO%29%20RTGS%20No.%202246%20-%2004.04.002%20-%202008%20-%202009_RTGS%20Transactions.pdf"
verification_status: "VERIFIED_LEVEL_5"
---
# RTGS Transactions

<!-- PAGE 1 -->

RBI/2008-09/499

DPSS (CO) RTGS No. 2246 / 04.04.002 / 2008 - 2009 June 16, 2009

Chairman and Managing Director / Chief Executive Officer of all banks participating in RTGS

Madam / Dear Sir,

|format in a standardized|RTGS Transactions As per the RTGS Business Guidelines, funds that cannot be credited to the account of the beneficiary for some reason or other, has to be sent back to the sender’s account within one hour and thirty minutes. At present, an RTGS customer transaction that is returned to the originating bank, is treated as an inter bank transaction. Thus, an R 41 message format, when returned, comes back to the originating bank as an R 42 message format. The R 42 message format is however intended for fresh interbank transactions and therefore has no specific field tag to incorporate return details. As a result, RTGS participants while returning a customer transaction, provide the return information in the optional field tags of R 42 message format in their own way and there is no uniformity in providing return information. Due to lack of homogeneity in providing information in the return messages, the originating bank finds it difficult to trace the original debit and hence the process of crediting back funds to the account of the sender is delayed. In order to address the problem, at a recent meeting with major RTGS user banks, the return process followed by various banks was reviewed. Based on these discussions, it has been decided to standardize the process as under: All RTGS participants, henceforth, will provide the return information in the R 42 message manner in the field tag 7495 as follows: Withdrawn with effect from February 18, 2022|
|---|---|
|Field tag|Line number Details to be provided Line 1 RETURN|
|7495|Line 2 UTR Number of the original transaction Line 3 Reason for return|

2.
3.
It may be noted that field tag 7495 contains 6 lines and the RTGS participants are required to provide the minimum return information as stated above in the first three lines. Any additional information, in case an RTGS participant intends to provide, may do so in the subsequent three lines.

<!-- PAGE 2 -->

4. All RTGS participants are advised to implement the new return guidelines latest by 15 July, 2009.
5. <u>Information Sharing</u> Some of the trade bodies / business councils have brought to our notice their difficulties on account of banks not notifying the RTGS debits /credits as and when the same takes place in the accounts of the customers. We understand that quite a good number of banks send SMSs to the account holders as and when the account is debited /credited. Besides, customers having access to their accounts through internet banking are also enabled to view their accounts without any dependency on the bank. However, in order to make RTGS more customer friendly, all RTGS participants may explore the possibility of sending SMS / email information to customers when an RTGS debit / credit takes place.
## Please acknowledge receipt of the circular.

Yours faithfully,

(G. Padmanabhan) Chief General Manager

# Withdrawn with effect from February 18, 2022
