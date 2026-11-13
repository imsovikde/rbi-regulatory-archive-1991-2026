---
doc_id: "Circulars_2014_RBI_2013-2014_651_DPSS_CO_RTGS_No_2589_04_04_017_2013-14"
title: "New features in RTGS System"
category: "Circulars"
year: 2014
source_rbi_url: "https://rbidocs.rbi.org.in/rdocs/Notification/PDFs/NFR200614FS.PDF"
pdf_sha256: "fc00b6781d775282807e516b2bb873bfaa6dd3c85b0174bea41689a4239992f2"
md_sha256: "7898b8fbfd1e1499c3ce53c0d131e9b5914578aaa17decdf5ab611e9bb7c7bd4"
total_pages: 5
native_pages: 5
ocr_pages: 0
conversion_engine: "firecrawl-anydoc 0.2.4"
converted_at_utc: "2026-11-13T10:11:18Z"
source: "hf"
source_hf_url: "https://huggingface.co/datasets/imsovikde/rbi-regulatory-archive-1991-2026/resolve/main/Circulars/2014/2014-06-20_Circular_RBI-2013-2014-651%20DPSS%20%28CO%29%20RTGS%20No.2589-04.04.017-2013-14_New%20features%20in%20RTGS%20System.pdf"
verification_status: "VERIFIED_LEVEL_5"
---
# New features in RTGS System

<!-- PAGE 1 -->

RBI/2013–14/651 DPSS (CO) RTGS No. 2589 / 04.04.017 / 2013-14 June 20, 2014

The Chairman / Managing Director / Chief Executive Officer of participants of RTGS

Madam / Sir, <u>New features in RTGS System</u>

# <u>2026</u>

Please refer to our <u>circular DPSS (CO) RTGS No.801/04.04.017/2013-14 dated October 11</u>, 7, <u>2013</u> regarding the launch of new RTGS system and coming into effect of “<u>RTGS System</u>

# April

<u>Regulations 2013</u>”. A reference is also invited to Chapter 9 of the “RTGS System Regulations 2013” wherein it had been indicated that the new features in RTGS system will be enabledfromafter due notifications to members. effect

2. The new RTGS system has been running smoothly and has stabilised. It has hence beenwith decided to enable the ‘Hybrid’ and ‘Future value dated transactionv1.0’ features in the system with effect from July 14, 2014. The details regarding operations of these two functionalities are given in Annex.
# Regulations

3. The Hybrid feature will be configured to do off-setting every 5 minutes. The transactions with normal priority would be settled in off-setting mechanism, with a maximum of two attempts i.e.
# System

the maximum time a transaction would be in “normal” queue is 10 minutes. If the transactions with normal priority are unable to be settled in offsetting mode within this time, the priority of the

# RTGS

transaction would be automatically changed to “urgent”. The parameter value will be set to 10%. into This means that 10% of the balance in the settlement A/c would be taken for settlement in the offsetting mode.

# Subsumed

4. The Future Value dated Transaction would enable the customers / participants to initiate RTGS transactions 3 working days in advance for settling in RTGS on value date.
5. The circular is issued under section 10 (2) of Payment and Settlement Systems Act 2007, (Act 51 of 2007). Yours faithfully, Vijay Chugh Chief General Manager
## Encl: As above.

<!-- PAGE 2 -->

## Annex

## 1. Hybrid feature

a) The RTGS system supports a new and unique way to handle large volume of payments using a minimum amount of liquidity from the Participants’ settlement accounts.
b) From the priority point of view, the RTGS system can handle two types of payments:
(i) Urgent payments (ii) Normal payments
c) Both categories are implemented over the same ISO20022 standard and share the same rules and regulations. However, while the urgent payments are processed as soon as they are received by the RTGS and using as much liquidity as required from the2026
7, settlement account of the sending Participant, the normal payments are processed

# April

differently, following some strict processing rules which do not apply to the urgent payments. These rules are: from

i. The normal payments are not settled immediately, even though the sending bank
effect may have sufficient funds in its settlement account; with ii. The normal payments may settle only at periodic time intervals which are controlled centrally by system parameter of RTGS;v1.0 iii. The RTGS does not take into consideration the pending normal transactions in the calculation for IDL funding request to CBS; iv. The settlement of normal payments can occur only if several participants, Regulations simultaneously, have sent normal payments to each other. If 0 % of allowance is set in parameter value (centrally), in that scenario the transactions would look for System settling transactions without using any amount from the settlement account, i.e.,

# RTGS

settlement will happen purely on offsetting mode. If an allowance of 1% is set in into the parameter in that scenario, the transactions would try to settle using a percentage of the amount from the settlement account.

v. If the condition for the settlement of normal payments is not possible, the system Subsumed will automatically promote the normal payments to the urgent payment stream, after a predefined timeout parameter. Once promoted, the transactions will be processed according to the urgent payments’ settlement rules. vi. From the format point of view, the field that designates a payment as normal or urgent is called **InstrPrty** and its content should be: NORM – for normal payments HIGH – for urgent payments

