---
doc_id: "Notifications_2016_10449"
title: "Credit Information Reporting in respect of Self Help Group (SHG) members"
category: "Notifications"
year: 2016
source_rbi_url: "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/NT424602F1590EFE94E4DAB4E79D2126641BF.PDF"
pdf_sha256: "55b66e7dbdc14448902bb435dec2e9034d4279556b2113a41b07ad3e98cf0996"
md_sha256: "90c4efb9962ba9c398627199a38722d4692a74dadc1daee3cfcde3e95270a94a"
total_pages: 28
native_pages: 28
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T13:55:28Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Notifications/2016/2016-06-16_Notification_10449_Credit%20Information%20Reporting%20in%20respect%20of%20Self%20Help%20Group%20%28SHG%29%20members.pdf"
verification_status: "NEEDS_REVIEW"
---
# Credit Information Reporting in respect of Self Help Group (SHG) members

<!-- PAGE 1 -->

RBI/2015-16/424 DBR.CID.BC.No.104/20.16.56/2015-16 June 16, 2016

All Scheduled Commercial banks (including RRBs) All Non-Banking Financial Companies (NBFCs) All Primary (Urban) Co-operative Banks, State / Central Co-operative Banks All Credit Information Companies

## Dear Sir/Madam

## Credit Information Reporting in respect of Self Help Group (SHG) members

Please refer to the instructions contained in paragraph 6 of our <u>circular</u> <u>DBR.CID.BC.No.73/20.16.56/2015-16 dated January 14, 2016</u> advising banks to put in place necessary systems and procedures including making necessary changes to their systems software so as to be able to begin collection of the relevant information from the SHG members and the reporting of the required information to Credit 1 Information Companies (CICs).

2. It has been decided to incorporate the SHG member level data into the existing Microfinance data sharing file format issued vide our <u>circular</u> <u>DBOD.No.CID.BC.127/20.16.056/2013-14 dated June 27, 2014</u>. A mapping of the relevant individual SHG member level data of Table 3 of the <u>circular</u> <u>DBR.CID.BC.No.73/20.16.56/2015-16 dated January 14, 2016</u> to the relevant fields of Microfinance data sharing file format is enclosed in Annex I.
3. The modified view of Microfinance Data file format to be submitted to all the four CICs from July 1, 2016 is given in Annex II. Yours faithfully, (Rajinder Kumar) Chief General Manager Encl: As above 1 All Non-Banking Financial Companies (NBFCs) must also follow the directions contained in this circular if they finance SHGs.
_____________________________________________________________________________________________________________________ ___________________________ बकं ग व�नयमन वभाग, के न्द्रय कायार्लय, 13वी मंजील, के न्द्रय कायार्लय भवन, श. भगत संग मागर्, मुंबई -400 001 Department of Banking Regulation, Central Office, 13th Floor, Central Office Building, S. Bhagat Singh Marg, Mumbai - 400 001 टेलफोन/Tel.No.:91-22-22601000,टेलफोन/Tel.No.(D):91-22-22701297, फै क् स /Fax No. 91-22-22701239, email ID: <u>cgmicdbrco@rbi.org.in</u>

<u>�हन्द आसान है, इसका प्रयोग बढाइये</u> Caution: RBI never sends mails, SMSs or makes calls asking for personal information like bank account details, passwords, etc. It never keeps or offers funds to anyone. Please do not respond in any manner to such offers.

<!-- PAGE 2 -->

## Annex I

**Table 3**

## The following additions have been incorporated in Data Sharing document for “SHG data”.

## Fields as per RBI

## Available Field in Microfinance Data Sharing format

## Circular

Member Segment-Field No. 6,7,8 for Name of the Name Customer The nature of the identity Member Segment-Field No. 32, 34, 36 for Other ID Type document accepted by Description the bank Member Segment-Field No. 33, 35, 37 for Other ID Unique number of the Value; identity document Member Segment – Field No. 28 to 31 should be used for accepted by the bank, fields such as UID (Aadhaar), Voter’s ID, Ration Card if available Number.

