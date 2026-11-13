---
doc_id: "Notifications_2019_11505"
title: "Compilation of R-Returns: Reporting under FETERS"
category: "Notifications"
year: 2019
source_rbi_url: "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/APDIR25639B479541E446839B356F40670FC526.PDF"
pdf_sha256: "48036ad70f3d04035752c3d8a8e0612e4793101cc3c3091d338c24962813e56d"
md_sha256: "78e58edd035f7e33e23ea4580913a75dd438064a9d13c4cc1036cd6110c942a6"
total_pages: 4
native_pages: 4
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T14:02:12Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Notifications/2019/2019-03-20_Notification_11505_Compilation%20of%20R-Returns-%20Reporting%20under%20FETERS.pdf"
verification_status: "VERIFIED_LEVEL_5"
---
# Compilation of R-Returns: Reporting under FETERS

<!-- PAGE 1 -->

## RBI/2018-2019/145 A.P. (DIR Series) Circular No. 25 March 20, 2019

To, All Authorised Dealers in Foreign Exchange

||Madam / Sir,|||
|---|---|---|---|
||dated February 29, 2012, Series) Circular No.50 dated February 11, 2016 (FETERS).|2. In order to facilitate compilation of estimates of bilateral trade in services, it has been decided to incorporate an additional field for capturing the country code of ultimate exporter/importer in the BoP file-format under FETERS. In case of export of services, bank may use the transaction information available with them to report country-code of the ultimate exporting country, whereas Form-A2 is being revised here for capturing the required country information for import of services.|Compilation of R-Returns: Reporting under FETERS Attention of Authorised Dealer (Category I) banks is invited to A.P. (DIR Series) Circular No.84 A.P. (DIR Series) Circular No.15 dated July 28, 2014 and A.P (DIR giving guidelines for compilation of R-Returns for reporting under the Foreign Exchange Transactions Electronic Reporting System|
|3.|The details of the additional field is as follows:|||
|i.|BoP file-format under FETERS|||
||Field|Format|Remarks|
||Country Code (SWIFT Code) of ultimate exporter/importer|Char(2)|To be added at the end of BOP file format|
|ii.|07, 08, 09 10, 11, 15, 16 or 17), please indicate: given in Annex I and Annex II, respectively. 4. The revised format is for reporting of R-Returns on fortnightly basis (15 the guidelines.|transactions performed w.e.f. April 01, 2019. AD Banks should make the required changes in their work-flows and information systems to capture the required additional data accordingly to comply with|Form A2 - If payment is for import of services (Purpose Group Nos. 02, 03, 05, 06, "Name of the country providing ultimate services: ..................... " The Form A2 (revised) and the file format (revised) of the BOP file for reporting under FETERS are th and end-month) for forex|
|5. T|he directions contained in this circular have been issued under permissions / approvals, if any, required under any other law. Yours faithfully,|of the Foreign Exchange Management Act, 1999 (42 of 1999) and are without prejudice to|Sections 10(4) and 11(1)|

(Ajay Kumar Misra) Chief General Manager -in -Charge

<!-- PAGE 2 -->

## Annex I

## FORM A2

(To be completed by the applicant)

|(For payments other|AD Code No.__________________________||
|---|---|---|
|than imports of goods and|Form No._____________________________||
|remittances||(To be filled in by the Authorised Dealer)|
|covering intermediary trade)|Currency_____ Amount ___Equivalent to Rs. _______||
|Application for||(To be completed by the Authorised Dealer)|

## <u>Remittance Abroad</u>

I/We _____________________________________________________________ (Name of applicant remitter) PAN No. __________________________________________________________ Address___________________________________________________________ authorize __________________________________________________________________ (Name of AD branch) To debit my Savings Bank/ Current/ RFC/ EEFC A/c. No. ____________________ together with their charges and

* a) Issue a draft: Beneficiary's Name _________________________________
Address _________________________________

* b) Effect the foreign exchange remittance directly –
1) Beneficiary's Name __________________________________
2) Name and address of the bank __________________________________
3) Account No. __________________________________
* c) Issue travellers cheques for __________________________________
* d) Issue foreign currency notes for __________________________________ Amount (specify currency) __________________________________
** (Strike out whichever is not applicable) for the purpose/s indicated below*
2) To be filled in by residents only if the remittance is made under LRS **Sr. Whether under LRS Purpose Code Description** **No. (Yes/No)**
**(3) Payment for import of services (Purpose Group Nos. 02, 03, 05, 06, 07, 08, 09** **10, 11, 15, 16 or 17), please indicate:** “Name of the country providing ultimate services: …………….” (Remitter should put a tick (√) against an appropriate purpose code. In case of doubt/ difficulty, the AD bank should be consulted).

<!-- PAGE 3 -->

## Declaration

## (Under FEMA 1999)

***1.** I, ………………. …………(Name), hereby declare that the total amount of foreign* *exchange purchased from or remitted through, all sources in India during the* *financial year* including this application *is as per the extant FEMA Regulations and* *certify that the source of funds for making the said remittance belongs to me and the* *foreign exchange will not be used for prohibited purposes / **Foreign exchange*** ***purchased from you is for the purpose indicated above.***
## Details of the remittances made/transactions effected under the Liberalised

## Remittance Scheme in the current Financial Year (April-March)…………

|Sr.|Date|Amount|Name and address of AD branch/FFMC through|
|---|---|---|---|
|No.|||which the transaction has been effected|

## Signature of the applicant

(Name) Date:

## Certificate by the Authorised Dealer

This is to certify that the remittance is not being made by/ to ineligible entities and that the remittance is in conformity with the instructions issued by the Reserve Bank from time to time under the Scheme.

Name and designation of the authorised official: Stamp and seal

Signature: Date:

<!-- PAGE 4 -->

## Annex II

## FETERS File Layouts

**1. BANKCODE_BOP6.TXT** relating to transactions involving sale and purchase of foreign exchange (excluding inter-office, inter-bank, RBI transactions) during the reporting fortnight

|Field|Format|Remarks|
|---|---|---|
|AD Code|Char (7)|BSR Part-1 Uniform Code|
|Fortnight-end Date|YYYYMMDD||
|Transaction Date|YYYYMMDD|Valid date within fortnight|
|Serial No.|Num. (4)||
|Purpose Code|Char (5)|Purpose code starting with P/S (Part A/B of Annex I)|
|Country Code|Char (2)|SWIFT code|
|Currency Code|Char (3)|SWIFT code|
|Amount [in Foreign Currency (FC)]|Num. (15)||
|Date of Shipment|YYYYMMDD||
|LC|char (1)|1 for Yes; 0 for No|
|Country of Vostro a/c Holder|char (2)|SWIFT code|
|Country Code of ultimate exporter/importer|Char (2)|SWIFT Code|

**2. BANKCODE_QE.TXT** for Cover Page Totals

|Field|Format|Remarks|
|---|---|---|
|A.D. Code|Char (7)||
|Fortnight-end date|YYYYMMDD||
|Serial Number|Num. (4)||
|Purpose Code|Char (5)|As per Part C of Annex I|
|Country of Vostro A/c holder|Char (2)||
|Currency|Char (3)||
|Amount in Currency|Num. (15)||
|Return (Vostro/Nostro)|Char (1)|V for Vostro; N for Nostro|
