---
doc_id: "Circulars_2010_RBI_2009-2010_305_DPSS_CO_EPPD_No_168_04_03_01_2009-2010"
title: "National Electronic Funds Transfer (NEFT) System – Refinement of process-flow and enhancement of features"
category: "Circulars"
year: 2010
source_rbi_url: "https://rbidocs.rbi.org.in/rdocs/Notification/PDFs/NEFTR050210.PDF"
pdf_sha256: "0ab0de07ee1516557e4366ac9dedf83139ccaacaab7c4eddddcda8e5c6ccda95"
md_sha256: "80803615786ffdefaf57a0e7948a06ade84f303551226e5fc2eb66621c88395c"
total_pages: 4
native_pages: 4
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T08:49:42Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Circulars/2010/2010-02-05_Circular_RBI-2009-2010-305%20DPSS%20CO%20EPPD%20No.168%20-%2004.03.01%20-%202009-2010_National%20Electronic%20Funds%20Transfer%20%28NEFT%29%20System%20%E2%80%93%20Refinement%20of%20process-flow%20and%20enhancement%20of%20features.pdf"
verification_status: "VERIFIED_LEVEL_5"
---
# National Electronic Funds Transfer (NEFT) System – Refinement of process-flow and enhancement of features

<!-- PAGE 1 -->

# भारतीय िरज़वर् बैंक RESERVE BANK OF INDIA

www.rbi.org.in

RBI/2009-10/305 **DPSS CO EPPD No.168 / 04.03.01 / 2009-2010 February 5, 2010**

The Chairman and Managing Director / Chief Executive Officer of all member banks participating in NEFT

Madam / Dear Sir,

## <u>National Electronic Funds Transfer (NEFT) System – Refinement of process-flow and enhancement of features</u>

The National Electronic Funds Transfer (NEFT) system has been successfully handling significant volumes, ever since its launch in November 2005. More than 6 million transactions were processed by the system during the month of January 2010 alone. The coverage has also increased substantially with the participation of over 63,000 bank branches spread across the length and breadth of the country.

2. NEFT uses the Public Key Infrastructure (PKI) technology to assure end-to-end security and the Indian Financial Network (INFINET) to connect bank branches for electronic transfer of funds. In line with the system capabilities and user expectations, a number of initiatives have been taken in the recent past to extend operating hours, increase the number of batches and handle more transaction types. Incidentally, NEFT has no amount restrictions and accepts cash up to Rs. 50,000 for originating transactions.
3. With a view to further strengthen the NEFT system in terms of availability, convenience, efficiency and speed, the following refinements to process-flow and enhancements to operational features are being introduced –
**(i) Tightening of Return Window** – Presently, the NEFT procedural guidelines mandate banks to return NEFT transactions in the very next available batch. The NEFT system has, however, been designed to allow destination banks to return transactions on a T+1 basis. The traffic ana
# Subsumed into NEFT Procedural Guidelines v1.1 with effect from April 7, 2026

lysis has revealed that a major chunk of returns are effected by banks either in the last batch of the day or in the first batch of the next day, indicating that the transactions are processed by the destination batches only at the end of the day instead of batch-wise. In order to streamline the system and complete the processing cycle on a near-real-time basis, the concept of return within two hours of completion of a batch is being introduced. The B+2 return discipline would require banks to afford credit to beneficiary accounts immediately upon completion of a batch or else return the transactions within two hours of completion of the batch settlement, if credits are unable to be afforded for any reason. Required changes in the SFMS / NEFT software has been carried out. Necessary changes are also being made to the Procedural Guidelines for the purpose.

भगतान ु और िनपटान ूणाली िवभाग, कें िीय कायार्लय, 14वी मंिजल, कें िीय कायार्लय भवन,शहीद भगत िसंह माग, र् फोटर्, मुम्बई - 400001 œ¸€¸½›¸ Tel: (91-22) 2264 4995; œ¸¾€Æ¬¸ Fax: (91-22) 22691557; ƒÄ-Ÿ¸½¥¸ e-mail : th <u>cgmdpssco@rbi.org.in</u> Department of Payment and settlement Systems, Central Office, 14 Floor, Central Office Building, Shahid Bhagat Singh Road, Fort, Mumbai - 400001 िहन्दी आसान है, इसका ूयोग बढ़ाइए

<!-- PAGE 2 -->

**-2-** **(ii) Increase in Operating Hours** – NEFT is currently available from 9 am to 5 pm on week days and from 9 am to 12 noon on Saturdays. There have been constant requests from various individual and business segments to elongate the operating hours. After examining the feasibility and customer benefits, it has been decided to extend NEFT operating hours from 9 am to 7 pm on week days and from 9 am to 1 pm on Saturdays. Member banks need to effect changes at their end to initiate and / or receive NEFT transactions taking full advantage of the increased hours of operation.

**(iii) Move to Hourly Settlements** – On date, NEFT has six batches of settlement at 9 am, 11 am, 12 noon, 1 pm, 3 pm and 5 pm on week days and three batches of settlement at 9 am, 11 am and 12 noon on Saturdays. An analysis of daily data has shown that the volume of transactions processed in batches that have a gap of two hours between batches is double the volume of

# 2026

transactions processed in batches that have only an hour’s gap between them. With a view to7, evenly space out transactions across batches, as also to make the system near-real-time, it has been decided to introduce the concept of hourly settlements. Accordingly, there would be eleven

