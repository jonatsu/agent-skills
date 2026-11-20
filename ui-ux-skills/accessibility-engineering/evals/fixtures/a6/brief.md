# Clinic booking widget: product brief

Patients will use this widget on the clinic's website, on phones and desktops, to book an appointment. Nothing
is built yet; the designer's notes below are the starting point.

- Patients pick a day on a calendar, then a time slot. Slots are a grid of coloured squares: green is free and
  red is taken. To book a double appointment, the patient drags across two slots.
- Each slot square is 20 by 20 pixels, so a whole week fits on a phone screen. A square shows its time only as a
  tooltip on hover.
- A picked slot is held for 3 minutes while the patient fills in their details. A countdown runs in the corner,
  and when it reaches zero the form clears.
- The details step asks for name, date of birth, phone, email, and the reason for the visit. Each field's name
  is placeholder text inside the box.
- On the confirmation step, the patient types their email address again so it can be checked against the first.
- Returning patients sign in with a password. Pasting into the password field is blocked, and they must also
  retype a six-character code shown as a distorted image, to stop bots.
- An error is shown as a red border around the field.

Many of the clinic's patients are older people, and some have low vision. The regional health authority requires
WCAG 2.2 Level AA for patient services.
