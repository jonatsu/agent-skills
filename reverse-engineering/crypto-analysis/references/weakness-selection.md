# Selecting a cryptographic hypothesis

Use these conditions to decide what to investigate, not to announce a vulnerability from a pattern match.

| Observation                     | Additional evidence required                                                  | What it can establish                                                                       |
| ------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Repeated ECB blocks             | Confirm mode, block alignment, and same key/context                           | Equality leakage; no automatic key recovery                                                 |
| CBC IV reuse or predictability  | Establish key reuse and the operation/threat model                            | Specific confidentiality leakage; not automatic arbitrary forgery                           |
| CTR keystream reuse             | Same key and overlapping counter/nonce stream                                 | XOR relation between plaintexts; known-plaintext recovery where available                   |
| GCM nonce reuse                 | Confirm identical key/nonce and available transcripts                         | Loss of security guarantees; concrete recovery/forgery needs construction-specific analysis |
| Short or unchecked tag          | Tag length, verification path, attempt limits, and accepted message structure | Feasible guessing or acceptance bypass under measured conditions                            |
| Embedded bytes resembling a key | Show the bytes reach the actual key schedule or cryptographic API             | Key extraction for that construction, not all device secrets                                |
| Fallback branch                 | Reachability and acceptance after failure or downgrade                        | A bypass only if trusted behavior survives without the required check                       |
| Decrypted firmware              | Signature coverage, verification key, and acceptance path                     | Access to plaintext; modification acceptance remains a separate question                    |

A CBC padding oracle needs distinguishable externally observable outcomes and adequate queries. A timing observation\
needs repeatability, noise analysis, and control over relevant inputs. State the observation channel and its\
constraints before extrapolating from a local experiment.

## RSA arithmetic

Recover modulus, exponent, padding, encoded message, and signature/encryption direction first. Raw RSA arithmetic\
identities do not automatically apply to randomized or hashed padding constructions.

| Candidate                             | Preconditions to establish                                                                   |
| ------------------------------------- | -------------------------------------------------------------------------------------------- |
| Small or structured modulus factoring | Weak modulus structure or feasible factor size, with bounded work                            |
| Common modulus                        | Same modulus, suitable exponents and related encoded messages; handle invertibility failures |
| Low public exponent                   | Small unpadded integer message or other specifically justified relation                      |
| Broadcast recovery                    | Same suitably encoded message under enough independent, coprime moduli                       |
| Small private exponent                | Parameters within the selected continued-fraction attack's assumptions                       |
| Shared-prime recovery                 | Multiple moduli with a nontrivial greatest common divisor                                    |

Use gmpy2 for large integer operations or SymPy for symbolic/number-theory support only after selecting the\
mathematical test. Check exact roots and re-encrypt or re-verify recovered values. Approximate numeric roots do not\
establish recovery. A valid signature over one encoding does not imply the verifier accepts another; inspect parsing\
and padding checks.
