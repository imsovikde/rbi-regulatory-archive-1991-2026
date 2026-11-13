---
doc_id: "Notifications_2022_12431"
title: "Central Payments Fraud Information Registry – Migration of Reporting to DAKSH"
category: "Notifications"
year: 2022
source_rbi_url: "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/NT158E6817A5F7C4B47F3AE93090730E257AB.PDF"
pdf_sha256: "ecbcbae37eefceceb2e31d6b005d0684795249d59c79908db0292393e646f21a"
md_sha256: "04e6d5284b925b03bdb0757c36b246083ad8613242b5efaeb1dd920150e80ab6"
total_pages: 16
native_pages: 16
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T14:06:43Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Notifications/2022/2022-12-26_Notification_12431_Central%20Payments%20Fraud%20Information%20Registry%20%E2%80%93%20Migration%20of%20Reporting%20to%20DAKSH.pdf"
verification_status: "VERIFIED_LEVEL_5"
---
# Central Payments Fraud Information Registry – Migration of Reporting to DAKSH

<!-- PAGE 1 -->

RBI/2022-23/158 CO.DPSS.OVRST.No.S1619/06-08-005/2022-2023 December 26, 2022

The Chairman / Managing Director / Chief Executive Officer Banks, Non-bank Payment System Operators (PSOs) and Credit Card issuing Non-Banking Financial Companies (NBFCs)

Madam / Dear Sir,

## Central Payments Fraud Information Registry – Migration of Reporting to DAKSH

As announced in the <u>Monetary Policy Statement 2019-20 on August 07, 2019</u>, the Reserve Bank of India (RBI) had operationalised the Central Payments Fraud Information Registry (CPFIR) in March 2020 with reporting of payment frauds by scheduled commercial banks and non-bank Prepaid Payment Instrument (PPI) issuers.

2. To streamline reporting, enhance efficiency and automate the payments fraud management process, the fraud reporting module is being migrated to <u>DAKSH – Reserve</u> <u>Bank’s Advanced Supervisory Monitoring System</u>. The migration will be effective from **January 01, 2023**, i.e., entities shall commence reporting of payment frauds in DAKSH from this date. In addition to the existing bulk upload facility to report payment frauds, DAKSH provides additional functionalities, viz. maker-checker facility, online screen-based reporting, option for requesting additional information, facility to issue alerts / advisories, generation of dashboards and reports, etc. The reporting guidelines are mentioned in the **Annex**.
3. These directions are issued under Section 10 (2) read with Section 18 of Payment and settlement Systems Act, 2007 (Act 51 of 2007). Yours faithfully, (P. Vasudevan) Chief General Manager

<!-- PAGE 2 -->

## (Annex to Circular CO.DPSS.OVRST.No.S1619/06-08-005/2022-2023 dated December 26,

## 2022)

## Annex

## CPFIR – Reporting Guidelines

- All RBI authorised Payment System Operators (PSOs) / providers and payment system participants operating in India are required to report all payment frauds, including attempted incidents, irrespective of value, either reported by their customers or detected by the entities themselves. This reporting was earlier facilitated through Electronic Data Submission Portal (EDSP) and is being migrated to DAKSH.
- The responsibility to submit the reported payment fraud transactions shall be of the issuer bank / PPI issuer / credit card issuing NBFCs, whose issued payment instrument has been used in the fraud.
- Entities are required to validate the payment fraud information reported by the customer in their own systems to ensure the authenticity and completeness, before reporting the same to RBI on individual transaction basis.
- Entities are required to report payment frauds (domestic and international) to CPFIR as per the specified timelines (currently within 7 calendar days from date of reporting by customer / date of detection by the entity).
- Entities may continue to report payment frauds as per the extant reporting format using the bulk upload facility in DAKSH or report individual payment frauds online using the screen-based facility under the Incident Module of the DAKSH platform.
- After go-live of payment fraud reporting in DAKSH effective January 01, 2023, entities shall not be able to report any payment frauds in EDSP. Entities may, however, continue to update and close payment frauds that were reported in EDSP until December 31, 2022. Reserve Bank shall subsequently migrate the historical data from EDSP to DAKSH.
- The reporting format remains unchanged (<u>Appendix</u>**)**.
- Though some elements / fields of the Reporting Format are indicated as ‘Optional’, entities shall strive to include them as part of initial reporting itself and only in exceptional cases be reported as updates.

