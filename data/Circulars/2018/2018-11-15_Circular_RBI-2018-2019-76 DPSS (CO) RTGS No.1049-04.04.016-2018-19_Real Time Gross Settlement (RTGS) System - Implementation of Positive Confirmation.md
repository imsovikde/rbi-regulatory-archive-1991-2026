---
doc_id: "Circulars_2018_RBI_2018-2019_76_DPSS_CO_RTGS_No_1049_04_04_016_2018-19"
title: "Real Time Gross Settlement (RTGS) System - Implementation of Positive Confirmation"
category: "Circulars"
year: 2018
source_rbi_url: "https://rbidocs.rbi.org.in/rdocs/Notification/PDFs/NOTI76F381FE590FC34B6AA6D1A23C18505D91.PDF"
pdf_sha256: "0594f130343ac2775d59f60fbed309a4e4df8a1db9e518e091e896e327518955"
md_sha256: "d4d37e395052d6c008a46d9ef82a9944da3da8a531315e656408e183a1884003"
total_pages: 4
native_pages: 4
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T10:40:33Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Circulars/2018/2018-11-15_Circular_RBI-2018-2019-76%20DPSS%20%28CO%29%20RTGS%20No.1049-04.04.016-2018-19_Real%20Time%20Gross%20Settlement%20%28RTGS%29%20System%20-%20Implementation%20of%20Positive%20Confirmation.pdf"
verification_status: "VERIFIED_LEVEL_5"
---
# Real Time Gross Settlement (RTGS) System - Implementation of Positive Confirmation

<!-- PAGE 1 -->

भारतीय �रज़वर् बक **RESERVE BANK OF INDIA** <u>www.rbi.org.in</u>

## RBI/2018-19/76 DPSS (CO) RTGS No.1049/04.04.016/2018-19 November 15, 2018

The Chairman / Managing Director / Chief Executive Officer of member banks participating in RTGS

Madam / Dear Sir,

## <u>Real Time Gross Settlement (RTGS) System - Implementation of Positive Confirmation</u>

Presently, the National Electronic Funds Transfer (NEFT) system provides for sending a positive confirmation to the remitter of the funds regarding completion of the funds transfer, thus giving an assurance to the remitter that the funds have been successfully credited to the beneficiary account. It has now been decided that banks will provide the same facility to the remitter of funds under the RTGS system as well.

2. Initially, the positive confirmation feature in RTGS would be available for member banks wherein both remitter and beneficiary banks access RTGS through thick client interface / SFMS member interface. Member banks are expected to communicate the same to their customers. The positive confirmation feature would be subsequently enabled for member banks accessing RTGS through other channels as well.
# Subsumed into RTGS System Regulations v1.1 effective from May 13, 2026

3. In this connection, a new message format (camt.059) is being introduced to communicate an acknowledgement to the remitting bank containing the date and time of credit to beneficiary account. This message would flow from the beneficiary bank to the remitter bank through the SFMS. After receiving the positive confirmation from the beneficiary bank, the remitter bank shall initiate an SMS and / or generate
भुगतान और िनपटान �णाली िवभाग, क ीय कायार्लय, 14वीमंिजल, क ीय कायार्लय भवन,शहीद भगतसंह मागर्, फोटर्, मुम्बई - 400001 फोनTel: (91-22) 2264 4995; फ ै क् स Fax: (91-22) 22691557; ईमेल-e-mail : <u>cgmdpssco@rbi.org.in</u> Department of Payment and Settlement Systems, Central Office, 14thFlr, Central Office Building, Shahid Bhagat Singh Road, Fort, Mumbai - 400001 हंदी आसान है, इसका �योग बढ़ाइए

<!-- PAGE 2 -->

an e-mail to the remitter. The <u>detailed process flow</u> for the positive confirmation process is appended.

4. All banks are required to put in place systems to ensure straight-through- processing (STP) based confirmation processing. The beneficiary bank shall ensure that such confirmation message is sent as soon as the amount is credited to the beneficiary account in CBS while the confirmation message from the remitting bank shall be necessarily sent on a real time basis and in any case not beyond one hour after receipt of credit message from the beneficiary bank.
5. The system of sending positive confirmation to the customers shall be 2026 operationalised by banks at the earliest but not later than two months from the date13, of this circular. May
from

6. These directions are issued by Reserve Bank of India, in exercise of the powers conferred by section 18 of Payment and Settlement Systems Act, 2007 (Act 51 of
effective

2007).
v1.1 Yours faithfully

# Regulations

(P. Vasudevan) Chief General Manager

# System

Encl.: As above

# RTGS into

# Subsumed

<!-- PAGE 3 -->

<u>Annex</u> <u>Process flow on positive confirmation in RTGS</u> **(DPSS (CO) RTGS No.1049/04.04.016/2018-19 dated November 15, 2018)**

This document outlines the process flow for electronic credit acknowledgement message (camt.059) to the remitter bank by the beneficiary bank after successful credit to the beneficiary account.

# 2026

The process flow for successful credits shall be as under:- 13,

1. On successful credit to the beneficiary account, the beneficiary bank will send a
May credit acknowledgement message (camt.059) through SFMS in an automated from manner.

2. The information in the camt.059 message shall necessarily contain among others
effective the date / time stamp of credit and the UTR number. v1.1

3. On receipt of the camt.059 message from the beneficiary bank, SFMS will forward the same outward camt.059 message to the remitter bank as an inward camt.059 message.
# Regulations

4. On receipt of the inward camt.059 message, the remitter bank will update the transaction status as "Credited to Customer" for the corresponding transaction.
# System

5. Remitter bank shall immediately forward the credit confirmation to the customer through SMS and / or e
# RTGS

-mail according to the details provided. The message shall among others contain the RTGS transaction number ascribed by the bank and / or into

UTR number, the date / time stamp of credit confirmation, beneficiary bank account number and amount.

# Subsumed

<!-- PAGE 4 -->

|Beneficiary Bank|Remitter Bank||
|---|---|---|
|Funds credited to|Update transaction||
|beneficiary account|status-Credited to Customer|Send SMS and / or e-mail|

# SFMS Customer

**camt.059 camt.059**

Banks may approach officials of IFTAS on <u>email</u> for the new message format camt.059. 2026 13, May from

effective v1.1

Regulations System RTGS into

Subsumed
