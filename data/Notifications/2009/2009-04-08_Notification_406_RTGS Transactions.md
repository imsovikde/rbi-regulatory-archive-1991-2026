---
doc_id: "Notifications_2009_406"
title: "RTGS Transactions"
category: "Notifications"
year: 2009
source_rbi_url: "https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/CRRTGST_0408.pdf"
pdf_sha256: "a4e15409f461bff67fe33d81f31eb537cf6172c7438130a4ac72f667ac644cd1"
md_sha256: "c24b730b7fab0f10cc1cd58e710a3f1d48a4d3a84a1cdf216653048a2b204212"
total_pages: 2
native_pages: 2
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T12:48:49Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Notifications/2009/2009-04-08_Notification_406_RTGS%20Transactions.pdf"
verification_status: "VERIFIED_LEVEL_5"
---
# RTGS Transactions

<!-- PAGE 1 -->

## RBI/2008/09/426

DPSS (CO) RTGS No. 1776 / 04.04.002 / 2008 - 2009 April 8, 2009

Chairman and Managing Director / Chief Executive Officer of all banks participating in RTGS

Dear Sir, <u>RTGS Transactions</u>

The volume of RTGS transactions is increasing rapidly. RTGS settled 1.94 million transactions in the month of March 2009 as against 0.72 million transactions in March 2008. Customer transactions settling in RTGS presently constitute 89 percent of total RTGS transactions and are growing. At a recent meeting with major banks, we reviewed the entire gamut of RTGS customer transactions with a view to making them more user friendly. Based on these discussions, the following decisions have been taken for implementation by RTGS members.

2. It may be recalled that we had vide our circular DPSS (CO) No. 1607 / 04.04.002 / 2007 - 2008 dated April 7, 2008 advised all RTGS members to comply with the wire transfer guidelines issued by the Reserve Bank of India while originating wire transfers. We had also enclosed prototype of a R41 message format and explained how the message format should capture the details of sender and receiver information. Banks were also required to furnish complete information in field tag No. 5500 and 5561 of customers message format (R-41) as under:-
## Field tag 5500

|Line 1|Sender's bank account number /||
|---|---|---|
||Country specific unique reference number /|35X|
||Identification number||
|Line 2|Name of the Sender/ remitter|35X|
|Line 3 and 4|Address and Place of Residence|2*35X|

## Field tag 5561

|Line 1|Account number|[/34X]|
|---|---|---|
|Line 2|Name of the Beneficiary|35X|
|Line 3, 4 and 5|Address and Place of Residence|3*35X|

<!-- PAGE 2 -->

3. We understand that while some of the banks are furnishing the required details in the messages, others have not yet implemented the guidelines. It is therefore once again reiterated that in a Straight Through Processing (STP) environment, standardization is very much necessary and uniformity in message format is a pre requisite for the success of STP.
4. RTGS Customers have been complaining that there is no uniformity on information provided to the customer in the pass books / account statements by different banks. Some banks merely indicate `RTGS credit’ without details while other banks are giving sender's bank account number or UTR number of the transactions etc. This is on account of the Core Banking Solution (CBS) of different banks capturing information from different field tags of the message format. As a result, a customer is receiving multiple RTGS credits on a given date, is at a loss to understand the source of funds leading to reconciliation issues.
5. It is therefore, advised that
a) A bank customer receiving RTGS credit shall be provided with the name of the remitter in his account statements / pass book.
b) A bank customer sending a RTGS remittance shall be provided with the name of the beneficiary in his account statements / pass book. For the purpose, it is advised that information in field tag no. 5500 and 5561 should be provided uniformly by all banks as advised above. The CBS of the banks should be fine tuned to capture line 2 of field tag no. 5500 for the receiver’s account statement/ pass book and line 2 of field tag no. 5561 for the sender’s account statement/ pass book. The banks are free to provide any additional information as they deem necessary / useful.
6. All RTGS member banks may initiate steps to comply with these instructions latest by June 01, 2009. Please acknowledge receipt and forward an action taken report in due course. Yours faithfully, (G. Padmanabhan) Chief General Manager
