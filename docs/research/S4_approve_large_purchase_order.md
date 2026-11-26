# S4 — approve_order: decision paths and test design

## User story and acceptance criteria
As David, the owner, I want large orders to be approved first so that we don't overspend.

- Under £1,000: automatic approval.
- £1,000 through £5,000 inclusive: manager (Alex) approval.
- Above £5,000: owner/admin (David) approval.
- The purchase-order workflow includes draft, submitted, approved/rejected and sent states.

## Implementation decisions requiring confirmation
- The implementation uses `total_ex_vat` for the monetary thresholds. The story does not specify whether the thresholds include VAT.
- `approver` is a username key in `store.users`; manager and admin are exact role values. Automatic approval does not require an approver.
- On approval, the in-memory purchase order is marked `sent`; the repository has no email/transport layer. Rejection marks it `rejected`.
- Authorization is checked before changing the order, so failed authorization leaves the order unchanged.

## Decision paths
1. Verify that the purchase order exists.
2. Verify that its status is `draft` or `submitted`.
3. Verify that the decision is `approve` or `reject`.
4. Determine the required role from the ex-VAT total.
5. For manager/admin approval, verify the user exists, is active, is unlocked and has the required role.
6. Mark a successful approval as sent, or mark a rejection as rejected.

## Test design and coverage
- Boundary-value analysis: £999.99, £1,000, £5,000 and £5,000.01.
- Equivalence partitioning: automatic, manager, admin and unauthorized approver groups.
- Random testing: deterministic seeded values from each monetary range.
- Statement, branch and representative path tests: exercise approval, rejection and authorization outcomes.
- Symbolic/concolic-style tests: use concrete representatives to satisfy and flip threshold and role conditions.
- Category Partition: `S4_Approval.tsl` defines the input categories; the checked-in Python module contains representative generated-style tests.

## Limitations
The symbolic and concolic modules are representative tests, not proof that an automated symbolic execution engine has explored every feasible path. The category-partition Python file is checked-in representative output; it has not been produced by running an external TSLGenerator unless separately recorded by the team.
