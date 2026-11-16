# The Principles in Detail

Each principle below gives its questions, how it shows in each interaction dimension, and the established
principles it draws on. Ask the questions for the dimensions the medium has, and skip the rest.

The dimensions come from Kevin Silver. He reports Gillian Crampton Smith's four (words, visual
representations, physical objects or space, and time) and adds a fifth, behaviour.

## Contents

1. Visible status and feedback
2. Match the user's world and conventions
3. Prevent errors
4. Help users recover
5. User control
6. Recognition over recall
7. Learnable and efficient
8. Minimal

## 1. Visible Status and Feedback

- Can the user tell what state the system is in, including its mode, without acting?
- Does every action get a response the user notices, within about a second?
- Does a long operation show that it is running, and does its end say how it went?

Words: a status line or a spoken confirmation. Visuals: an indicator, a progress bar, a changed control.
Physical: a click, a detent, a light beside the control. Time: a response within the limits in
[laws.md](laws.md#response-time-limits). Behaviour: a state change that is visible where the user is looking.

A mode the user cannot see is the classic failure, because the same action then does different things. Caps
Lock with no indicator light is the familiar example.

Sources: Nielsen 1, Shneiderman 3 (feedback) and 4 (closure), Norman's feedback and gulf of evaluation, ISO
9241-110 self-descriptiveness.

## 2. Match the User's World and Conventions

- Do labels use the user's words rather than the system's?
- Does the interface work like the others its users already know, on the same platform or device class?
- Does the layout of the controls map onto what they control?
- Does the same word, icon, or control mean the same thing everywhere in the interface?

Words: domain vocabulary, not internal names. Visuals: platform conventions for icons and layout. Physical: up
means more, a control sits next to what it affects. Time and behaviour: steps in the order users think of them.

Sources: Nielsen 2 and 4, Shneiderman 1, Norman's mappings and conventions, ISO 9241-110 conformity with user
expectations.

## 3. Prevent Errors

- Does the design make the wrong action hard and the right one obvious?
- Are rules and formats shown before the user can break them?
- Does a destructive or costly action need a deliberate step, with defaults that do the least harm?

Words: the format and constraints stated beside the input. Visuals: an unavailable action shown as such.
Physical: a guard or a two-handed action for a dangerous control, distinct shapes for different functions.
Time: a short delay before an irreversible step, such as an email client's undo-send window. Behaviour: an
action that is safe to repeat, such as a payment button that charges once however often it is pressed.

Sources: Nielsen 5, Shneiderman 5, Norman's constraints, ISO 9241-110 use error robustness.

## 4. Help Users Recover

- Does an error say what went wrong, where, and how to fix it, in plain words?
- Is the user's work kept after an error?
- Can a mistake be reversed, or at least repaired without starting over?

Words: a specific message at the place of the error. Visuals: the failing field or part highlighted. Physical:
a reset that returns to a known state. Behaviour: input preserved, a safe retry.

Sources: Nielsen 9, Shneiderman 5 and 6, Quesenbery's error tolerance.

## 5. User Control

- Can the user cancel, go back, or leave any state, by a means they can see?
- Does the system act only when the user asks, and avoid surprising changes?
- Can a timeout or automatic step be paused or extended?

Physical and behaviour: a visible way out of every mode, such as the Back key on a television's menus. Time: a
timeout the user can extend, such as a session warning with a "Stay signed in" button.

Sources: Nielsen 3, Shneiderman 6 and 7, ISO 9241-110 controllability.

## 6. Recognition Over Recall

- Are the options shown, or must the user remember a command, gesture, or code?
- Is information the user needs carried to where they need it, not left on a previous screen?
- Does each control carry a signifier: a cue that shows where and how to act?

Words: a visible name on every control and field. Visuals: menus and examples. Physical: printed symbols on
each button, as on a microwave keypad. Voice: the options offered, not expected to be guessed.

A signifier is the perceivable cue; an affordance is the action an object allows. Norman's revised account says
signifiers matter more to designers than affordances, so fix a hidden function by adding a signifier.

Sources: Nielsen 6, Shneiderman 8, Norman's signifiers and discoverability.

## 7. Learnable and Efficient

- Can a first-time user complete the main task without help or a manual?
- Does a frequent user have shortcuts that do not get in the novice's way?
- Is help available at the point of need, short and task-focused?

Sources: Nielsen 7 and 10, Shneiderman 2, ISO 9241-110 learnability, Quesenbery's easy to learn and efficient.

## 8. Minimal

- Does each screen, display, or prompt carry only what the current task needs?
- Does secondary information compete with what the user must see?

Words: short prompts, especially in voice, where users cannot skim. Visuals: one clear primary action.

Sources: Nielsen 8, ISO 9241-112 conciseness (as ISO 9241-110 lists it), and Gerhardt-Powals' principle of
showing only the needed information.
