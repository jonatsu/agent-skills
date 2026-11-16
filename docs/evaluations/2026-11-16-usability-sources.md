# Evaluation: Sources for a General Usability Skill

Read date for every web source below: 2026-11-16, unless a date is given. It surveys the established usability principle
sets, evaluation methods, and laws, as the source base for the `usability` skill.

## How to read this file

- **Read** means the original or an official preview was opened and the text checked.
- **Secondary** means a reputable third party that cites the original. The reason is given each time.
- **Lead** means a search-engine summary that was not confirmed on a page. Treat a lead as unverified.
- Confidence: high (original read, or two independent sources agree), medium (one secondary, or inference),
  low (lead only).
- Licence notes record what the source page states. They are not legal advice.
- Three load-bearing claims were rechecked against the originals: Quesenbery's 2001 expansion sentence and
  her five names, Nielsen's severity scale and its factors, and the seven ISO 9241-110:2020 names (through a
  secondary that cites the standard, because the ISO page refused the request).

## 1. Principle sets and models

### 1.1 Nielsen's 10 usability heuristics

- **Source.** Jakob Nielsen, "10 Usability Heuristics for User Interface Design", Nielsen Norman Group (NN/g),
  1994-04-24, last reviewed 2024-01-30. <https://www.nngroup.com/articles/ten-usability-heuristics/> (read).
  Academic roots: Molich and Nielsen 1990 (CACM 33(3):338-348); Nielsen and Molich 1990 (CHI'90, 249-256);
  Nielsen 1994a "Enhancing the explanatory power of usability heuristics" (CHI'94, 152-158); Nielsen 1994b
  "Heuristic evaluation" in Nielsen and Mack (eds.), *Usability Inspection Methods*, Wiley.
- **Names as stated (2024 page).** 1 Visibility of System Status. 2 Match Between the System and the Real World.
  3 User Control and Freedom. 4 Consistency and Standards. 5 Error Prevention. 6 Recognition Rather than Recall.
  7 Flexibility and Efficiency of Use. 8 Aesthetic and Minimalist Design. 9 Help Users Recognize, Diagnose, and
  Recover from Errors. 10 Help and Documentation.
- **Summary.** Ten broad rules of thumb for interactive systems: show state, speak the user's language, allow
  exit and undo, stay consistent, prevent errors, reduce memory load, support experts, keep it focused, make
  errors understandable, and offer help.
- **History.** Nielsen says the set came from his 1990 work with Rolf Molich and was refined in 1994 by a factor
  analysis of 249 usability problems. The 2020 update changed wording and examples only; the ten headings are
  unchanged since 1994 (from the page's "Note from Jakob").
- **Standing.** The most used heuristic set in practice; NN/g recommends it for heuristic evaluation.
  Cited as a source by ISO 9241-110:2020 (see 1.7).
- **Licence.** Page says you may use the heuristics with credit to Jakob Nielsen and the page address, or cite
  Nielsen 1994a. Reproducing the page needs permission (NN/g copyright page).
- **Criticism.** NN/g itself says a heuristic violation is not automatically a problem: the hamburger menu
  violates heuristic 6 but may be the right trade-off on mobile (How to Conduct a Heuristic Evaluation, 2023).
  Heuristics are guidelines, not laws. Method limits are in section 2.1.
- **Confidence.** High.

### 1.2 Shneiderman's Eight Golden Rules of Interface Design

- **Source.** Ben Shneiderman, "The Eight Golden Rules of Interface Design", author page at the University of
  Maryland (read): <https://www.cs.umd.edu/users/ben/goldenrules.html>. The page reproduces section 3.3.4 of
  Shneiderman, Plaisant, Cohen, Jacobs and Elmqvist, *Designing the User Interface*, 6th ed., Pearson, May 2016.
  He says the original list dates from 1985 and each edition changes it.
- **Names as stated (6th ed.).** 1 Strive for consistency. 2 Seek universal usability. 3 Offer informative
  feedback. 4 Design dialogs to yield closure. 5 Prevent errors. 6 Permit easy reversal of actions. 7 Keep users in
  control. 8 Reduce short-term memory load.
- **Summary.** Eight rules distilled from experience: consistent sequences and terms, design for diverse users
  and experts, feedback for every action, grouped action sequences with a clear end, error prevention plus
  constructive recovery, undo, user in charge, and low memory demand.
- **Standing.** Widely taught in HCI courses; the page notes that Nielsen and Jeff Johnson extended the list.
  A textbook now in its 6th edition. No citation count was measured.
- **Licence.** Copyright Shneiderman and Pearson; page is free to read. No reuse licence stated.
- **Criticism.** Shneiderman says the rules "require validation and tuning for specific design domains" and no
  list can be complete. Rule 8 cites "seven plus or minus two chunks"; later work puts working memory nearer four
  chunks (see 3.3). Rule 4 (closure) and rule 2 (universal usability) have no direct Nielsen equivalent.
- **Confidence.** High.

### 1.3 Norman: design principles, signifiers, gulfs

- **Source.** Donald A. Norman, *The Design of Everyday Things*, revised and expanded edition, Basic Books, 2013
  (the BYU source says the first edition was called *The Psychology of Everyday Things*; year not verified).
  Book not read. Author-published articles read:
  "Affordances and Design" and "Signifiers, not affordances", *Interactions* 15(6), 2008-11-17, both on jnd.org;
  the book page and preface on jnd.org. <https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/>
  Full-text PDFs of the book on archive.org and mirror servers look unauthorised; not used.
- **Affordances versus signifiers.** Norman uses James Gibson's
  affordance (1977/1979): a relation between an actor and an object that allows an action. He earlier introduced
  "perceived affordance"; his 2008 article and the 2013 preface say the term confused designers, especially for
  virtual objects, because on a screen a designer can only show a signifier. A signifier is the perceivable cue
  that tells people where the action should happen. The 2013 edition adds signifiers as a new concept and says
  signifiers matter more to designers than affordances. Cultural constraints are conventions (jnd.org articles).
- **The set of principles.** Two secondary sources disagree on the count. The Brigham Young University Design
  Review (secondary, a student summary citing the chapter "Fundamental Principles of Interaction") says seven:
  discoverability, then affordances, signifiers, constraints, mappings, feedback, conceptual models. A search
  summary quoting p.10 of the 2013 text (lead only; the quoted sentence was not read in an authorised copy)
  says discoverability results from five fundamental psychological concepts (affordances, signifiers,
  constraints, mappings, feedback) and that "a sixth principle, perhaps most important" is the conceptual model.
  The jnd.org table of contents shows a section titled "Seven Stages of Action: Seven Fundamental Design
  Principles". Reading: discoverability is the goal, five concepts serve it, and the conceptual model ties them
  together. Whether the book itself counts this as six or seven was not checked in an authorised copy. Mark the
  count unverified; the list of concepts is consistent.
- **Gulfs.** Gulf of execution (can the user work out how to act?) and gulf of evaluation (can the user tell
  what happened?). Origin: Hutchins, Hollan and Norman 1986, in Norman and Draper (eds.), *User Centered System
  Design*, Erlbaum. Seen only through NN/g (2018) as secondary. Norman's book says signifiers, constraints,
  mappings and a conceptual model bridge the gulf of execution; feedback and the conceptual model bridge the
  gulf of evaluation (lead).
- **Standing.** The best-known popular design text; high.
- **Licence.** Copyright Norman and Basic Books. Articles on jnd.org are copyrighted by the author.
- **Criticism.** Norman himself retreated from "affordance" as a design term (above). The term is also used
  loosely in industry to mean "looks clickable", which is Norman's signifier, not an affordance.
- **Confidence.** Medium (book unread).

### 1.4 Tognazzini's First Principles of Interaction Design

- **Source.** Bruce "Tog" Tognazzini, "First Principles of Interaction Design (Revised & Expanded)", asktog.com,
  2014-03-05 (read). <https://asktog.com/atc/principles-of-interaction-design/> An earlier shorter version (about
  2003\) is cited in the older literature; the 2014 version replaces it.
- **Names as stated (section headings, 19).** Aesthetics, Anticipation, Autonomy, Color (incl. colour blindness),
  Consistency (four sub-principles), Defaults, Discoverability, Efficiency of the User, Explorable Interfaces,
  Fitts's Law, Human Interface Objects, Latency Reduction, Learnability, Metaphors Use of, Protect Users' Work,
  Readability, Simplicity, State, Visible Navigation.
- **Summary examples (read).** Anticipation: bring the user all the information and tools needed for each step.
  Fitts's Law: acquisition time depends on distance to and size of the target. Protect Users' Work: users never
  lose their work. Defaults: easy to "blow away". Readability: text that must be read has high contrast.
- **Standing.** A long-standing practitioner list; ISO 9241-110:2020 names Tognazzini among its sources.
  NN/g calls it slightly too long for heuristic evaluation but a useful checklist.
- **Licence.** "Copyright 1978-2014 by Bruce Tognazzini." Copies allowed for personal use if the notice remains;
  not for publication for money (page notice).
- **Criticism.** Not a validated set. Mixes principles with specific laws (Fitts) and platform advice.
  Several items are Apple-era interaction advice.
- **Confidence.** High on content; medium on date of the earlier version.

### 1.5 Gerhardt-Powals' cognitive engineering principles

- **Source.** Jill Gerhardt-Powals, "Cognitive engineering principles for enhancing human-computer
  performance", *International Journal of Human-Computer Interaction* 8(2):189-211, 1996. Paper behind a
  paywall (closed access per Semantic Scholar); not read. The list was read as reproduced in a knowledge-base
  copy of the paper's list and in Wikipedia's heuristic evaluation article (secondary; used because the journal
  is closed). The human factors firm HFI newsletter also cites the paper.
- **Names as stated (10).** Automate unwanted workload. Reduce uncertainty. Fuse data. Present new information
  with meaningful aids to interpretation. Use names that are conceptually related to function. Group data in
  consistently meaningful ways. Limit data-driven tasks. Include in the displays only that information needed by
  the user (operator) at a given time. Provide multiple coding of data when appropriate. Practice judicious
  redundancy.
- **Summary.** Reduce the user's mental calculation and search load by moving work to the system and
  presenting summarised, well-grouped data. Principle 10 settles the tension between 6 (consistent grouping)
  and 8 (show only what is needed).
- **Standing.** Cited about 175 times (Semantic Scholar count). Less used than Nielsen's set; appears in
  heuristic-evaluation comparisons and in display design for command-and-control. The source domain was
  anti-submarine warfare displays (lead).
- **Licence.** Journal copyright (Taylor & Francis); list quoted widely without a stated licence.
- **Criticism.** Some web copies list nine principles and omit "Group data..." (design knowledge base page).
  One copy of the list says principle 10 "was devised by the first two authors", which is odd for a
  single-author paper. The list may come from a related multi-author report. Unresolved.
- **Confidence.** Medium (names confirmed by three secondary copies; paper unread).

### 1.6 Weinschenk and Barker (speech interfaces)

- **Source.** Susan Weinschenk and Dean T. Barker, *Designing Effective Speech Interfaces*, Wiley, 2000.
  Book unread. Secondary: Wikipedia (earlier run) describes a 20-category classification, and the design knowledge
  base page lists the first categories: User control, Human limitations, Modal integrity. The remaining category
  names were not seen in this run and are **unverified**.
- **Why it matters.** It is a rare published set aimed at voice interfaces, which the target skill must cover.
- **Confidence.** Low.

### 1.7 ISO 9241-110 interaction principles

- **Source.** ISO 9241-110:2020, *Ergonomics of human-system interaction, Part 110: Interaction principles*,
  2nd ed., 2020-05, ISO. Formerly "dialogue principles" (ISO 9241-10:1996, then 9241-110:2006). Paid standard.
  Official iTeh preview read: foreword, introduction, scope. The iso.org catalogue abstract was also read.
  Principle names read from the preview text via search and Wikipedia (secondary for the full list).
- **Names as stated (2020, seven).** Suitability for the user's tasks, Self-descriptiveness, Conformity with
  user expectations, Learnability, Controllability, Use error robustness, User engagement.
- **2006 names (seven, secondary only).** Suitability for the task, Self-descriptiveness, Controllability,
  Conformity with user expectations, Error tolerance, Suitability for individualization, Suitability for
  learning. Source: usability.de glossary and a heurio.co summary (search leads). Names unverified in the 2006
  text itself.
- **What changed in 2020 (read, foreword and Wikipedia).** Individualization merged into controllability;
  user engagement is new; guidance from ISO 14915-1 absorbed.
- **Summary.** Seven general principles with design recommendations for each, independent of technology. The
  introduction says the recommendations derive from ergonomics research and heuristic sources including
  Bastien, Dzida, Molich, Nielsen and Tognazzini. It lists typical problems the principles prevent: extra steps,
  misleading or missing information, unexpected responses, navigation limits and poor error recovery.
- **Scope limits (read).** Applies to all interactive systems but does not cover the specifics of every domain,
  with safety-critical systems, collaborative work and artificial intelligence features given as examples. It
  excludes marketing, aesthetics and corporate identity. Presentation of information goes to ISO 9241-112,
  whose principles the introduction lists: detectability, freedom from distraction, discriminability,
  unambiguous interpretability, conciseness and consistency.
- **Standing.** The main international standard for interaction principles (adopted as EN ISO 9241-110:2020 by
  European standards bodies, per catalogue listings). No citation count measured.
- **Licence.** © ISO. No reproduction without permission. Paraphrase names only.
- **Criticism.** No independent validation of the seven-way split was found. The 2020 text excludes
  safety-critical domains, so it does not replace the HMI standards in 1.9.
- **Confidence.** High on names and scope; medium on definitions (not read in full).

### 1.8 ISO 9241-11 definition of usability

- **Source.** ISO 9241-11:2018, *Ergonomics of human-system interaction, Part 11: Usability: Definitions and
  concepts*, 2nd ed., 2018-03. Official SIS preview PDF read: foreword, introduction, scope, clause 3.1.1.
- **Definition (clause 3.1.1, verbatim).** "extent to which a system, product or service can be used by
  specified users to achieve specified goals with effectiveness, efficiency and satisfaction in a specified
  context of use". Note 1: the specified users, goals and context refer to the combination being considered.
  Note 2: "usability" is also a qualifier for design knowledge, competencies, activities and attributes.
- **Introduction (read).** Usability is the outcome of interacting, not an attribute of a product. It is "a more
  comprehensive concept than ... ease-of-use or user friendliness". It is relevant to regular use, learning,
  infrequent use, widest range of capabilities, minimising the risk of use errors, and maintenance.
- **Changes from 1998 (foreword, read).** Scope extended to systems and services; wider range of goals including
  personal and organisational outcomes; efficiency defined relative to results achieved, not accuracy and
  completeness; satisfaction widened. Sub-clauses cover accessibility, user experience and avoidance of harm
  as "other outcomes of use" (contents page, read).
- **Standing.** The standard definition; Brooke (SUS) and Quesenbery (5Es) cite the 1998 edition.
- **Licence.** © ISO.
- **Criticism.** The definition names three measures only; critics (including Quesenbery, below) add learnability
  and error tolerance, which the 2018 introduction covers in prose but not in the definition.
- **Confidence.** High. ISO 9241-210:2019 (human-centred design process) abstract was also read; the document
  itself was not.

### 1.9 Quesenbery's 5Es and the ISO 9241-11 question

- **Source.** Whitney Quesenbery, "What Does Usability Mean: Looking Beyond 'Ease of Use'", Proceedings of the
  48th Annual Conference of the Society for Technical Communication, 2001 (read on the author's site):
  <https://www.wqusability.com/articles/more-than-ease-of-use.html>. A later piece "Balancing the 5Es: Usability",
  Cutter IT Journal 2004, is a lead only (PDF fetch failed; unread).
- **Names as stated.** Effective, Efficient, Engaging, Error Tolerant, Easy to Learn.
- **Which source owns the 5Es: resolved.** The 2001 paper quotes the ISO 9241 usability definition (effectiveness,
  efficiency, satisfaction) and says it "can be expanded, and made more comprehensive, by including five
  characteristics". The 5Es are therefore Quesenbery's expansion, not ISO's. ISO 9241-11:2018 (read) defines only
  effectiveness, efficiency and satisfaction. A third-party skill that attributes the 5Es to ISO 9241-11 is
  wrong. Overlap: ISO's introduction covers learning and use errors in prose, but not as defined measures.
- **Summary.** Effective is accuracy and completeness. Efficient is speed with accuracy, counted in clicks or
  time on task. Engaging is pleasant and satisfying use. Error tolerant means preventing errors and helping
  recovery. Easy to learn covers first use and learning across the whole life of use. Her weights depend on
  context: the paper shows a benefits site and a conference registration site with different rankings, and
  maps each E to an evaluation technique and a sample goal.
- **Standing.** Widely repeated in practitioner writing; not a standard. No citation count measured.
- **Licence.** Paper on the author's site; no licence stated. Cite, do not copy.
- **Criticism.** No validation study found. Overlaps with Nielsen's heuristics (error prevention, learnability).
- **Confidence.** High on attribution; medium on standing.

### 1.10 Morville's user experience honeycomb

- **Source.** Peter Morville, "User Experience Design", Semantic Studios (read, author's own site):
  <https://semanticstudios.com/user_experience_design/>. The page carries no date. Internal evidence ("ten
  tempestuous years" since 1994) suggests about 2004; the year is **unverified**.
- **Names as stated (seven facets).** Useful, Usable, Desirable, Findable, Accessible, Credible, Valuable.
- **Summary.** A diagram of seven qualities of user experience, made to show clients that usability is
  "necessary but not sufficient". Each quality needs a priority trade-off, and the model supports modular
  redesign (for example, a credibility audit).
- **Standing.** Frequently reproduced diagram in UX teaching; no citation count measured.
- **Licence.** None stated on the page.
- **Criticism.** A framing device, not a testable principle set. Written for web sites. "Valuable" and "useful"
  are business and product questions, outside interface review.
- **Confidence.** High on names; low on date.

### 1.11 Crampton Smith's four dimensions and Silver's fifth

- **Source.** Kevin Silver, "What Puts the Design in Interaction Design", UXmatters, 2007-07-10 (read, original
  article): <http://www.uxmatters.com/mt/archives/2007/07/what-puts-the-design-in-interaction-design.php>
  Silver credits Gillian Crampton Smith, in the introduction of Bill Moggridge, *Designing Interactions*, MIT Press,
  2007\. The Moggridge book was not read, so her four dimensions are known **only through Silver** (secondary,
  used because the book is not online).
- **Names as stated by Silver.** 1D words; 2D visual representations; 3D physical objects or space; 4D time;
  5D behaviour (action or operation, and presentation or reaction). Crampton Smith's four are 1D to 4D; Silver
  says "I have added a fifth".
- **Summary.** The first three dimensions enable interaction; time and behaviour define it. Silver ties
  behaviour to the flow between action and reaction and calls interaction a conversation.
- **Standing.** Cited in interaction-design teaching (the Interaction Design Foundation has an article). Silver's
  2025 follow-up says it is cited by over 90 papers (lead, from a search summary; not confirmed).
- **Criticism.** It is a descriptive language for interaction design, not a rule set. It does not tell a
  reviewer what is wrong with an interface. Popular summaries of "5D" sometimes say it means emotions, which is
  not Silver's meaning.
- **Confidence.** High on Silver; medium on Crampton Smith.

### 1.12 WCAG 2.2 principles (accessibility)

- **Source.** W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 2024-12-12.
  <https://www.w3.org/TR/WCAG22/> (the first 100k characters read, and the raw source file in the w3c/wcag repository).
- **Names as stated (four principles).** Perceivable, Operable, Understandable, Robust.
  Perceivable: "Information and user interface components must be presentable to users in ways they can
  perceive." Operable: "User interface components and navigation must be operable."
- **13 guidelines (read).** Text Alternatives, Time-based Media, Adaptable, Distinguishable, Keyboard Accessible,
  Enough Time, Seizures and Physical Reactions, Navigable, Input Modalities, Readable, Predictable, Input
  Assistance, Compatible.
- **Conformance.** Success criteria at levels A, AA and AAA. WCAG 2.2 removed 4.1.1 Parsing and added nine
  success criteria (raw source, read).
- **Standing.** The reference accessibility standard; WCAG 2.0 is also ISO/IEC 40500 (from memory, **unverified**).
  Many laws and procurement rules cite it.
- **Licence.** Copyright W3C; W3C Document License applies (page notice).
- **Criticism.** Web-oriented; testable criteria are not the same as usable. Not checked: WCAG 3 status.
- **Confidence.** High.

### 1.13 HMI, control-room and industrial standards

All items below were identified from catalogue abstracts, official previews or agency pages. None were read in
full. Treat details as pointers.

- **ISO 11064, Ergonomic design of control centres, parts 1 to 7** (iTeh sample of part 4 read: layout and
  dimensions of workstations). The UK Health and Safety Executive control-room page cites ISO 11064 and EEMUA 201.
- **ANSI/ISA-101.01-2015, Human-Machine Interfaces for Process Automation Systems.** Seen only on an ANSI blog
  (secondary); the preview PDF was empty. Contents **unverified**.
- **NUREG-0700 Rev 3**, Human-System Interface Design Review Guidelines, O'Hara and Fleger, US NRC, July 2020.
  Public domain US government text; NRC page read.
- **MIL-STD-1472H**, Human Engineering, 2020-09-15 (everyspec listing read). US government document.
- **IEC 60447:2004** (actuating principles for man-machine interfaces; webstore abstract and iTeh sample read:
  scope, contents including opposite effects, emergency stop, visual, acoustic and tactile identification).
- **IEC 60073:2002** (coding principles for indicators and actuators; iTeh sample read: coding by colour, shape,
  position, flashing; acoustic and tactile). The colour-meaning table was not in the preview; a search summary
  of it is **unverified**.
- **IEC 62366-1:2015 +A1:2020**, usability engineering for medical devices (iso.org abstract read).
- **Standing.** ISO, IEC and ISA documents are formal references in their fields (inference from catalogue
  entries). They are paid and copyrighted. The NRC and MIL-STD documents were publicly listed; their copyright
  status was not checked.
- **Why it matters.** These cover physical controls, alarms, emergency stops and colour codes. Software
  heuristics do not.
- **Confidence.** Medium for existence and scope; low for content.

### 1.14 Other candidate sets noted but not surveyed

Names only, none fetched or verified: Jeff Johnson's interface design rules, Bastien and Scapin's ergonomic
criteria and Dzida's and Molich's lists (all named by ISO 9241-110:2020 as sources), platform guides such as Apple
Human Interface Guidelines and Material Design, and any published guidelines for AI-driven interfaces.

## 2. Evaluation methods

### 2.1 Heuristic evaluation

- **Sources.** Nielsen and Molich 1990, CHI'90 (names above). Nielsen, "Heuristic evaluation", in *Usability
  Inspection Methods*, 1994. NN/g web copy, "How to Conduct a Heuristic Evaluation" (Moran and Gordon, 2023-06-25)
  and "The Theory Behind Heuristic Evaluation" (Nielsen, 1994) (both read).
- **How it is done.** A few evaluators each examine the interface alone, one to two hours, usually twice (first
  to learn the flow, then to find violations), against a set of heuristics. Findings are listed per heuristic.
  Evaluators must not see each other's notes until finished. Results are consolidated afterwards, for example by
  affinity diagram. Narrow the scope to one task, section, user group or device.
- **How many evaluators.** Nielsen recommends three to five. Averaged over six of his projects, a single evaluator
  found 35 percent of the problems. The Nielsen and Landauer (1993) model, `ProblemsFound(i) = N(1 - (1 - l)^i)`
  with `l` from 19 to 51 percent (mean 34 percent) and `N` from 16 to 50 problems. In a sample cost model four
  evaluators was optimal, with a benefit-cost ratio of 62; one case study found a ratio of 48. The cost figures
  are from the early 1990s.
- **Severity ratings.** Nielsen, "Severity Ratings for Usability Problems", NN/g (read). Severity combines
  frequency, impact and persistence, plus market impact. Scale: 0 "I don't agree that this is a usability
  problem at all"; 1 cosmetic only; 2 minor, low priority; 3 major, high priority; 4 usability catastrophe,
  imperative to fix before release. Collect ratings after the session, from a list of all problems, with each
  evaluator rating independently. A single evaluator's rating is "too unreliable"; the mean of three is
  satisfactory for many purposes (about 30 minutes per evaluator).
- **Limits.**
  - NN/g: it cannot replace user research and finds likely problems, not whether users succeed.
  - Evaluator effect: Hertzum and Jacobsen, "The Evaluator Effect: A Chilling Fact About Usability Evaluation
    Methods", *IJHCI* 13(4):421-443, 2001. Review of 11 studies. Different evaluators report markedly different
    problem sets for heuristic evaluation, cognitive walkthrough and think-aloud. They recommend several evaluators.
    **Secondary only:** the publisher abstract page returned 403 (twice with another route); the abstract was
    taken from a search summary. Confidence medium.
  - Comparison studies: Gray and Salzman, "Damaged Merchandise? A Review of Experiments That Compare Usability
    Evaluation Methods", *Human-Computer Interaction* 13(3):203-261, 1998. They argue design flaws in five
    influential comparison studies make their method rankings unreliable (abstract via search summary of the ACM
    record; paper unread).
  - CUE-4 (Molich and Dumas, *Behaviour & Information Technology* 27(3), 2008): 17 teams evaluated one hotel
    site, nine by usability testing and eight by inspection; the author's page (read, dialogdesign.dk/CUE-4.htm)
    says inspection was as effective and efficient as usability testing, that testing is not a gold standard, and
    that effort beyond about 25 person-hours added little. A search summary gave 340 problems, 205 reported by a
    single team, and nine reported by more than half of the teams; the author's page did not state those numbers,
    so they are **unverified**.
- **Confidence.** High on procedure; medium on limits.

### 2.2 Cognitive walkthrough

- **Original sources.** Lewis, Polson, Wharton and Rieman, "Testing a walkthrough methodology for theory-based
  design of walk-up-and-use interfaces", CHI'90, 235-242 (reference as given by NN/g; paper unread).
  Polson, Lewis, Rieman and Wharton, "Cognitive walkthroughs: a method for theory-based evaluation of user
  interfaces", *Int. J. Man-Machine Studies* 36:741-773, 1992 (title and citation from a search result; unread).
  Wharton, Rieman, Lewis and Polson, "The cognitive walkthrough method: a practitioner's guide", in Nielsen and
  Mack (eds.), *Usability Inspection Methods*, Wiley, 1994, pp. 105-140 (ACM DL record shows about 165
  citations). The University of Colorado technical report 93-07 holds the same text but is scanned images that no
  tool here could read. The 1994 text was **not read**.
- **Four questions as stated by Wharton et al. 1994.** Spencer 2000 quotes them in his Table 1 (read in the
  original PDF; secondary for Wharton). 1 "Will the user try to achieve the right effect?" 2 "Will the user notice
  that the correct action is available?" 3 "Will the user associate the correct action with the effect that user
  is trying to achieve?" 4 "If the correct action is performed, will the user see that progress is being made
  toward the solution of the task?" NN/g (2022) paraphrases them as "right result", "notice", "associate" and
  "progress".
- **How it is done.** Define users and tasks, write the action sequence, then walk through step by step,
  telling a plausible success story for each of the four questions. Record problems, design ideas, design gaps
  and task-analysis issues. The method targets learnability for first-time (walk-up-and-use) users.
- **Streamlined cognitive walkthrough.** Rick Spencer, "The Streamlined Cognitive Walkthrough Method, Working
  Around Social Constraints Encountered in a Software Development Company", CHI 2000, pp. 353-359 (original read).
  Spencer cut the four questions to two: "Will the user know what to do at this step?" and "If the user does the
  right thing, will they know that they did the right thing, and are making progress towards their goal?" He
  added ground rules: no design discussions, explicit defusing of defensiveness, roles, and softer language
  ("potential problem"). He found the full method gave voluminous output, was slow, led to design discussion
  and defensiveness, and that his team did not find it useful at first.
- **Limits.** Learnability focus only; needs a task analysis; slow and verbose in the full form (Spencer).
  Hertzum and Jacobsen 2001 found an evaluator effect for it. NN/g says it suits new or complex flows and is
  overkill for standard patterns. The Usability Body of Knowledge page says the streamlined variant is widely
  used with little published validation (lead).
- **Licence.** ACM copyright on Spencer; Wharton chapter by Wiley.
- **Confidence.** High on Spencer and on the question text; medium on Wharton overall.

### 2.3 Usability testing

- **Sources.** NN/g, "Why You Only Need to Test with 5 Users", Nielsen, 2000-03-18 (read); Nielsen and Landauer
  1993, INTERCHI'93, 206-213; NN/g "Thinking Aloud: The #1 Usability Tool" and the 2012 think-aloud notes (read
  earlier). ISO 9241-11 gives the measures (effectiveness, efficiency, satisfaction).
- **How it is done.** Representative users attempt realistic tasks while an observer watches; think-aloud is the
  common protocol; the team records task success, time, errors and comments. Test early and often. Quesenbery
  maps each of her 5Es to a test technique (2001 paper, table of evaluation types).
- **The five-user claim.** Problems found by n users is `N(1 - (1 - L)^n)` with `L` typically 31 percent. Five users
  find about 85 percent; 15 find nearly all. Nielsen's advice is three tests of five users, not one test of 15,
  and more users when there are several distinct user groups (3 to 4 per group for two groups, 3 per group for
  more). The same article says the model holds only for comparable users.
- **Limits and corrections.**
  - Faulkner, "Beyond the five-user assumption: Benefits of increased sample sizes in usability testing",
    *Behavior Research Methods, Instruments, & Computers* 35(3):379-383, 2003. A 60-user study found 45
    problems; random sets of five found as few as 55 percent of them and as many as 99 percent. The publisher
    page redirected to a login twice, so this is **secondary only** (search summary). Medium confidence.
  - Evaluator effect and CUE studies above: results depend on who runs and analyses the test.
  - The popular reading "five users are enough" ignores the iterative use, the homogeneity assumption and `L`
    varying by project. Nielsen's own article says 15 are needed to find all problems.
  - NN/g's think-aloud notes (read in an earlier run, 2012) list downsides of the protocol; the specifics
    were not re-checked here.
- **Confidence.** High on Nielsen; medium on Faulkner.

### 2.4 System Usability Scale (SUS) and other questionnaires

- **SUS source.** John Brooke, "SUS: A quick and dirty usability scale", in Jordan et al. (eds.), *Usability
  Evaluation in Industry*, Taylor & Francis, 1996 (author's preprint read at hell.meiert.org). Copyright line on the
  scale: "(c) Digital Equipment Corporation, 1986". Brooke worked at Redhatch Consulting; the scale was built for
  Digital Equipment Co.
- **Items (verbatim, all five-point strongly disagree to strongly agree).** 1 I think that I would like to use
  this system frequently. 2 I found the system unnecessarily complex. 3 I thought the system was easy to use. 4 I
  think that I would need the support of a technical person to be able to use this system. 5 I found the various
  functions in this system were well integrated. 6 I thought there was too much inconsistency in this system. 7 I
  would imagine that most people would learn to use this system very quickly. 8 I found the system very
  cumbersome to use. 9 I felt very confident using the system. 10 I needed to learn a lot of things before I could
  get going with this system.
- **Scoring (verbatim logic).** Items 1, 3, 5, 7, 9 contribute scale position minus 1; items 2, 4, 6, 8, 10
  contribute 5 minus scale position; sum times 2.5 gives 0 to 100. Individual item scores are "not meaningful on
  their own". Use right after use, before debriefing; tick the midpoint if unsure.
- **How it was built.** From a pool of 50 items rated by 20 people on two systems, one easy and one very hard;
  extreme, strongly correlated items were kept, half positive and half negative.
- **Standing.** Very widely used. Sauro (MeasuringU, 2011, secondary) puts the mean at 68 over about 500 studies.
  Lewis and Sauro 2009 report two factors, with items 4 and 10 reading as learnability. Brooke's text says SUS
  yields a single composite; the factor work is later. Lewis 2018, "The System Usability Scale: Past, Present, and
  Future", *IJHCI* (DOI 10.1080/10447318.2018.1455307) is closed and unread. The JUX 2013 retrospective was
  unreachable.
- **Licence.** Notes record that SUS is free to use if the source is acknowledged; this survey did not re-read
  that statement and the preprint shows only the DEC copyright line. Treat the terms as **unverified** and cite
  Brooke 1996 when reproducing.
- **Limits.** Global measure only; it does not diagnose causes; scores need a comparison point; the mean of 68 is
  an average of past studies, not a pass mark; wording may need adapting for non-software products (inference).
- **Other questionnaires seen but not read in the original.** Single Ease Question (SEQ, 7-point; seen in
  Wikipedia's ISO 9241 article, secondary); CSUQ and PSSUQ (IBM, Lewis 1995; name only); UMUX-Lite and SUPR-Q
  (names only, no source read). Add if the skill needs them.
- **Confidence.** High on SUS content; medium on its standing figures.

## 3. Laws and quantitative findings

### 3.1 Fitts's law

- **Source.** Paul M. Fitts, "The information capacity of the human motor system in controlling the amplitude of
  movement", *Journal of Experimental Psychology* 47(6):381-391, 1954 (Semantic Scholar lists about 8,800
  citations; volume and pages from memory, unverified). MacKenzie, "Fitts' law as a research and design tool in
  human-computer interaction", *Human-Computer Interaction* 7:91-139, 1992 (scanned PDF; pages 91-96 read).
- **What it says.** Movement time to a target rises with the logarithm of distance divided by target width. In
  MacKenzie's text, index of difficulty `ID = log2(2A/W)`, index of performance `IP = ID/MT`. He treats Fitts's law
  and the Hick-Hyman law as the two information-theory models that survived in HCI.
- **Popular misstatements (inference).** "Screen edges are infinitely large targets" is Tognazzini's corollary
  for a cursor that stops at the edge (see his Fitts's Law section); it does not hold for touchscreens or
  non-clamped pointers. Fitts's law gives pointing time, not whether a control is findable or understandable.
  The 1954 task was reciprocal tapping (from memory, **unverified**).
- **Standing.** Standard in input-device research and ISO 9241-411 style evaluation (the last is from memory,
  **unverified**).
- **Confidence.** Medium (1954 paper unread).

### 3.2 Hick-Hyman law

- **Source.** W. E. Hick, "On the rate of gain of information", *Quarterly Journal of Experimental Psychology*
  4:11-26, 1952; Ray Hyman, "Stimulus information as a determinant of reaction time", *Journal of Experimental
  Psychology* 45:188-196, 1953 (years confirmed by Semantic Scholar metadata; pages from memory, unverified).
- **What it says.** Choice reaction time grows with the information content of the choice, about the log of the
  number of equally likely alternatives, for a practised stimulus-response task.
- **Popular misstatement.** "Fewer menu items are always faster to choose from." The law describes
  reaction time for a given set of alternatives, not time to scan an unordered menu. Wikipedia (secondary) cites
  Landauer and Nachbar 1985 and Cockburn et al. 2007 for menu models that combine Hick-Hyman with Fitts and
  linear search in unordered lists. Cockburn 2007 could not be fetched twice, so
  that claim is **unverified**.
- **Confidence.** Medium.

### 3.3 Miller's 7 plus or minus 2 and Cowan's 4 plus or minus 1

- **Miller.** George A. Miller, "The magical number seven, plus or minus two: Some limits on our capacity for
  processing information", *Psychological Review* 63(2):81-97, 1956 (read at psychclassics.yorku.ca). It reports
  two things: absolute judgment along one dimension (about seven categories) and immediate memory span (about
  seven items), measured differently. He introduces "chunks" and calls the repeated number "a pernicious,
  Pythagorean coincidence".
- **Cowan.** Nelson Cowan, "The magical number 4 in short-term memory: A reconsideration of mental storage
  capacity", *Behavioral and Brain Sciences* 24(1):87-114, 2001 (open PDF read). With rehearsal and chunking
  controlled, capacity is about three to five chunks, four on average.
- **Popular misstatements.** (1) "Menus, navigation or pages should have 7 plus or minus 2 items": Miller did not
  study interface lists, and recognition tasks (a visible menu) do not rely on memory span. (2) Shneiderman's golden
  rule 8 cites seven plus or minus two; the later estimate is lower. (3) Treating the number as a hard limit
  ignores chunking. The accurate design lesson is to avoid making users hold information across screens.
- **Confidence.** High.

### 3.4 Response-time limits: 0.1 s, 1 s, 10 s

- **Source.** Nielsen, *Usability Engineering*, Academic Press, 1993, chapter 5; web version "Response Times:
  The 3 Important Limits" (NN/g, read). Nielsen cites Miller 1968 (AFIPS Fall Joint Computer Conference) and Card,
  Robertson and Mackinlay 1991 (CHI'91).
- **What it says.** About 0.1 s: the system feels instantaneous (direct manipulation), no feedback needed other
  than the result. About 1.0 s: the user's flow of thought stays unbroken though the delay is noticed; show
  feedback beyond 1 s. About 10 s: the limit for keeping attention on the dialogue; beyond it give a percent-done
  indicator and a way to interrupt.
- **Popular misstatement.** These are not Nielsen's own measurements. Nielsen restates earlier work; every limit
  is stated as "about" and tied to the kind of task. They should not be read as exact thresholds. Miller 1968 and
  Card et al. 1991 were seen only through Semantic Scholar metadata, so the earlier work is unread.
- **Confidence.** Medium (original sources unread).

### 3.5 Other findings the survey touched

- Nielsen and Landauer's problem-discovery model (sections 2.1 and 2.3).
- Jakob's Law (from the NN/g heuristics page): people spend most of their time on other products, so they
  expect yours to work like those. A practitioner rule, not a measured law.
- Not surveyed: Doherty threshold, steering law, power law of practice, Weber and Fechner. Add on request.

## 4. Where the frameworks overlap and differ

Overlap, shown by names across the sets:

- **Feedback and visible state.** Nielsen 1, Shneiderman 3, Norman (feedback, gulf of evaluation), Tognazzini
  (state, latency reduction), ISO 9241-110 (self-descriptiveness), ISO 9241-112 (detectability).
- **Consistency and convention.** Nielsen 4, Shneiderman 1, Tognazzini (consistency), ISO (conformity with user
  expectations), Norman (conventions as cultural constraints).
- **Error prevention and recovery.** Nielsen 5 and 9, Shneiderman 5 and 6, Norman (constraints), ISO (use error
  robustness), Quesenbery (error tolerant). Quesenbery and ISO 9241-11 intro both treat use errors as part of usability.
- **User control and undo.** Nielsen 3, Shneiderman 6 and 7, ISO (controllability), Tognazzini (autonomy).
- **Memory load.** Nielsen 6, Shneiderman 8, Gerhardt-Powals (several), Norman (mapping, conceptual model).
- **Learnability and expert efficiency.** Nielsen 7, Shneiderman 2, ISO (learnability), Quesenbery, Tognazzini
  (learnability, efficiency of the user).
- **Minimalism.** Nielsen 8, Gerhardt-Powals 8, ISO 9241-112 (conciseness), Tognazzini (simplicity).

Differences:

- **Level.** Nielsen, Shneiderman and the ISO set are general rules for review. Norman is explanatory theory
  (why interfaces fail). Fitts, Hick and Miller are quantitative laws. WCAG is testable criteria. IEC, ISA and
  ISO 11064 cover physical and process-control interfaces that the general sets ignore.
- **Definition of success.** ISO 9241-11 defines usability as an outcome in context (effectiveness, efficiency,
  satisfaction). Nielsen's heuristics describe interface properties. Morville and Quesenbery widen to
  experience; Morville's honeycomb mixes usability with business value.
- **Unique to one source.** Closure (Shneiderman 4), universal usability (Shneiderman 2), data fusion
  (Gerhardt-Powals), user engagement (ISO 2020), signifiers and conceptual models (Norman), perceivable and
  robust (WCAG), emergency-stop and colour coding (IEC).
- **Scope exclusions.** ISO 9241-110:2020 excludes safety-critical and AI-feature specifics; no surveyed source
  gives a mature heuristic set for AI-driven or agentic interfaces (Microsoft's guidelines are a lead only).
- **Evidence base.** Only Nielsen's set has a published factor analysis behind it (249 problems, 1994). Others
  rest on experience or standards committees. No independent validation study of any set was read.

## 5. Source reachability and what was only read through a secondary

Read in the original: Nielsen heuristics page and its two companion method pages; Shneiderman's page; Tognazzini's
page; Norman's jnd.org articles; ISO 9241-11 official preview; ISO 9241-110 official preview (front matter);
Spencer 2000 PDF; Brooke 1996 chapter; Morville; Quesenbery 2001; Silver 2007; NN/g severity and response-time
pages; Cowan 2001; Miller 1956; WCAG 2.2 (W3C and raw source); parts of MacKenzie 1992.

Read only through a secondary or lead: Wharton et al. 1994 (via Spencer and NN/g); Crampton Smith's four
dimensions (via Silver); Gerhardt-Powals list (via three reproductions); Hertzum and Jacobsen, Faulkner, Gray and
Salzman, CUE-4 detail (search summaries or author page); Norman's seven-principle count; 2006 ISO names; SUS
standing figures; most HMI standards.

Failed twice or blocked: Springer (Faulkner), Taylor & Francis (Hertzum), core.ac.uk PDF, W3C TR via two tools
(read through other routes), Cockburn 2007, Colorado ICS 93-07 PDF (scanned). Search-engine summaries were used
for leads only.

## 6. Open questions

- Does Norman's book call its principle count six or seven? Needs an authorised copy.
- What did the 2006 ISO 9241-110 text name and define? Preview PDF at sis.se/api/document/preview/907276/ not read.
- Which paper holds the Gerhardt-Powals "first two authors" sentence?
- Exact CUE-4 totals, and whether the CUE-4 conclusion matches the published paper's abstract.
- Faulkner 2003 numbers and Hertzum and Jacobsen's any-two agreement values, from the publisher pages.
- Original sources for Fitts 1954, Hick 1952, Hyman 1953, Miller 1968 and Card et al. 1991 (pages and statements).
- SUS licence statement: where does the free-use wording live, and is it current?
- Standard HMI documents (ISO 11064, ISA-101, IEC 60073 colour table) beyond abstracts.
- Whether to include Weinschenk and Barker's 20 voice-interface categories after reading a copy.
- Whether to survey the unsurveyed candidates in 1.14, especially a heuristic set for AI interfaces.
