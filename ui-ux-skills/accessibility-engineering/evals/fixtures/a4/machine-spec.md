# Parking ticket machine, model P3: interface specification

The machine stands on the pavement in a city centre and is used by anyone parking on the street. It is a closed
system: users cannot attach their own devices or install software.

- **Screen:** a 10-inch colour touchscreen. Its centre is 1.6 m above the ground, under a glass canopy.
- **Input:** touch only. Buttons on the screen are 12 mm squares. There are no physical keys.
- **Flow:** choose a zone, enter the car's plate number on an on-screen keyboard, choose a duration, then pay by
  contactless card. The plate keyboard has no feedback other than the characters appearing on the screen.
- **Payment:** the card reader sits beside the screen. After the user taps "Pay", the payment step times out
  after 20 seconds and returns to the start, losing everything entered. There is no way to ask for more time.
- **Status light:** a ring around the card reader glows green when payment succeeds and red when it fails.
  The screen then returns to the start without a message.
- **Sound:** a short beep on each touch. No speech output.
- **Help:** a sticker on the side with a phone number.