<!-- PAGE 3 -->

## Appendix

## CPFIR – Payment Fraud Reporting

The data collection file format is a combination of a single Header row and one or more data rows. The Header row is used to collect the metadata information about the data submitted by the reporting entity and data row contains details of the payment fraud reported.

# Header Format

|Field Name||Field Length|Comments|Example|
|---|---|---|---|---|
|Return Code||3|Must be ‘ PFR|’ (Payment Fraud Reporting) PFR|
|Flag||1|I – To identify the file has come for inserting the records for initial reporting U – To identify file has come for updating the records already reported|I or U|
|Reporting Entity Code||Upto 7 digit|As per the Centralised Information System for Banking Infrastructure (CISBI) of RBI|010|

File Submission 8 Must be ‘**DDMMYYYY**’ 21012020 Date 20 Number of data rows present in the submitted Record Count 1 file excluding header

**Note:**

- All individual fields must be separated by a colon (:).
- Header record must end with semi-colon (;)
## Example:

PFR:I:010:21012020:1;

# Data Row Format

||Field|Mandatory|||
|---|---|---|---|---|
|Field Name|Length|(M) / Optional (O)|Guidelines|Comments|
|Internal|||Alphanumeric field that|Only alphanumeric,|
|identifier used|20|O|can be used by reporting|underscore, hyphen|
|by bank / non-|||entity for their internal|and multiple spaces|
|bank entity|||reference, if required.|are allowed.|

<!-- PAGE 4 -->

|category|||document.|
|---|---|---|---|
|System|||System involved to be|
|involved in|10|M|selected from the master|
|the fraudulent|||data provided in Annex|
|transaction|||of this document.|
|Payment|||Three digit code from the|
|channel used|3|M|master data code list|
|for fraudulent|||provided in Annex of this|
|transaction|||document.|

|fraud ?|||Else – N;|
|---|---|---|---|
|Payment|||Three digit code from the|
|transaction|3|M|master data code list|
|instrument|||provided in Annex of this|
|used|||document.|
|Payment|||Three digit code from the|
|system|3|M|master data code list provided in Annex of this|
|category|||document.|
|System|||System involved to be|
|involved in|10|M|selected from the master|
|the fraudulent|||data provided in Annex|
|transaction|||of this document.|
|Payment|||Three digit code from the|
|channel used|3|M|master data code list|
|for fraudulent|||provided in Annex of this|
|transaction|||document.|
|Nature of|||Three digit code from the|
|fraudulent|3|O|master data code list provided in Annex of this|

|Was the fraud|||If fraud reported by|
|---|---|---|---|
|reported by|1|M|Customer – Y; If fraud detected by Bank|
|customer ?|||/ non-bank entity – N;|
|Was it an|||If attempted fraud – Y;|
|attempted|1|M||

transaction document. Date of occurrence of the fraud as

|identified by|8||Must be DDMMYYYY|
|---|---|---|---|
|the bank /||||
|non-bank||If Fraud||
|entity||Reported by||
|Date of||Customer =||
|detection of||No; M||
|the fraud by|8||Must be DDMMYYYY|

bank / non- bank entity Date of entering in the 8 Must be DDMMYYYY system Date of occurrence of

## Must be DDMMYYYY

|the fraud transaction|8 If Fraud|
|---|---|
|reported by|Reported by|
|customer|Customer = Yes; M|

Time of occurrence of Must be HH:MM:SS the fraud

<!-- PAGE 5 -->

transaction reported by customer

Reporting date of fraud by the 8 Must be DDMMYYYY customer to bank / PPI issuer / PSO Date of entering the fraud by the 8 Must be DDMMYYYY bank / PPI issuer / PSO in the system Unique Transaction Reference No. generated

