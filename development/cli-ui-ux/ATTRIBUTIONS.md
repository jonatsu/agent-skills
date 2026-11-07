# Attributions

- Author: Joonas Onatsu
- License: `MIT`

## Third-party Sources

### Aanand Prasad, Ben Firshman, Carl Tashian, and Eva Parish: Command Line Interface Guidelines

- Source: <https://clig.dev/>, repository <https://github.com/cli-guidelines/cli-guidelines>
- License: `CC-BY-SA-4.0`
- Version: `697d6a2`

The guidelines supplied most of the subjects the conventions cover: the stdout and stderr split, help and
version behaviour, error content, prompts only on terminals, a no-input flag, confirmation and dry runs,
configuration precedence, XDG locations, signal handling, and consent for telemetry. Every sentence was written
independently; no prose was copied due to the content license.

### Adedayo Agarau: CLI for Everybody, a Content Designer's Guide to Command-line UX

- Source:
  <https://medium.com/@adedayoagarau/cli-for-everybody-a-content-designers-guide-to-command-line-ux-39d574b4cd86>
- License: `LicenseRef-Proprietary`
- Version: December 2025

The article supplied help that leads with purpose and examples, errors that name a next step, confirmations that
name the target and say whether the action can be undone, announcing a consequential default, colour that adds
to text, and its counter-example of a generic destructive remedy. All rights are reserved; nothing was copied.

### Kfir Barki: 3 Steps to Create an Awesome UX in a CLI Application

- Source: <https://opensource.com/article/22/7/awesome-ux-cli-application>
- License: `CC-BY-SA-4.0`
- Version: July 2022

The article supplied one enum option in place of interacting boolean flags, a stable output contract, and the
positional-argument question the arguments section settles. No prose was copied due to the content license.

### Lucas da Costa: UX Patterns for CLI Tools

- Source: <https://www.lucasfcosta.com/blog/ux-patterns-cli-tools>
- License: `LicenseRef-Unspecified-Copyleft`
- Version: 2022-06-01

The post supplied typo suggestions, validating input before work begins, progress with counts and phases,
saying whose problem an error is, stable error codes, and stdin input for pipelines. Its notice reads "Copyleft,
all rights reversed" without naming a license; nothing was copied.

### Alister Lewis-Bowen: claude-cli-ux-skill

- Source: <https://github.com/ali5ter/claude-cli-ux-skill>
- License: `MIT`
- Version: `aa4fa9a30701729f4eb70e256c2c64afa563be71`

The skill supplied the set of review areas that the review reference rescopes, from discovery and safety to
consistency and accessibility. Nothing was copied.

### GitHub CLI Team: Primer Guidelines for `gh`

- Source: <https://github.com/cli/cli/tree/trunk/docs/primer>
- License: `MIT`
- Version: `a6cb3e8`

The guidelines supplied noun-verb grammar for tools with several resource kinds and colour that only enhances
meaning. Nothing was copied.

### Microsoft: Command-line Design Guidance for System.CommandLine

- Source: <https://learn.microsoft.com/en-us/dotnet/standard/commandline/design-guidance>
- License: `CC-BY-4.0`
- Version: 2025-06-19

The guidance supplied the view of verb-first grammar as verbs applied across resource types, which the grammar
test uses. Nothing was copied.

### Heroku: CLI Style Guide

- Source: <https://devcenter.heroku.com/articles/cli-style-guide>
- License: `LicenseRef-Proprietary`
- Version: 2025-01-31

The guide supplied topic-and-command grammar, flags preferred over positional arguments, and prompts that can
always be bypassed. Nothing was copied.

### Free Software Foundation: GNU Coding Standards

- Source: <https://www.gnu.org/prep/standards/>, read from the gnulib copy
  <https://github.com/coreutils/gnulib/blob/master/doc/standards.texi>
- License: `GFDL-1.3-or-later`
- Version: gnulib `7755639`

The standards supplied the `--help` and `--version` contract, long forms for every option, the `program: message` error
prefix, and the `file:line:col:` location prefix. No prose was copied due to the content license.

### IEEE and The Open Group: POSIX Utility Conventions

- Source: <https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html>
- License: `LicenseRef-Proprietary`
- Version: POSIX.1-2024

The conventions supplied `--` as the end of options and `-` as standard input. Nothing was copied.

### Joshua Stein: NO_COLOR

- Source: <https://no-color.org/>
- License: `LicenseRef-No-License`
- Version: 2026-11-03

The convention supplied disabling colour when `NO_COLOR` is set and non-empty. No license is stated; nothing was
copied.

### Jan Niklas Hasse: CLICOLOR and CLICOLOR_FORCE

- Source: <https://bixense.com/clicolors/>
- License: `LicenseRef-No-License`
- Version: read 2026-11-07

The proposal supplied forcing colour on and its order against `NO_COLOR`. No license is stated; nothing was
copied.

### Freedesktop.org: XDG Base Directory Specification

- Source: <https://specifications.freedesktop.org/basedir-spec/latest/>
- License: `LicenseRef-No-License`
- Version: read 2026-11-07

The specification supplied the user config, data, cache, and state locations. No license is stated; nothing was
copied.