<!-- PAGE 3 -->

## Process flow

The normal payments will have the following flow in RTGS:

1. A new normal message is received, validated and (if successful) placed in the ENTER status queue.
2. The item will stay with status ENTER until the first gridlock cycle for the normal stream runs. After the cycle is completed, the item will change its status to COMPLETE (if the item was settled) or PENDING (if the item was not included in any gridlock solution).
3. Subsequent gridlock cycles will attempt to settle the item (every 5 minutes), considering other normal payments found in the system. If a solution is found by the
# 2026

normal payment stream gridlock resolution process, the respective transactions are 7, updated to status COMPLETE and the respective output messages are generated to

# April

the sender and receiver.

4. If a solution is not found within the timeout period (10 minutes) for the normal from payments, the item is promoted to the urgent stream. The change is visible to the
effect end user when listing the transaction and also in the audit trail of the item. with

5. Once the transaction is promoted to urgent, if the sending Participant does not have the required liquidity, the IDL funding may be invoked depending on the TTC of thev1.0 item.
## Example

# Regulations

The following table demonstrates how this feature will work. T1, T2, T3 etc. indicates the transaction initiated by banks. The bank initiating the transaction is debited and beneficiary bank System is credited.

# RTGS

|Normal into Transaction in queue|Initiating Bank (Debit)|Recipient Bank (Credit)|Amount|
|---|---|---|---|
|T1|A|B|5,00,000|
|Subsumed T2|B|C|4,80,000|
|T3|C|A|4,60,000|
|T4|B|C|1,00,000|
|T5|C|A|1,10,000|

The following table explains how these transactions would be settled in off-setting mode when no liquidity is used from the settlement account of the banks or when a percentage of the amount in the settlement account is used for settling the transactions in offsetting mode. The parameter value indicates the percentage of the liquidty, that can be used for settlement of the transactions in offsetting mode (transactions with normal priority).

<!-- PAGE 4 -->

||Example Parameter||Settlement Account||Settled|Used|Used|Used|
|---|---|---|---|---|---|---|---|---|
||Value|Balance of Bank A|Balance of Bank B|Balance of Bank C|Transaction|Liquidity from A|Liquidity from B|Liquidity from C|
|1|0%|10,00,000|10,00,000|10,00,000|0|0|0|0|
|2|5%|10,00,000|0|0|T1,T2,T3|40,000|0|0|
|3|10%|10,00,000|10,00,000|10,00,000|T1,T2,T3,T4,T5|0|80,000|0|

In the **example 1** the parameter value is set to 0% i.e. no amount will be utilised from the settlement account to settle these transactions. Hence, none of the above transactions listed (T1, T2, T3, T4 and T5 will be settled) as there is no transaction with equal value to offset (settle) the transaction.

In **example 2,** the parameter value is set to 5%. The maximum amount which can be used from

# 2026 7,

the settlement account is Rs.50,000 (i.e.5% of Rs. 10,00,000). The transaction T1, T2 and T3 are settled. Though the maximum which can be used from settlement account is Rs.50,000 theApril actual amount utilised from A’s settlement account is 40,000 to settle these transactions. i.e. from Rs.40,000 is utilised to settle transactions T1, T2 and T3 amounting to Rs.14,40,000. However, transaction T4 and T5 could not be settled as liquidity requirement for settling these transactionseffect was more than Rs.50,000.with v1.0 In **example 3** the parameter value is set to 10%. The maximum amount which can be utilised from the settlement account for settlement of the transactions with normal priority is Rs. 1,00,000. In this case, all the transactions listed (T1, T2, T3, T4 and T5) are settled by usitlising

# Regulations

Rs.80,000 from settlement account of B.

# System

# RTGS into

# Subsumed

<!-- PAGE 5 -->

## 2. Future Value Transactions

1. This feature will allow Participants to send RTGS payments which are not submitted for settlement immediately, but at a later date. This option will facilitate the scheduling of certain important payments days in advance.
2. The RTGS will not attempt to settle them immediately but it will wait until the respective value date is reached.
3. The value date must be within a certain time period which is controlled by system parameter of the application (3 working days). When sending a future value payment, the sender must ensure that the respective value date is a working date according to the present RTGS calendar. If the value date is set on a non-working date, the payment will
# 2026

be rejected immediately. 7,

4. A future value dated transaction can be manually canceled at any time, as long as its
# April

status is FUTURE, from the Settlement / Transaction / Cancel menu option. (The cancel from operations requires an approve confirmation.)

5. When a Participant is removed, any future value payments already sent by the saideffect participant and stored in RTGS will be automatically canceled. The sender will be
with notified about the cancelation using standard notification messages. v1.0

6. If the calendar of RTGS is modified by RBI and as a result some future value payments already present in the system have their value date falling on a non-working date, the respective transactions will not be canceled. The items will remain in the system and
# Regulations

they will be submitted to the settlement process on the first working day following the original value date.

# System

# RTGS

********************** into

# Subsumed