|Unique|by the payment system||
|---|---|---|
|Transaction|that has processed the payment transaction.|Only alphanumeric,|
|Reference|M For attempted frauds that|underscore and|
|No. of the|do not have any UTR,|hyphen are allowed.|
|fraudulent|entities may specify||

transaction ATTEMPTEDXXXX where XXXX is a sequence number. Is the fraud a If domestic transaction-domestic 1 M Y; else – N; transaction? Only alphabets, numbers, dot, parentheses, single

|Reporting|||quote / apostrophe,|
|---|---|---|---|
|customer|100|If Fraud|ampersand, comma, hyphen, forward|
|name||Reported by Customer = Yes; M|slash, back slash, underscore and multiple spaces are allowed.|
|Reporting|||Only numeric, single|
|customer|15||and hyphen are space, plus (1st char)|

## Name of the customer

mobile no. allowed. Reporting Standard characters customer e-50 O accepted in e-mail mail Only alphabets, Any other numbers, hyphen, detail of the O dot, comma, single reporting quote, colon, semi customer colon, forward slash

<!-- PAGE 6 -->

||and multi-spaces between them are allowed.|
|---|---|
|If PA / PG involved – Y; else – N;|Only alphabets, numbers, hyphen, dot, comma, single quote, colon, semi colon, forward slash, parentheses, ampersand, back slash, @ sign, hash, + and multiple spaces are allowed.|

Was any PA / 1 M <u>PG Involved ?</u>

If PA / PG If PA / PG involved, the 100 Involved = Y; name may be M provided

Was any third If third party PSP party PSP 1 M involved -Y; else N; involved ? Only alphabets, numbers, hyphen, dot, comma, single

|If third party|If Third party|quote, colon, semi|
|---|---|---|
|PSP involved,|PSP|colon, forward slash,|
|the name may|involved = Y;|parentheses,|
|be provided|M|ampersand, back|

slash, @ sign, hash, +, multiple spaces are allowed. Amount involved (INR If Attempted Only numbers are actuals) in the 20 Fraud = N; Amount in rupees allowed. fraudulent M transaction Amount recovered Only numbers are (INR actuals) 20 O Amount in rupees allowed. in the fraudulent transaction Was insurance If insurance coverage 1 O coverage available – Y; else – N; available ? Only alphabets,

|Name of||numbers, hyphen,|
|---|---|---|
|insurer and|If Insurance|dot, comma, single|
|per|Coverage =|quote, double quotes,|
|transaction|Y; M|ampersand, colon,|
|coverage||semicolon,|
|amount||parentheses, forward|

slash, dollar, euro,

<!-- PAGE 7 -->

pound, rupee, krona, back slash, multiple spaces and line break are allowed. Amount recovered If Insurance Only numbers are due to 20 Coverage = allowed. Insurance Y; M cover Only alphabets, numbers, dot, parentheses, single quote / apostrophe, Beneficiary 100 O Name of the Beneficiary ampersand, comma, name hyphen, forward slash, back slash, underscore and multiple spaces are allowed. Only numeric, single Beneficiary space, plus (1st char) 15 O mobile and hyphen are allowed. Beneficiary e-Standard characters

|mail|50|O||accepted in e-mail|
|---|---|---|---|---|
|Beneficiary||||Only numbers and|
|account number|50|O||alphabets are allowed.|
|Beneficiary|||Bank Working Code from||
|bank|7|O|CISBI. For Non-Bank the code provided by DPSS||
|Beneficiary|||Part 1 Code to be||
|branch (part 1|7|O|provided here as per the||
|code)|||CISBI||
|Beneficiary||||Only numbers and|
|branch IFSC|11|O|IFSC for the Branch|alphabets are allowed.|
|Beneficiary||||Only numbers and|
|PAN card no.|10|O||alphabets are allowed.|
|Beneficiary||||Only numbers are|
|debit / credit|16|O|||

allowed. card no.

<!-- PAGE 8 -->

|Beneficiary|Only alphabets,|
|---|---|
|PPI card /|numbers, + and multiple spaces are|

50 O wallet no. allowed. Only alphabets, numbers, @ sign, dot and hyphen are allowed in standard pattern.

Beneficiary @ is mandatory for 50 O UPI ID UPI ID.