# April

hourly settlements starting from 9 am to 7 pm on all week days and five hourly settlements from 9 from am to 1 pm on Saturdays. Necessary changes have been carried out in the SFMS / NEFT software. effect **(iv) Implementation of Positive Confirmation** – At present, the un-credited NEFT transactions are returned by destination banks and it is presumed that credit for all other transactions have beenwith afforded to beneficiary accounts. In order to remove any ambiguity and to introduce the element of v1.1 positive confirmation, the NEFT outward message format is being modified to contain two additional fields, wherein mobile number and / or e-mail address of the originating customer can be populated. A new message format is also being introduced to relay to the originating bank an acknowledgement containing the date and time of credit, immediately after the credit is afforded toGuidelines beneficiary accounts. This message would flow from the destination bank / branch to the originating bank / branch. The originating banks after receiving the positive confirmation from the destination banks shall have to initiate a mobile SMS or generate an e-mail to the originator to convey the fate

# Procedural

of the transaction. Detailed process flow for generating the positive confirmation is enclosed. SFMS / NEFT has been modified to add the required fields in the existing messages as also to handle the

# NEFT

new messages. into

4. The above modifications will be implemented in NEFT with effect from March 1, 2010. Member banks are advised to carry out appropriate changes to their CBS / system interfaces to handle the enhancements. In order to facilitate smooth migration, IDRBT-Hyderabad would release modified patches to be applied on SFMS / NEFT applications by February 15, 2010. For any additional
# Subsumed

information / clarifications, the NEFT team at your bank can contact officials of DPSS or IDRBT through <u>email</u>.

5. Please acknowledge receipt and confirm completion of necessary arrangements. Yours faithfully, -Sd- (**G Padmanabhan**) Chief General Manager Encl. : Process flow for positive confirmation in NEFT

<!-- PAGE 3 -->

## <u>Enclosure to letter DPSS.CO.EPPD.No.1687 /04.03.01/2009-2010 dated February 5, 2010</u>

## <u>Process Flow on Positive Confirmation in NEFT</u>

This document discusses the work flow to send a credit acknowledgement (N10) to the sender bank after successfully crediting to the beneficiary account. On receiving the credit acknowledgement (N10) at the sender bank, SFMS at the sender bank should send an e-mail / SMS to the sender party (customer) about the successful transfer of the funds.

The process flow of credit confirmation based on CBS banks and non-CBS banks is as follows :

## A. <u>CBS Implemented Banks</u>

1. After successfully crediting the beneficiary account, CBS will send a Credit Acknowledgement (N10 message) to SFMS. On receiving the outward N10 message from
# 2026

receiver CBS, SFMS will update the status of respective transactions as “Credited to 7, Customer”. The same outward Credit Acknowledgement (N10) will be sent to RBI Service centre (RBIP0NEFTSC). Outward N10 messages may contain transactions of differentApril banks’.

2. On receiving N10 at RBI Service centre, NEFT segregates the N10’s b
from ank-wise and sends to corresponding sending / initiator bank’s service centre through SFMS. effect

3. At the bank’s service centre, on receiving the inward N10 messages, corresponding transactions will be updated with the transaction status as "Credited to Customer" and willwith send the inward N10 to CBS. Finally, SFMS will send credit confirmation to the customer through SMS / e-mail according to the details provided in the field SMS / e-mail of debit v1.1 transaction. The CBS branches are provided with the interface to receive the positive acknowledgement from their CBS in a STP manner.
# Guidelines

## B. <u>Non-CBS Banks</u>

1. After successful crediting to the beneficiary a Procedural ccount, the user in the beneficiary branch will initiate a credit acknowledgement by clicking a button provided in SFMS. This will update the status of respective transactions as “Credited to Customer”. An outward N10 message is
# NEFT

created and sent to his bank’s service centre IFSC. into

2. A new process in SFMS polls on database and consolidates the credit acknowledgements based on the “Credited to customer” status and sends a new outward N10 message to RBI service centre.
3. On receiving N10 at RBI Service centre, Subsumed
NEFT segregates the N10’s bank-wise and sends to corresponding sending / initiator bank’s service centre through SFMS.

4. On receiving the inward N10 messages at Sending bank’s service centre, NEFT will segregate the N10 messages branch-wise and will send them to Gateway Æ Sender branch IFSC.
5. On receiving the inward N10 messages at Sender branch, corresponding transaction status will be updated as "Credited to the Customer". Finally, SFMS will send credit confirmation to the customer through SMS / e-mail according to the details provided in the field SMS / e-mail of debit transaction. The destination banks / branches which are non-CBS may use the SFMS / NEFT screen to create the N10 messages by clicking the appropriate button, similar to creating the return messages.

<!-- PAGE 4 -->

The originating bank will send the SMS / e-mail to the originator. The SMS / e-mail will mention – “NEFT Transaction with reference number 123456789 for Rs.

999.99 has been credited on DD-MM-YYYY at HH:MM:SS”. It is also intended to initiate SMS and / or generate e-mail to be sent to the originator for negative acknowledgements – i.e., for those transactions returned without offering credit to beneficiary accounts. For the modified / new message format, banks may approach officials of DPSS or IDRBT through <u>email</u>.
2026 7, April from effect with v1.1

Guidelines

Procedural NEFT into

Subsumed
