"""The Painfully Honest Out-of-Office — make.fun entry (honest-ooo-a).

This program writes the out-of-office auto-reply to /output/entry.txt.

Sealed gate, from the kit's RULES.txt: the output file must hold
UTF-8 text, 1 to 200 characters, more than whitespace, on one line.
The judge then compares replies two at a time, weighing honesty
first, then politeness, then the turn of phrase — the most honest
reply that still sounds professional takes the reward.
"""

import os

# The honesty is the queue: emails will be answered in order of
# how much the sender is liked, and yours is in the queue,
# somewhere. Polite enough to send, honest enough to sting — the
# balance the brief asks for.
ENTRY_TEXT = (
    "I'm away until Monday and will answer emails in order of how "
    "much I like you \u2014 yours is in the queue, somewhere."
)

CHAR_LIMIT = 200
FILE_NAME = "entry.txt"


def problems_in(text, limit):
    """List every way `text` breaks the sealed gate; empty means valid."""
    found = []
    if not isinstance(text, str):
        return ["entry must be a string"]
    if not text.strip():
        return ["entry must not be only white space"]
    if text != text.strip():
        found.append("entry has leading or trailing whitespace")
    if len(text) > limit:
        found.append("entry is %d chars, limit is %d" % (len(text), limit))
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    return found


def output_dir():
    """Where the entry goes: env override, else the kit's /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def emit(text, directory):
    """Validate, then write `text` to <directory>/entry.txt."""
    bad = problems_in(text, CHAR_LIMIT)
    if bad:
        raise ValueError("gate failed: " + "; ".join(bad))
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, FILE_NAME)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(text)
    return target


def report(path):
    """Print what was written, with the gate numbers, for the log."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    print("Wrote %s" % path)
    print("chars: %d / %d (%d headroom), words: %d, lines: 1"
          % (len(text), CHAR_LIMIT, CHAR_LIMIT - len(text),
             len(text.split())))
    print(text)


def run():
    report(emit(ENTRY_TEXT, output_dir()))


if __name__ == "__main__":
    run()