In case the transaction is based on UPI Number that should be entered. (@ is not required) Only alphabets, numbers, hyphen, dot, single quote,

|Name of|colon, semi colon,|
|---|---|
|destination|forward slash, parentheses,|

100 O PPI issuer ampersand, back slash, @ sign, hash, + and multiple spaces are allowed. Only alphabets, numbers, forward slash, parentheses, dot, ampersand, Destination comma, colon, star, 50 O merchant ID hash, underscore, single quote / apostrophe, + and multiple spaces are allowed. Only alphabets, numbers, forward slash, parentheses,

|Destination|dot, ampersand,|
|---|---|
|merchant|hash, underscore, comma, colon, star,|

100 O name single quote / apostrophe, + andmultiple spaces are allowed. Only alphabets, Destination O numbers, hyphen, payment dot, comma, single

<!-- PAGE 9 -->

gateway / quote, colon, aggregator semicolon, forward slash, parentheses, Ampersand, Back slash, @, hash, + and multiple spaces are allowed. Destination Only alphabets and 50 O ATM ID <u>numbers are allowed.</u> Only alphabets, numbers, hyphen, dot, comma, single Suspect 100 O Website address quote, colon, semi website used colon, forward slash, hash and no spaces are allowed. Only alphabets, numbers, hyphen,

|Suspect|dot, comma, single|
|---|---|
|mobile app|quote, colon, semi colon, forward slash,|

100 O used hash and multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single Suspect quote, colon, semi 50 O device ID colon, forward slash, hash and multiple spaces between them are allowed.

|Suspect IP|||Only numbers, dot|
|---|---|---|---|
|Address|50|O|and colon are allowed.|
|Suspect IMEI|20|O|Only alphabets and|
|number|||numbers are allowed.|

Only alphabets, numbers, hyphen, dot, comma, single Suspect quote, colon, semi 50 O geotag ID colon, forward slash and multiple spaces between them are allowed. Only alphabets,

|Any other|numbers, hyphen,|
|---|---|
|details of|dot, comma, single quote, colon, semi|

100 O suspect colon, forward slash, hash and multiple

<!-- PAGE 10 -->

spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes,

|Initial inputs||ampersand, colon,|
|---|---|---|
|on modus|O Fraud related|semi colon, parentheses, forward|
|operandi of|information, if any|slash, dollar, euro,|

fraud pound, rupee, krona, line break and multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes, ampersand, colon,

|Modus|Fraud related updates, if|semi colon,|
|---|---|---|
|operandi – update 1|O any|parentheses, forward slash, dollar, euro,|

pound, rupee, krona, line break and multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes, ampersand, colon,

|Modus|Fraud related updates, if|semi colon,|
|---|---|---|
|operandi – update 2|O any|parentheses, forward slash, dollar, euro,|

pound, rupee, krona, line break and multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single

|Modus||quote, double quotes,|
|---|---|---|
|operandi –|O Fraud related updates, if any|ampersand, colon, semi colon,|

2000 update 3 parentheses, forward slash, dollar, euro, pound, rupee, krona, line break and

<!-- PAGE 11 -->

multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes, ampersand, colon,

|Modus|Fraud related updates, if|semi colon,|
|---|---|---|
|operandi – update 4|O any|parentheses, forward slash, dollar, euro,|

pound, rupee, krona, line break and multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes, ampersand, colon,

|Modus|Fraud related updates, if|semi colon,|
|---|---|---|
|operandi – update 5|O any|parentheses, forward slash, dollar, euro,|

pound, rupee, krona, line break and multiple spaces between them are allowed. False alert –

|transaction|1|O|Must be Y/N, after|
|---|---|---|---|
|was not a fraud|||investigation done|
|Fraud was||||
|registered||||
|with Law||||
|Enforcement|1|O|Y/N to be provided|

Agencies (LEA) / sub- judice Only alphabets, numbers, hyphen, dot, comma, single

|If fraud was||quote, double quotes,|
|---|---|---|
|registered|Details to be provided if|ampersand, colon,|
|with LEA,|O the above field response|semicolon,|
|details of|is YES|parentheses, forward|
|case reported||slash, dollar, euro,|