|Date of birth|Member Segment-Field No. 10 for Member Birth Date|
|---|---|
|(DD/MM/YYYY)||
|Father’s /Husband’s|Member Segment-Field No. 17,18,19,20 for Member|
|Name|Relationship Details|
|Address (Complete|Address Segment – Field No. 60,61, 62 for Address,|
|address with State Code and PIN Code)|State Code and PIN Code|
|Male or Female|Member Segment-Field No. 13 for Member Gender|
||Type|
|Name of the SHG of|Member Segment-Field No. 5 for Group Identifier|
|which the person is a|The field has been modified to capture “Group Unique|
|member|ID^Group Name”|
|Savings Account|Member Segment-Field No. 45,46, 47 for Member’s|
|Number of the SHG|Savings Bank Details (Bank Name, Branch Code, Account #)|
|Loan Account Number of the SHG Reference number of|Account Segment-Field No. 66 for Account Number|
|any other identity document that has|Member Segment-Field No. 28-31 and 35, 37 for Other|

ID Value been relied upon by the bank

<!-- PAGE 3 -->

Not covered in existing format Educational level of *Member Segment: Field No. 42 has been changed from* the SHG member *Poverty Index to Educational Qualification.* Member Segment-Field No. 49 for Monthly Income Annual Income Suggest to continue with Monthly Income indicator

Occupation Member Segment-Field No. 48 for Occupation

Social Strata Member Segment-Field No. 52 for Member’s Caste

Member Segment-Field No. 39,41 for Member’s Phone Mobile Number Number

Amount availed by the Account Segment-Field No. 83 for Total Amount SHG member Disbursed

## The following additional changes has been affected in the format:

- Header Segment: Field# 3 Layout Version Number: For the new format, it is proposed to use version 3.2.
- Header Segment: Field# 9 Structure Indicator: It is proposed to use SHG for when the file contains SHG data, and JLG when the file contains JLG + Individual Data
- Member Segment: Field# 13 – A new possible value of T has been included to support Third/Trans Gender
- Member Segment: Field# 16,18,20,22,24,26 – Propose to reduce the list of relations to simplify
- Member Segment: Field# 43 – Asset Indicator and Poverty Index have been merged into one single field to allow capture of Member’s Educational Qualification
- Member Segment: Field#48 – Occupation – A list of possible values have been included in the Occupation field to support SHG reporting as recommended in the RBI circular dated Jan 14, 2016
- Member Segment: Field#52 – Member’s Caste/Social Strata – A list of possible values have been included in the Member’s Caste and Social Strata field to support SHG reporting as recommended in the RBI circular dated Jan 14, 2016. Also the

<!-- PAGE 4 -->

description of the field has been changed from Member’s Caste to “Member’s Caste/Social Strata”

- Member Segment: Field#53 – Member’s Role – The description of the field has been changed from Group Leader Indicator to “Member’s Role” to allow capture of SHG- specific roles as well. A list of possible values has been included, and the length of the field has been increased from 1 to 3.
- Member Segment: Field#55 – Member’s Status – The earlier Dummy field has been used to include a new field “Member’s Status” to indicate the individual’s engagement status within the Group. A list of possible values have been included and the field length has been reduced from 30 to 3.
- Member Segment Field #5 (or Account Segment Field # 72) – Group Identifier: This field now can capture Group Name if the Group ID is not available. If both are available, Group ID and Group Name both can be reported separated by a separator ^. The field length has been increased from 20 to 50.
- Account Segment: Field #71 – Loan Category – Additional types have been defined from T04 through T08 to accommodate different types of SHG data capture (SHG Individual: where the amount of lending is being tracked at individual level; SHG – Group: where the lent amount is being tracked at Group level only; SHG Group Govt: same as SHG Group but linked to a Government program; SHG-Group-Intra: same as Group but where intra group lending is happening)
- Account Segment: Field#75 – Account Status: A new status S15 has been introduced to allow reporting cancellation of loans which got booked in the system.
- Group Segment: A new segment has been introduced to capture group level details for SHG accounts. This segment is to be contributed only for SHG data.

<!-- PAGE 5 -->

## Annex II

# Microfinance Data Sharing File Format (Including SHG)

This document provides description of the file format for Microfinance data to be reported to Credit Bureau. This format follows Group, Consumer, Account structure – Multiple Groups, Each Group with Multiple Consumers and Each Consumer if taken credit has an account. It is recommended that a separate file is shared with CIC for SHG accounts and JLG + Individual accounts. All Microfinance borrowings in the names of the individuals, regardless of the purpose, should be included in this format. The data should contain all live loan accounts during the period, all accounts which got closed during the period and all accounts which opened during the period. Irrespective of the frequency of data sharing, the format of data sharing remains the same.

## Segments in Input File Format

The following table describes the different segments that make up the Data Input File Format

|#|Segment|Segment Tag|Option|Occurrences|Field Separator|
|---|---|---|---|---|---|
|1|Header|HDR|Required|Occurs once for a file|Fixed length separation|
|2|Group Segment|GRPCRD|Required|Occurs multiple times, as many Groups in the portfolio (only for SHG Groups)|Separated (¬ or ~ or Pipe “|”)|
|3|Member/ Consumer Segment|CNSCRD|Required|Occurs multiple times, as many customers in the Portfolio. Multiple Members exist under one Group|Separated (¬ or ~ or Pipe “|”)|
|4|Address Segment|ADRCRD|Required|One or more for every Consumer|Separated (¬ or ~ or Pipe “|”)|
|5|Account Segment|ACTCRD|Required|One or more for every Account|Separated (¬ or ~ or Pipe “|”)|
|6|Trailer|TRL|Required|Occurs once for a file|Fixed length|

*Note: ¬ is ASCII Character 170.*

<!-- PAGE 6 -->

## Header Segment (HDR)

The Header Record is the first segment of the data submission file. It is a required segment, only one Header segment is reported for each file and it is reported at the start of the File. It contains information necessary to identify the Member Institution and the Reporting date. It is a fixed length segment.

|#|Field Name|Option|Type|Length|Description|
|---|---|---|---|---|---|
|1|Segment Identifier|Required|AN|3|Must contain the value "HDR" to identify the Header Segment.|
|2|Name of Submission File|Required|AN|5|Contains the value "HMMFI" which indicates CRIF High Mark Microfinance Input File.|
|3|Layout Version Number|Required|AN|3|Indicates Input file format version number. Contains the value "3.2"|
|4|Submitting MEMBER ID|Required|AN|10|Must contain the unique member ID assigned by CRIF High Mark to the Member Institution.|
|5|Submitting MEMBER Name|Required|AN|30|Must contain the name of Member Institution submitting the file|
|6|Submitting Branch ID|Required When present|AN|30|Unique Branch ID assigned by CRIF High Mark to the Institution’s Branch for a decentralized data submission. Could be left blank, 30 spaces to be added if BLANK.|
|7|Reported Date|Required|D|8|Must contain the date "AS OF WHICH" the data is being reported to CRIF High Mark. If records in the file are updated on different dates, use the most recent date. Valid calendar date in the DDMMYYYY format|
|8|File Creation Date/ Extraction Date|Required|D|8|The date when the file was created, which must be equal to or later than date in the Date Reported Field. Valid calendar date in DDMMYYYY format. For example, Date Reported is August 31, 2007. If the file was extracted on September 7, 2007 and submitted to CRIF High Mark on September 8, 2007, then the file creation date will be September 7, 2007, i.e. 07092007.|

<!-- PAGE 7 -->

|9|Organization Data Structure Indicator|Required|AN|3|Contains the organization's account or Customer structure. SHG for SHG data JLG for JLG + Individual Data|
|---|---|---|---|---|---|
|10|Password|Required|AN|30|Must contain the encrypted password assigned by CICs to the Member Institution|
|11|System Vendor Identifier|Required when available|AN|30|A unique identifier agreed upon to identify the vendor of Member Institution, furnishing the data, in case Vendor system is being used. For in-house developed system, specify "INHOUSE ". Could be left blank, 30 spaces to be added if BLANK|
|12|Vendor System Version Identifier|Required when available|AN|10|The version of the system used to furnish the data in case Vendor system is being used. For In-house developed system, specify "INHOUSE ". Could be left blank, 10 spaces to be added if BLANK|
|13|Reserved for Future Use||AN|20|Reserved for Future Use|

## Group Segment (GRPCRD)

The Group Segment is the second segment in the data submission file. It contains the information necessary to identify the Group (only for SHG). It is present once per Group. Each Group can many customers/members within it. This is a required segment if Loan Category is T04 or T05 or T06 or T07.

## Ty Len

## # Field Name Option Description pe gth

1 Segment Identifier A/N 6 Required Must contain the value "GRPCRD" to identify the Member/Consumer Segment. 2 Group Identifier A/N 50 Required Unique Group Identifier used by the Member Institution to identify the Group uniquely. 3 Group Name A/N 200 Required Name of the SHG Group

<!-- PAGE 8 -->

|4|Group Loan Account Number|A/N|30|Required|Loan Account Number of the Group as in the Bank’s records|
|---|---|---|---|---|---|
|5|Disbursed Amount (Rs)|N|9|Required|Total Disbursed amount for this loan (in Rupees)|
|6|Outstanding Balance (Rs)|N|9|Required|Total outstanding principal for this loan (in Rupees)|
|7|Date Opened/Disbursed|D|8|Required|Valid calendar date in DDMMYYYY format|
|8|Date Closed (if closed)|D|8|Required When present|Valid calendar date in DDMMYYYY format|
|9|Date of last payment|D|8|Required When present|Valid calendar date in DDMMYYYY format|
|10|Number of Installments|N|3|Required When present|Original Number of installments at the time of disbursement|
|11|Repayment Frequency|A/N|3|Required|Enumeration: F01- Weekly F02 - Biweekly F03 - Monthly F04- Bimonthly F05- Quarterly F06- Semi-annually F07-Annually F08-Single Payment Loan (bullet / balloon) F10-Other|
|12|Instalment Amount|N|9|Required|Installment Amount for the Loan (Rs)|
|13|Amount Overdue (Rupees)|N|9|Required|Amount which is due past the payment date|
|14|DPD (Days past due)|A/N|3|Required|Enumeration: 000 = 0 payments past due (current account) with Positive Balance 001 to 999 = Number days past due. If an account is above 999 days, mark as 999 XXX = No payment history available for this month|
|15|Loan Cycle ID|N|3|Required When present|Renewal cycle number of the Group|
|16|Loan Type (Term or Cash Credit)|A/N|10|Required|C01-Term Loan C02-Cash Credit|
|17|Write Off Amount (Rupees)|N|9|Required When present||
|18|Date Write-Off (if written-off)|D|8|Required When present||

<!-- PAGE 9 -->

|19|Write-off reason (if written off)|A/N|20|Required When present|Enumeration: X01- First Payment Default X02-Death X03-Willful Default Status X04-Suit Filed, Willful Default Status X09-Untagged X10 - Not Applicable|
|---|---|---|---|---|---|
|20|Groups’ Communication Address|A/N|200|Required when present|Communication Address for the Group-as per address proof document (Number, Village/Taluk, Landmark, District)|
|21|State Code (Groups’ Communication Address)|N|2|Required if Address is provided|Must be a code as defined in Appendix A|
|22|Pin Code (Groups’ Communication Address)|N|10|Required if Address is provided|Valid 6 digit PIN Code|
|23|Telephone Number 1 type Indicator|A/N|3|Required When present|Telephone / contact information details Enumeration: P01-Residence P02-Company P03- Mobile P04-Permanent P07-Other P08-Un tagged|
|24|Group Telephone Number 1|A/N|15|Required When present|Group’s telephone number (contact)|
|25|Group’s Bank Account-Bank Name|A/N|50|Required|Name of the Bank where the group has a savings bank account|
|26|Group’s Bank Account-Branch Name|A/N|50|Required|IFSC Code (preferred) or Name of the Bank Branch where the group has a savings bank account|
|27|Group’s Bank Account-Account Number|A/N|35|Required|Account Number of group’s savings bank account|
|28|Group’s Bank Account-Account Balance|N|10|Required if available|Account Balance (in Rupees) of group’s savings bank account|
|29|First Created Date|D|8|Required if available|Date when the Group was formed|
|30|First Linkage Date|D|8|Required if available|Date when the Group was first linked for credit|

<!-- PAGE 10 -->

|31|Group Identifier (Govt)|A/N|30|Required if available|Identifier for the Group as captured with Government|
|---|---|---|---|---|---|
|32|Linked to a Govt program|A/N|20|Required if available|U01- NRLM U02-NULM U03-SRLM U04-MEPMA U99-Others|
|33|SHPI/NGO Identifier|A/N|30|Required if available|Identifier for the NGO/SHPI as captured with the Member Institution|
|34|SHPI/NGO Name|A/N|100|Required if available|Name of NGO/SHPI involved in Group Formation|
|35|SHPI/NGO Officer Name|A/N|100|Required if available|Name of NGO/SHPI Personnel involved in Group Formation/Linkage|
|36|SHPI/NGO Address (with State and Pincode)|A/N|100|Required if available|Address of NGO/SHPI involved in Group Formation (Street, Village/Locality, Taluk, District, State, Pin Code)|

## Member/Consumer Segment (CNSCRD)

The Member/Consumer Segment is the third segment in the data submission file. It contains the information necessary to identify the Customer like name, date of birth, the identification numbers like Voters ID, Aadhaar (UID), Driving License and so on. It is present once per Customer. For group loans, Customer means Individual Member within the group.

It is a good practice that the key demographic details of the individual member (name, address, father/spouse name, age, Date of Birth) are captured exactly from one of the standard KYC Identifiers, preferably from UID/Aadhaar, Voter ID, Ration card or MNREGA Job Card.

## Typ Lengt

## # Field Name Option Description e h

1 Segment Identifier A/N 6 Required Must contain the value "CNSCRD" to identify the Member/Consumer Segment. 2 Member Identifier A/N 35 Required Unique customer identification number used by the Member institution 3 Branch Identifier A/N 30 Required Unique branch code of the when Member Institution where the present customer was originally enrolled. Could be left blank if not

<!-- PAGE 11 -->

||||||available|
|---|---|---|---|---|---|
|4|Kendra/Centre Identifier|A/N|30|Required when present|Unique center code of the Member Institution where the customer was originally enrolled Could be left blank if not available|
|5|Group Identifier|A/N|50|Required When present|Unique group Identifier used by the Member Institution where the Customer had originally enrolled. Or Group Name to be provided here. If both are present, then Group ID^Group Name (separator as ^) This is a required field if Loan Category is T01 or T02 or T04 or T05 or T06 or T07|
|6|Member Name 1|A/N|100|Required|Name of the Customer (First Name)|
|7|Member Name 2|A/N|50|Required When present|Name of the Customer (Middle Name)|
|8|Member Name 3|A/N|50|Required When present|Name of the Customer (Last Name)|
|9|Alternate Name of Member|A/N|30|Required When present|If any alias or maiden name of the Customer is captured.|
|10|Member Birth Date|D|8|Required|Date of birth of Customer. Valid Calendar date in DDMMYYYY format. Could be left blank if Age & Age as on is captured|
|11|Member Age|N|3|Required|If instead of DOB, age is captured then the age as captured at the time of membership. Could be left blank if DOB is captured.|
|12|Member's age as on date|D|8|Required|Date on which the age was recorded-to identify the current age Valid Calendar date in DDMMYYYY format. Could be left blank if DOB is captured|
|13|Member Gender Type|A/N|1|Required|Enumerated: F-Female M – Male T-Third/Trans Gender|

<!-- PAGE 12 -->

|14|Marital Status Type|A/N|3|Required when present|Enumerated: M01 - Married M02 - Separated M03- Divorced M04 - Widowed M05 - Unmarried M06 - Untagged Could be left blank if not available|
|---|---|---|---|---|---|
|15|Key Person's name*|A/N|100|Required when present|Guardian's name. Either Key Person/Member Relationship/Nominee details need to be filled|
|16|Key Person's relationship|A/N|3|Required when Key Person’s Name is populate d|Enumerated: K01 - Father K02 - Husband K03- Mother K04 -Son K05 -Daughter K06-Wife K15 –Other|
|17|Member relationship Name 1*|A/N|100|Required|Relative name. Either Key Person/Member Relationship/Nominee details need to be filled.|
|18|Member relationship Type 1|A/N|3|Required when Member Relation ship Name 1 is populate d|Enumerated: K01 - Father K02 - Husband K03- Mother K04 -Son K05 -Daughter K06-Wife K15 -Other|
|19|Member relationship Name 2*|A/N|100|Required when present||

<!-- PAGE 13 -->

|20|Member relationship Type 2|A/N|3|Required when Member Relation ship Name 2 is populate d|Enumerated: K01 - Father K02 - Husband K03- Mother K04 -Son K05 -Daughter K06-Wife K15 –Other|
|---|---|---|---|---|---|
|21|Member relationship Name 3*|A/N|100|Required when present||
|22|Member relationship Type 3|A/N|3|Required when Member Relation ship Name 3 is populate d|Enumerated: K01 - Father K02 - Husband K03- Mother K04 -Son K05 -Daughter K06-Wife K15 -Other|
|23|Member relationship Name 4*|A/N|100|Required when present||
|24|Member relationship Type 4|A/N|3|Required when Member Relation ship Name 4 is populate d|Enumerated: K01 - Father K02 - Husband K03- Mother K04 -Son K05 -Daughter K06-Wife K15 -Other|
|25|Nominee Name*|A/N|100|Required when present|Nominee for insurance purposes if defined. Either Key Person/Member Relationship/Nominee details need to be filled|

<!-- PAGE 14 -->

|26|Nominee relationship|A/N|3|Required when Nominee Name is populate d|Enumerated: K01 - Father K02 - Husband K03- Mother K04 -Son K05 -Daughter K06-Wife K15 -Other|
|---|---|---|---|---|---|
|27|Nominee Age|N|3|Required when Nominee Name is populate d|In years as of today|
|28|Voter's ID*|A/N|20|Required When present||
|29|UID*|A/N|40|Required When present|Aadhaar|
|30|PAN*|A/N|15|Required When present||
|31|Ration Card*|A/N|20|Required When present||
|32|Member Other ID 1 Type description|A/N|20|Required When present|Reserved for NREGA ID. If NREGA ID is captured, then put “NREGA” in this field|
|33|Member Other ID 1*|A/N|30|Required When present|If NREGA ID is captured, then Identifier Number to be captured here|
|34|Member Other ID 2 Type description|A/N|20|Required When present|If any other id is captured, then information about such id|
|35|Member Other ID 2*|A/N|30|Required When present|If any other id is captured, then information about such id|
|36|Other ID 3 Type|A/N|20|Required When present|If any other id is captured, then information about such id|
|37|Other ID 3 Value*|A/N|30|Required When present|If any other id is captured, then information about such id|

<!-- PAGE 15 -->

|38|Telephone Number 1 type Indicator|A/N|3|Required When present|Telephone / contact information details Enumeration: P01-Residence P02-Company P03- Mobile P04-Permanent P07-Other P08-Un tagged|
|---|---|---|---|---|---|
|39|Member Telephone Number 1|A/N|15|Required||
|40|Telephone Number 2 type Indicator|A/N|3|Required When present|Enumeration: P01-Residence P02-Company P03- Mobile P04-Permanent P07-Other P08-Un tagged|
|41|Member Telephone Number 2|A/N|15|Required When present||
|42|Member’s Educational Qualification|A/N|3|Required|Educational Qualification of the Customer (Individual Member) Enumeration: Y01: Illiterate Y02: Passed 5th class Y03: Passed 8th class Y04: Passed 10th class th Y05: Above 10|
|43|Asset ownership indicator/Poverty Index|A/N|3|Required When present|If the customer has any assets, then mark Y Enumeration: Y- Yes N- No If Poverty Index is available, then it is to be directly supplied. Provide poverty index (if calculated internally by the Member Institution) or related details such as BPL, etc|
|44|Number of Dependents|N|2|Required When present|Dependent family members|
|45|Bank Account-Bank Name|A/N|50|Required|Name of the Bank where the customer has a savings bank|

<!-- PAGE 16 -->

||||||account|
|---|---|---|---|---|---|
|46|Bank Account-Branch Name|A/N|50|Required|IFSC Code (preferred) or Name of the Bank Branch where the customer has a savings bank account|
|47|Bank Account-Account Number|A/N|35|Required|Account Number of customer’s savings bank account|
|48|Occupation|A/N|50|Required When present|Occupation/Profession of the Customer Enumeration: Z01- Home Maker Z02- Landless labourer Z03- Marginal Farmer Z04- Small farmer Z05- Non-farming Z06- Others|
|49|Total Monthly Family Income|N|9|Required|In Rupees, no decimal|
|50|Monthly Family Expenses|N|9|Required|In Rupees, no decimal|
|51|Member's Religion|A/N|3|Required When present|Customer’s Religion Enumeration: R01 - Hindu R02 - Muslim R03 - Christian R04 - Sikh R05 - Buddhist R06 - Jain R07 - Bahai R08 - Others R09 - Religion not stated|
|52|Member's Caste or Social Strata|A/N|30|Required|Customer’s Caste Enumeration: V01 - SC V02 - ST V03 - OBC V04 - NT/VJ (Vimukta Jati and Nomadic Tribes) V05 - General V08 - Others V09 - Untagged|
|53|Member’s Role|A/N|3|Required When present|Indicator for the role of Customer within the group Enumeration: L01- Leader/President/Office- bearer|

<!-- PAGE 17 -->

||||||L02- Associate/Secretary L03-Member L04- Untagged|
|---|---|---|---|---|---|
|54|Center Leader indicator|A/N|1|Required When present|Is the customer a center leader Enumeration: Y- Yes N- No U- Untagged|
|55|Member’s Status|A/N|3|Required When present|Indicator for the engagement status of the Member within the Group Enumeration: W01- Active (Loanee Member) W02- Inactive/Dormant (Non- loanee member) W03-Exited W04-Untagged|
|*|most widely-used identifiers.||one of Relationship details (Key Person’s Name, Member Relationship Name, Nominee Name) or KYC IDs (Voter’s ID, UID/Aadhaar, Ration Card, PAN, Other IDs) is required. For the Microfinance customers, UID/Aadhaar, Voter’s ID, Ration Card Number and NREGA ID are|||

<!-- PAGE 18 -->

## Address Segment (ADRCRD)

The Address Segment is the fourth segment in the data submission file. It contains the addresses of the customer-permanent address and present address for a customer along with state code and PIN code. One address segment is mandatory per Member segment.

|#|Field Name|Ty pe|Lengt h|Option|Description|
|---|---|---|---|---|---|
|56|Segment Identifier|A/N|6|Require d|Must contain the value "ADRCRD" to identify the Address Segment.|
|57|Member's Permanent Address|A/N|200|Require d when present|Permanent address of the Customer- as per address proof document|
|58|State Code (Permanent Address)|N|2|Require d if Perman ent Addres s is provide d|Must be a code as defined in Appendix A|
|59|Pin Code (Permanent Address)|N|10|Require d if Perman ent Addres s is provide d|Valid 6 digit PIN Code|
|60|Member's Current Address|A/N|200|Require d|Present or Communication address of the Customer-if not residing in permanent address. If only 1 address is available, provide the same as current address|
|61|State Code (Current Address)|N|2|Require d|Must be a code as defined in Appendix A|
|62|Pin Code (Current Address)|N|10|Require d|Valid 6 digit PIN Code|
|63|Dummy|A/N|30|Require d When present|No input required Reserved for future use|

Note: It is advisable to capture the address exactly from one of the KYC Identifiers

<!-- PAGE 19 -->

## Account Segment (ACTCRD)

The Account Segment is the fifth segment within the data submission file. It contains the financial information related to account such as account number, type of credit product, original and current terms and repayment information. More than one Account segment can be present for one Customer segment.

|#|Field Name|Type|Lengt h|Option|Description|
|---|---|---|---|---|---|
|64|Segment Identifier|A/N|6|Required|Must contain the value "ACTCRD" to identify the Account Segment.|
|65|Unique Account Reference number|A/N|35|Required|This field will not change even if the Account number changes, it can have customer ID. This field must be consistent on each submission basis to avoid duplication of information. In case of a branch split or branch join where the account number changes within the tenor of the loan, the original loan account number should be shown here.|
|66|Account Number|A/N|35|Required|Account number of the loan account. Will be same as previous field if no split or branch combination has happened during the tenor of the loan.|
|67|Branch Identifier|A/N|30|Required when present|Unique branch code where the loan account is held currently. Could be left blank if not available|
|68|Kendra/Centre Identifier|A/N|30|Required when present|Unique center code where the loan account is held currently Could be left blank if not available|
|69|Loan Officer originating the loan|A/N|30|Required when present|Employee Code of Officer originating the loan Could be left blank if not available|
|70|Date of Account Information|D|8|Required|Date on which Account was last updated. Valid calendar date in DDMMYYYY format|
|71|1 Loan Category|A/N|3|Required|Enumeration: T01- JLG Group T02- JLG Individual T03 - Individual T04 - SHG Group T05 - SHG Individual|

1 JLG-Individual: JLG loan where lending is being tracked at individual level; JLG-Group: JLG loan where lending is being tracked at group level; Individual: Individual Microfinance loan (not JLG or SHG) – this loan should either be reported in this format or in the consumer data format but not in both formats; SHG Individual: where the amount of lending is being tracked at individual level; SHG – Group:where the lent amount is being tracked at Group level only; SHG Group Govt: same as SHG Group but linked to a Government program; SHG-Group-Intra: same as Group covering intra group lending.

<!-- PAGE 20 -->

||||||T06 - SHG Group-Govt T07 - SHG Intra-Group T08 - Others|
|---|---|---|---|---|---|
|72|Group Identifier|A/N|50|Required When present|Required field if Loan Category is T01 or T02 or T04 or T05 or T06 or T07 This is the unique group code assigned by the Member Institution. Group Name to be provided here. If both are present, then provide it as “Group ID^Group Name”|
|73|Loan Cycle-id|A/N|30|Required When present|Renewal cycle number of the customer with the Member Institution|
|74|Loan Purpose|A/N|20|Required|Purpose of the loan|
|75|Account Status|A/N|3|Required|Enumeration: S01 - Loan Submitted S02 - Loan Approved-Not yet disbursed S03 - Loan Declined S04 - Current S05 - Delinquent S06 - Written Off S07 - Account Closed S15 – Cancelled|
|76|Application date|D|8|Required When present|Valid calendar date in DDMMYYYY format|
|77|Sanctioned Date|D|8|Required When present|Valid calendar date in DDMMYYYY format|
|78|Date Opened/Disburs ed|D|8|Required|Valid calendar date in DDMMYYYY format|
|79|Date Closed (if closed)|D|8|Required When present|Required if account status is S07. Valid calendar date in DDMMYYYY format|
|80|Date of last payment|D|8|Required When present|Valid calendar date in DDMMYYYY format|
|81|Applied For amount|N|9|Required When present|Amount applied for in the application|
|82|Loan amount Sanctioned|N|9|Required|Could be replicated with value under Total Amount Disbursed (Rupees)|
|83|Total Amount Disbursed (Rupees)|N|9|Required|Amount disbursed|
|84|Number of Installments|N|3|Required When|Original Number of installments at the time of disbursement|

<!-- PAGE 21 -->

|||||present||
|---|---|---|---|---|---|
|85|Repayment Frequency|A/N|3|Required|Enumeration: F01- Weekly F02 - Biweekly F03 - Monthly F04- Bimonthly F05- Quarterly F06- Semi-annually F07-Annually F08-Single Payment Loan (bullet / balloon) F10-Other|
|86|Minimum Amount Due/Instalment Amount|N|9|Required|Installment Amount for the Loan|
|87|Current Balance (Rupees)|N|9|Required|Only principal outstanding on the loan|
|88|Amount Overdue (Rupees)|N|9|Required|Amount which is due past the payment date|
|89|DPD (Days past due)|A/N|3|Required|Enumeration: 000 = 0 payments past due (current account) with Positive Balance 001 to 999 = Number days past due. If an account is above 999 days, mark as 999 XXX = No payment history available for this month|
|90|Write Off Amount (Rupees)|N|9|Required When present|Required if account status is S06|
|91|Date Write-Off (if written-off)|D|8|Required When present|Required if account status is S06. Valid calendar date in DDMMYYYY format|
|92|Write-off reason (if written off)|A/N|20|Required When present|Enumeration: required if account status is S06 X01- First Payment Default X02-Death X03-Willful Default Status X04-Suit Filed, Willful Default Status X09-Untagged X10 - Not Applicable|
|93|No. of meetings held|N|3|Required When present|Number of center meetings held since the loan disbursement|
|94|No. of meetings missed|N|3|Required When present|Number of center meetings out of the above which the customer has not attended|
|95|Insurance Indicator|A/N|1|Required When|Enumeration: Y- Yes|

<!-- PAGE 22 -->

|||||present|N- No|
|---|---|---|---|---|---|
|96|Type of Insurance|A/N|3|Required When present|Enumeration: L01 - Life Insurance L02 - Credit Insurance L03 - Health/Medical Insurance L04 - Property Insurance L05 - Liability Insurance L10 – Other|
|97|Sum Assured/Covera ge|N|10|Required When present|Sum Assured for the Insurance|
|98|Agreed meeting day of the week|A/N|3|Required When present|Enumeration: MON-Monday TUE-Tuesday WED-Wednesday THU-Thursday FRI-Friday SAT-Saturday SUN-Sunday|
|99|Agreed Meeting time of the day|A/N|5|Required When present|Should be in HH:MM format|
|100|Dummy|A/N|30|Required When present|Reserved for future use|

<!-- PAGE 23 -->

## Trailer Segment (TRL)

The Trailer Record is the last segment of the credit reporting file. This segment is a required segment, appears only once per file and indicates end of the file. It is a fixed length segment.

|#|Field Name|Option|Type|Length|Description|
|---|---|---|---|---|---|
|1|Segment Identifier|Required|AN|3|Must contain the value "TRL" to identify the Trailer Segment.|
|2|Layout Version Number|Required|AN|3|Indicates Input file format version number. Contains the value "3.0"|
|3|Submitting Member ID|Required|AN|10|Must contain the unique Member ID assigned by CRIF High Mark to the Member Institution.|
|4|Reserved for Future Use||AN|20|Reserved for Future Use|

<!-- PAGE 24 -->

## Glossary

|Term|Description|
|---|---|
|D|Date|
|N|Numeric data|
|A/N|Alphanumeric|

## Catalogues

## <u>Annexure</u> A: State

|Code|Description|Code|Description|
|---|---|---|---|
|AN|Andaman and Nicobar Islands|LD|Lakshadweep|
|AP|Andhra Pradesh|MH|Madhya Pradesh|
|AR|Arunachal Pradesh|ML|Maharashtra|
|AS|Assam|MN|Manipur|
|BR|Bihar|MP|Meghalaya|
|CG|Chandigarh|MZ|Mizoram|
|CH|Chhattisgarh|NL|Nagaland|
|DD|Dadra and Nagar Haveli|OR|Orissa|
|DL|Delhi|PB|Punjab|
|DN|Daman and Diu|PY|Puducherry|
|GA|Goa|RJ|Rajasthan|
|GJ|Gujarat|SK|Sikkim|
|HP|Haryana|TN|Tamil Nadu|
|HR|Himachal Pradesh|TR|Tripura|
|JH|Jammu and Kashmir|TS|Telangana State|
|JK|Jharkhand|UK (Formerly UA)|Uttarakhand|
|KA|Karnataka|UP|Uttar Pradesh|
|KL|Kerala|WB|West Bengal|

<!-- PAGE 25 -->

## Sample Structure

## Header Segment

|Segment Identifier|HDR|
|---|---|
|Name of Submission File|HMMFI|
|Layout Version Number|3.2|
|Submitting MEMBER ID|XXXXXXXXXX|
|Submitting MEMBER Name|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
|Submitting Branch ID|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
|Reported Date|31032016|
|File Creation Date/ Extraction Date|12042016|
|Organization Member Structure Indicator|XXX|
|Password|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
|System Vendor Identifier|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
|Vendor System Version Identifier|XXXXXXXXXX|
|Reserved for Future Use|XXXXXXXXXXXXXXXXXXXX|

## Trailer Segment

|Segment Identifier|TRL|
|---|---|
|Layout Version Number|3.0|
|Submitting Member ID|XXXXXXXXXX|
|Reserved for Future Use|XXXXXXXXXXXXXXXXXXXX|

<!-- PAGE 26 -->

## Data Segment

|Segment Identifier|A/N|CNSCRD|
|---|---|---|
|Member Identifier|A/N|12345678|
|Branch Identifier|A/N|9003|
|Kendra/Centre Identifier|A/N|039003|
|Group Identifier|A/N|039001^INDIRA SHG|
|Member Name 1|A/N|ANITA JAYANT NATH|
|Member Name 2|A/N||
|Member Name 3|A/N||
|Alternate Name of Member|A/N||
|Member Birth Date|(DDMMYYYY)|01011975|
|Member Age|N|39|
|Member's age as on date|DDMMYYYY)|31012015|
|Member Gender Type|A/N|F|
|Marital Status Type|A/N|M01|
|Key Person's name|A/N|JAYANT NATH|
|Key Person's relationship|A/N|K02|
|Member relationship Name 1|A/N||
|Member relationship Type 1|A/N||
|Member relationship Name 2|A/N||
|Member relationship Type 2|A/N||
|Member relationship Name 3|A/N||
|Member relationship Type 3|A/N||
|Member relationship Name 4|A/N||
|Member relationship Type 4|A/N||
|Nominee Name|A/N|JAYANT NATH|
|Nominee relationship|A/N|K02|
|Nominee Age|N||
|Voter's ID|A/N||
|UID|A/N||
|PAN|A/N||
|Ration Card|A/N||
|Member Other ID 1 Type description|A/N|VOTER ID|
|Member Other ID 1|A/N|Value1|
|Member Other ID 2 Type description|A/N||
|Member Other ID 2|A/N||
|Other ID 3 Type|A/N||
|Other ID 3 Value|A/N||
|Telephone Number 1 type Indicator|A/N|P03|
|Member Telephone Number 1|A/N|8754698XXX|
|Telephone Number 2 type Indicator|A/N||
|Member Telephone Number 2|A/N||
|Member’s Educational|A/N||

<!-- PAGE 27 -->

|Qualification|||
|---|---|---|
|Asset ownership indicator/ Poverty Index|A/N||
|Number of Dependents|N|2|
|Bank Account-Bank Name|A/N||
|Bank Account-Branch Name|A/N||
|Bank Account-Account Number|A/N||
|Occupation|A/N||
|Total Monthly Family Income|N||
|Monthly Family Expenses|N||
|Member's Religion|A/N|R08|
|Member's Caste|A/N||
|Member’s Role|A/N|L01|
|Centre Leader indicator|A/N|Y|
|Member’s Status|A/N|W01|
|Segment Identifier|A/N|ADRCRD|
|Member's Permanent Address|A/N|LAING PART ,LAING,RAJGANGPUR,SUNDARGARH|
|State Code (Permanent Address)|N|OR|
|Pin Code (Permanent Address)|N|770017|
|Member's Current Address|A/N|LAING PART ,LAING,RAJGANGPUR,SUNDARGARH|
|State Code (Current Address)|N|OR|
|Pin Code (Current Address)|N|770017|
|Address|A/N||
|Segment Identifier|A/N|ACTCRD|
|Unique Account Reference number|A/N|039000012|
|Account Number|A/N|123456|
|Branch Identifier|A/N|9003|
|Kendra/Centre Identifier|A/N|039003|
|Loan Officer for Originating the loan|A/N|ABC XYZ|
|Date of Account Information|D (DDMMYYYY)|03102015|
|Loan Category|A/N|T04|
|Group Identifier|A/N|039001^INDIRA SHG|
|Loan Cycle-id|A/N|1|
|Loan Purpose|A/N|SEA|
|Account Status|A/N|S04|
|Application date|(DDMMYYYY)|04022014|
|Sanctioned Date|(DDMMYYYY)|28022014|
|Date Opened/Disbursed|(DDMMYYYY)|28022014|
|Date Closed (if closed)|(DDMMYYYY)||
|Date of last payment|(DDMMYYYY)|08032016|

<!-- PAGE 28 -->

|Applied For amount|N|15000|
|---|---|---|
|Loan amount Sanctioned|N|15000|
|Total Amount Disbursed (Rupees)|N|15000|
|Number of Installments|N|24|
|Repayment Frequency|A/N|F03|
|Minimum Amt Due/Instalment Amount|N|808|
|Current Balance (Rupees)|N|4599|
|Amount Overdue (Rupees)|N|0|
|DPD (Days past due)|A/N|0|
|Write Off Amount (Rupees)|N||
|Date Write-Off (if written-off)|DDMMYYYY)||
|Write-off reason (if written off)|A/N||
|No. of meetings held|N|45|
|No. of meetings missed|N|22|
|Insurance Indicator|A/N||
|Type of Insurance|A/N||
|Sum Assured/Coverage|N||
|Agreed meeting day of the week|A/N||
|Agreed Meeting time of the day|A/N||
|Dummy|A/N||
