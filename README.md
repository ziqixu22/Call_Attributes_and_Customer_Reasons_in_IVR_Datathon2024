# Datathon 2024
https://youtu.be/ExZWnrCFxI0

Data cleaning pipeline

external_status: Convert "S" to "U".
auto_pay_enrolled_status: Ensure this column contains integers only: 0 or 1.
account_balance: Confirm all entries are numeric.
resolved: Change "resolved" to 1 and "floor" to 0 for numerical processing.
no_of_account_with_syf: Verify all entries are numeric.


MOS: lowercase and uppercase letters should be kept. There’s no need to convert to anything else. This doesn’t need to be changed

external_status: S should be converted to U

auto_pay_enrolled_status: make sure 0 and 1 in this column are all integers 0 represents the absence, and 1 represents the presence of that category

account_balance:  Do not remove null rows; make sure they are all numbers, not words

resolved: convert resolved to be 1, floor to be 0 (number) (this is for simpler calculations)

no_of_account_with_syf: make sure they are numbers

account_open_date_13_march and account_open_date_18_march: There are 2 rows with different open dates (previously asked in discord). Use the older date. 

card_activation_status: make sure they are all numbers; check if there are numbers other than 0, 7, 8, 9; Chage “ ” to 6.

account_status: do not remove NULL since it means no restrictions; replace B, C, E, F, I, Z as letter C (closed); replace blank as N (no restriction)

serial: probably there are duplicate serial number -> same person call more than once

delinquency_history:
  compare delinquency_history_13_March and delinquency_history_18_March, see if they are equal
  separate e.g., [01] to two columns like: 
    delinquency_history_18_March_current: 0
    delinquency_history_18_March_past: 1
  create a new attribute delinquency_compare_13_March
    M: [32] more delinquency in current than the past
      There can only be 1 more comparing current and past
    N: [00] no delinquency at all
    E: [22] current = past, but with delinquency
    P: [03] or [23] paid delinquency currently
    NA: current - past > 1, bad data
  e_bill_enrolled_status:
    create a new attribute e_bill_enrolled_status_combined:
      replace blank to be P (paper)
      replace B, D, L to be B (both paper and electronic)
      keep E (electronic)

Analyze Data:
![Alt text](file:///Users/ziqixu/Desktop/Screenshot%202024-04-04%20at%2020.47.48.png)






