pound, rupee, krona, line break and multiple spaces

<!-- PAGE 12 -->

between them are allowed. Has the fraud incident been 1 M Must be Y/N closed? Date should be lesser

|||Details to be provided if|than or equal to|
|---|---|---|---|
|Date of|If Fraud|the above field response|current date and|
|closure of|Closed = Y;|is yes in DDMMYYYY|greater than or equal|
|fraud|M||to occurrence date as|

format well as detection date. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes, ampersand, colon,

|Justification|If Fraud|Details to be provided if|semicolon,|
|---|---|---|---|
|for closure of|Closed = Y;|the above field response|parentheses, forward|
|fraud|M|is yes|slash, dollar, euro,|

pound, rupee, krona, line break and multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes,

|Any other|ampersand, colon,|
|---|---|
|information|semicolon,|
|pertaining to|parentheses, forward slash, dollar, euro,|

## 2000 O

the fraud pound, rupee, krona, line break and multiple spaces between them are allowed. Only alphabets, numbers, hyphen, dot, comma, single quote, double quotes,

|Steps taken|ampersand, colon,|
|---|---|
|to address /|semicolon,|
|prevent such|parentheses, forward|
|frauds in|slash, dollar, euro,|
|future|pound, rupee, krona,|

## 2000 O

line break and multiple spaces between them are allowed.

<!-- PAGE 13 -->

**Note:**

- Mandatory fields once submitted cannot be modified (except for fraud closed which can be updated from No to Yes).
- Once a fraud is closed, no updates are permitted.
- The output file generated for successful records shall contain a Fraud Reference Number (FRN) assigned to all successfully inserted records. The FRN shall begin with ‘F’ for actual frauds and ‘A’ in case of attempted frauds. The same FRN must be used for reporting Updates.
- The format for reporting updates is same as the format for initial reporting (Insert). Only the FRN generated during initial (Insert) reporting must be appended at the start of the record followed by pipe (|).
- Although some fields are marked as optional, entities are advised to report maximum available data to facilitate analysis and strengthen the ecosystem.
- All data elements to be separated by pipe (|).
- No additional character to be included at the end of each record.
## Example: Insert record

CAN15112022000043446|Y|N|DEC|CAN|VISA|POS|OTH|||16112022|07112022|14:15:03|1411 2022|16112022|231108479433|Y|SANDEEP R PATEL|1234567890|||N||N||18805.62||Y|National - 100000|0.00||||||||||||||||||||||||SUSPECTED FRAUD TRANSACTION|||||||N||N||||

## Example: Update record

F010161120221|CAN15112022000043446|Y|N|DEC|CAN|VISA|POS|OTH|||16112022|0711202 2|14:15:03|14112022|16112022|231108479433|Y|SANDEEP R PATEL|1234567890|||N||N||18805.62||Y|National - 100000|0.00||||||||||||||||||||||||SUSPECTED FRAUD TRANSACTION|||||||N||N||||

<!-- PAGE 14 -->

## Annex

## Payment Transaction Instrument

## Payment Transaction

|ATM|ATM Networks|
|---|---|
|PII|Prepaid Payment Instrument Issuers|
|CMO|Cross-Border Money Transfer Operators|
|TRD|Trade Receivables Discounting System (TReDS)|
|IMO|Instant Money Transfer Operators|
|INB|Intra-Bank (Banks’ Core Banking System)|
|OTH|Other|

|Payment System Involved : Payment System Involved|Name of Payment System|Payment System Code|
|---|---|---|
|Based on input in 3C – Payment system category, the name of payment system used – RBI operated payment systems|Real Time Gross Settlement|RTGS|
||National Electronic Funds Transfer|NEFT|
|NPCI Operated Payment Systems|Immediate Payment Service|IMPS|
||National Automated Clearing House|NACH|
||Unified Payments Interface|UPI|
||Bharat Bill Payment System|BBPS|
||National Electronic Toll Collection|NETC|
||Cheque Truncation System|CTS|
||Aadhaar enabled Payment System|AEPS|
||BHIM Aadhaar Pay|BHIMAP|
|Card Networks (Visa, Mastercard, Rupay, Diners, Amex)|American Express Banking Corp., USA|AMEX|
||Diners Club International Ltd., USA|DINERS|

