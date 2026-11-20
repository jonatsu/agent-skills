#!/usr/bin/env python3
"""Compute the WCAG 2.x contrast ratio of a foreground colour against one or more backgrounds.

Usage:
    contrast.py [--json] FOREGROUND BACKGROUND [BACKGROUND ...]

Colours are hex: RGB, RRGGBB, or with an alpha channel RGBA and RRGGBBAA, each with or without a leading `#`.
A translucent foreground is composited over each background before the ratio is computed. A background must be
opaque, because its ratio depends on whatever lies behind it.

Give several backgrounds for text over an image or a gradient: sample the colours the text crosses, and the
report judges the worst of them, because contrast fails where it is lowest.

Each verdict compares the exact ratio with its threshold; WCAG does not round. The printed ratio is truncated
to two decimals, so a failing 4.498:1 prints as 4.49, never as 4.50.

Large text is at least 18 point (24 CSS pixels), or 14 point (about 18.7 CSS pixels) when bold.

Exit status: 0 when the ratio was computed, whatever the verdicts; 2 for invalid usage or an unreadable colour.

Standard library only; Python 3.9 or later.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import asdict, dataclass

EXIT_OK = 0
EXIT_USAGE = 2

HEX_COLOUR = re.compile(r"#?([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})")

# Each threshold with the success criterion and level that set it.
THRESHOLDS: tuple[tuple[str, str, float], ...] = (
    ("normal text", "1.4.3 Contrast (Minimum), AA", 4.5),
    ("large text", "1.4.3 Contrast (Minimum), AA", 3.0),
    ("controls and graphics", "1.4.11 Non-text Contrast, AA", 3.0),
    ("normal text, enhanced", "1.4.6 Contrast (Enhanced), AAA", 7.0),
    ("large text, enhanced", "1.4.6 Contrast (Enhanced), AAA", 4.5),
)


class ColourError(ValueError):
    """A colour argument that is not a readable hex colour."""


@dataclass(frozen=True)
class Colour:
    """An sRGB colour with 8-bit channels and an alpha between 0 and 1."""

    red: int
    green: int
    blue: int
    alpha: float = 1.0

    def hex(self) -> str:
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"


def parse_colour(text: str) -> Colour:
    """Read a hex colour such as `#777`, `777777`, or `#00000080`.

    Raises:
        ColourError: when the text is not a 3, 4, 6, or 8 digit hex colour.
    """
    match = HEX_COLOUR.fullmatch(text.strip())
    if match is None:
        raise ColourError(f"not a hex colour: {text!r} (expected RGB, RGBA, RRGGBB, or RRGGBBAA)")
    digits = match.group(1)
    if len(digits) in (3, 4):
        digits = "".join(digit * 2 for digit in digits)
    channels = [int(digits[index : index + 2], 16) for index in range(0, len(digits), 2)]
    alpha = channels[3] / 255 if len(channels) == 4 else 1.0
    return Colour(channels[0], channels[1], channels[2], alpha)


def composite(foreground: Colour, background: Colour) -> Colour:
    """Blend a translucent foreground over an opaque background, as a browser paints it."""
    if foreground.alpha >= 1.0:
        return foreground

    def blend(top: int, bottom: int) -> int:
        return round(top * foreground.alpha + bottom * (1 - foreground.alpha))

    return Colour(
        blend(foreground.red, background.red),
        blend(foreground.green, background.green),
        blend(foreground.blue, background.blue),
    )


def relative_luminance(colour: Colour) -> float:
    """Return WCAG relative luminance, from 0 for black to 1 for white."""

    def linear(channel: int) -> float:
        value = channel / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    return 0.2126 * linear(colour.red) + 0.7152 * linear(colour.green) + 0.0722 * linear(colour.blue)


def contrast_ratio(first: Colour, second: Colour) -> float:
    """Return the contrast ratio of two opaque colours, from 1 to 21."""
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def truncated(ratio: float) -> str:
    """Format a ratio to two decimals without rounding up across a threshold."""
    return f"{math.floor(ratio * 100) / 100:.2f}"


@dataclass(frozen=True)
class Measurement:
    """The ratio of the foreground, as painted, against one background."""

    background: str
    painted_foreground: str
    ratio: float
    ratio_display: str


@dataclass(frozen=True)
class Verdict:
    """Whether the worst ratio meets one threshold."""

    use: str
    criterion: str
    threshold: float
    passes: bool


@dataclass(frozen=True)
class Report:
    """Every measurement, the worst of them, and the verdicts for the worst."""

    foreground: str
    measurements: list[Measurement]
    worst: Measurement
    verdicts: list[Verdict]


def measure(foreground: Colour, background: Colour) -> Measurement:
    painted = composite(foreground, background)
    ratio = contrast_ratio(painted, background)
    return Measurement(background.hex(), painted.hex(), ratio, truncated(ratio))


def build_report(foreground: Colour, backgrounds: list[Colour]) -> Report:
    measurements = [measure(foreground, background) for background in backgrounds]
    worst = min(measurements, key=lambda measurement: measurement.ratio)
    described = foreground.hex() if foreground.alpha >= 1.0 else f"{foreground.hex()} at alpha {foreground.alpha:.2f}"
    verdicts = [
        Verdict(use, criterion, threshold, worst.ratio >= threshold) for use, criterion, threshold in THRESHOLDS
    ]
    return Report(described, measurements, worst, verdicts)


def render_text(report: Report) -> str:
    lines = [f"foreground {report.foreground}"]
    lines.extend(f"  on {item.background}: {item.ratio_display}:1" for item in report.measurements)
    if len(report.measurements) > 1:
        lines.append(f"worst: {report.worst.ratio_display}:1 on {report.worst.background}")
    for verdict in report.verdicts:
        outcome = "pass" if verdict.passes else "FAIL"
        lines.append(f"  {outcome}  {verdict.use}, {verdict.threshold:g}:1 ({verdict.criterion})")
    return "\n".join(lines)


def parse_arguments(arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute the WCAG 2.x contrast ratio of a foreground colour against each background.",
        epilog="Several backgrounds report each ratio and judge the worst, for text over an image or gradient.",
    )
    _ = parser.add_argument("foreground", help="hex colour of the text or control, optionally with alpha")
    _ = parser.add_argument("backgrounds", nargs="+", metavar="background", help="opaque hex background colour")
    _ = parser.add_argument("--json", action="store_true", help="print the report as JSON")
    return parser.parse_args(arguments)


def main(arguments: list[str] | None = None) -> int:
    options = parse_arguments(sys.argv[1:] if arguments is None else arguments)
    foreground_text: str = options.foreground
    background_texts: list[str] = options.backgrounds
    as_json: bool = options.json
    try:
        foreground = parse_colour(foreground_text)
        backgrounds = [parse_colour(text) for text in background_texts]
    except ColourError as error:
        print(f"contrast.py: {error}", file=sys.stderr)
        return EXIT_USAGE
    translucent = [text for text in background_texts if parse_colour(text).alpha < 1.0]
    if translucent:
        print(
            f"contrast.py: background {translucent[0]!r} is translucent; give the opaque colour it shows "
            "over its own background",
            file=sys.stderr,
        )
        return EXIT_USAGE
    report = build_report(foreground, backgrounds)
    print(json.dumps(asdict(report), indent=2) if as_json else render_text(report))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