||Instrument Code||Payment Transaction Instrument|
|---|---|---|---|
|BNK||Bank Account||
|PAI||Paper Instruments||
|DEC||Debit Cards (including tokenised debit card or virtual debit card)||
|CRC||Credit Cards (including tokenised credit card or virtual credit card)||
|PPI||Pre-paid Payment Instruments (wallet or physical card)||
|OTH||Other Payment System Category||
||Payment System Code||Payment System Involved|
|ROP||RBI Operated Payment Systems (RTGS / NEFT)||
|NOP||NPCI Operated Payment Systems (IMPS, NACH, UPI, BBPS, NETC, CTS, AEPS, BHIM Aadhaar Pay)||
|CAN||Card Networks (VISA, Mastercard, Rupay, Diners, Amex)||

<!-- PAGE 15 -->

||MasterCard Asia / Pacific Pte. Ltd., Singapore|MASTER|
|---|---|---|
||National Payments Corporation of India (RuPay)|NPCI|
||Visa Worldwide Pte. Limited, Singapore|VISA|
|ATM Networks (list of authorised ATM networks);|Bank of India|BOIATM|
||Euronet Services India Private Limited|EURATM|
||National Payments Corporation of India (NFS)|NFSATM|
||Punjab National Bank|PNBATM|
||State Bank of India|SBIATM|
||Other – On Us Transaction|ONUS|
|Prepaid Payment Instrument Issuers|Prepaid Payment Instrument Issuers – Not Applicable|PPI-NA|
|Cross-Border Money Transfer Operators (list of authorised MTSS Principals);|Bahrain Financing Company, BSC (C)|BFCBSC|
||Continental Exchange Solutions Inc, USA Fast Encash Money Transfer Services Ltd. Mastercard Transaction Services (Canada) Inc.(formerly Transfast Inc., Canada and Global Foreign Exchange Inc.) MoneyGram Payment Systems Inc, USA. Muthoot Finserve USA Inc. {formerly Royal Exchange (USA) Inc.}|CESUSA FEMTSL TICCAN MGPUSA MUTUSA|
||UAE Exchange Centre LLC, UAE|UAEECL|
||Wall Street Exchange Centre LLC, UAE|WSEUAE|
||Western Union Financial Services Incorporated, USA|WUFUSA|
|TReDS (list of authorised TReDS entities);|A.TREDS Limited|ATREDS|
||Mynd Solutions Private Limited|MTREDS|
||Receivables Exchange of India Limited (RXIL)|RTREADS|
|Instant Money Transfer Operators – Not Applicable;|Instant Money Transfer Operators – Not Applicable;|IMTP-NA|
|Intra-Bank – Not Applicable;|Intra-Bank – Not Applicable;|INTRA-NA|
|Others – Not Applicable;|Others – Not Applicable;|OTH-NA|

<!-- PAGE 16 -->

## Payment Channel Used

## Payment Channel Used

|Payment Channel Code||
|---|---|
|BRN|Branch|
|INT|Internet (Online)|
|MBL|Mobile|
|ITB|Internet Banking|
|MOB|Mobile Banking|
|ATM|ATM|
|POS|POS|
|BCA|BC Agent|
|IVR|IVR|
|MOT|MOTO|
|OTH|Others Nature of Fraud|
|Fraud Nature Code|Nature of Fraud|
|ACH|Account Hacking / Compromise / Identity theft|
|PHH|Phishing|
|RMD|Remote Capture of Device|
|LSI|Lost / Stolen Device / Instrument|
|CRS|Card Skimming|
|VIS|Vishing|
|SMI|Smishing|
|SIS|SIM Swap|
|WBC|Website Cloning / Fraudulent Link|
|FRA|Fraudulent App|
|EHC|Email Hacking / Compromise|
|FMP|Forgery / Modification of Payment|
|MRC|Merchant Collusion|
|CLR|Collect Payment Request|
|OTH|Other|
