"""Render the Open-Source Software cards in index.html from hvtiR's manifest.

Third sink for the same manifest, after the CV Quarto source and the profile
README. This one owns the HTML house style: `<div class="pkg">` cards with
`<span class="pkg-role">` badges, and `&mdash;` where the README renders a
literal em dash from identical input.

Standard library only -- no pip install step on the runner.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
import time
import urllib.request
from pathlib import Path

MANIFEST_URL = "https://ehrlinger.github.io/hvtiR/members.json"
MARKER_BEGIN = "<!-- BEGIN:packages -->"
MARKER_END = "<!-- END:packages -->"
INSTALLER_URL = "https://github.com/ehrlinger/hvtiR"

_WORDS = (
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
)


class NetworkError(RuntimeError):
    """The manifest could not be fetched. Distinct from a malformed manifest."""


def number_word(n: int) -> str:
    return _WORDS[n] if 0 <= n < len(_WORDS) else str(n)


def _join(names: list[str]) -> str:
    tagged = [f"<code>{html.escape(n)}</code>" for n in names]
    if len(tagged) <= 1:
        return "".join(tagged)
    return f"{', '.join(tagged[:-1])} and {tagged[-1]}"


def _badge(pkg: dict) -> str:
    """At most one badge per card, in the order the site already uses."""
    label = None
    if pkg["cran"]:
        label = "CRAN"
    elif pkg["role"]:
        label = pkg["role"]
    elif pkg["family"] == "book":
        label = "Book"
    elif pkg["status"] == "wip":
        label = "WIP"
    if label is None:
        return ""
    return f'\n          <span class="pkg-role">{html.escape(label)}</span>'


def _card(pkg: dict) -> str:
    text = html.escape(pkg["blurb"]).replace(" -- ", " &mdash; ")
    if pkg["family"] == "book":
        text += " Quarto book, CC BY 4.0."
    return (
        '      <div class="pkg">\n'
        '        <div class="pkg-name">\n'
        f'          <a href="{html.escape(pkg["url"], quote=True)}">'
        f'{html.escape(pkg["package"])}</a>'
        f'{_badge(pkg)}\n'
        "        </div>\n"
        f'        <div class="pkg-desc">{text}</div>\n'
        "      </div>"
    )


def _grid(packages: list[dict]) -> str:
    body = "\n\n".join(_card(p) for p in packages)
    return f'    <div class="pkg-grid">\n\n{body}\n\n    </div>'


def render_block(manifest: dict) -> str:
    pkgs = manifest["packages"]
    counts = manifest["counts"]

    cran_members = [p for p in pkgs if p["family"] == "member" and p["cran"]]
    github_only = [p for p in pkgs if p["family"] == "member" and not p["cran"]]
    standalone = [p for p in pkgs if p["family"] == "standalone"]
    book = [p for p in pkgs if p["family"] == "book"]

    # Cards and sentence come from the same manifest, so a count that
    # disagrees with the package list is an upstream defect. Say so rather
    # than publishing a sentence contradicting the grid beneath it.
    members = len(cran_members) + len(github_only)
    if counts.get("members") != members:
        raise ValueError(
            f"manifest counts.members is {counts.get('members')} but it lists {members} members"
        )
    if counts.get("members_github_only") != len(github_only):
        raise ValueError(
            f"manifest counts.members_github_only is {counts.get('members_github_only')} "
            f"but it lists {len(github_only)}"
        )
    known = {p["package"] for p in cran_members}
    unknown = [n for n in manifest["cran_member_names"] if n not in known]
    if unknown:
        raise ValueError(
            f"manifest cran_member_names lists {', '.join(unknown)}, "
            "which is not a member carrying a cran field"
        )

    tail = (
        f"the {number_word(counts['members_github_only'])} below plus "
        f"{_join(manifest['cran_member_names'])} above."
        if manifest["cran_member_names"]
        else "listed below."
    )
    sentence = (
        f'    <p class="pkg-desc"><a href="{INSTALLER_URL}"><code>hvtiR</code></a> '
        "&mdash; a one-command installer, version status table, and environment "
        "diagnostic &mdash; resolves the family from public GitHub repositories and "
        f"version-checks it as a unit: {number_word(counts['members'])} member packages, "
        f"{tail}</p>"
    )

    return "\n".join([
        _grid(cran_members + standalone + book),
        "",
        "    <h3>The HVTI R package family</h3>",
        sentence,
        "",
        _grid(github_only),
    ])


def splice(document: str, block: str) -> str:
    start = document.find(MARKER_BEGIN)
    if start < 0:
        raise ValueError(f"{MARKER_BEGIN} not found; cannot splice")
    end = document.find(MARKER_END, start)
    if end < 0:
        raise ValueError(f"{MARKER_END} not found after {MARKER_BEGIN}; cannot splice")
    return f"{document[: start + len(MARKER_BEGIN)]}\n{block}\n{document[end:]}"


def _fetch_text(url: str, timeout: int = 30) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        if resp.status != 200:
            raise OSError(f"{url} returned HTTP {resp.status}")
        return resp.read().decode()


fetch_text = _fetch_text


def load_manifest(source: str, attempts: int = 3) -> dict:
    if source.startswith(("http://", "https://")):
        last = None
        for attempt in range(1, attempts + 1):
            try:
                body = fetch_text(source, timeout=30)
                break
            except Exception as exc:
                last = exc
                if attempt < attempts:
                    time.sleep(2 ** (attempt - 1))
        else:
            raise NetworkError(f"could not fetch {source} after {attempts} attempts: {last}")
        manifest = json.loads(body)
    else:
        manifest = json.loads(Path(source).read_text())

    for key in ("packages", "counts", "cran_member_names"):
        if key not in manifest:
            raise ValueError(f"manifest is missing required key: {key}")
    if not manifest["packages"]:
        raise ValueError("manifest lists no packages; refusing to publish an empty grid")
    return manifest


def main(argv=None) -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=MANIFEST_URL)
    parser.add_argument("--target", type=Path, default=root / "index.html")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest(args.manifest)
    except NetworkError as exc:
        if args.check:
            print(f"skipping check: {exc}", file=sys.stderr)
            return 0
        print(f"error: {exc}", file=sys.stderr)
        return 1

    current = args.target.read_text()
    rendered = splice(current, render_block(manifest))

    if args.check:
        if rendered != current:
            print(f"{args.target} is out of date with {args.manifest}", file=sys.stderr)
            return 1
        print(f"{args.target} is up to date")
        return 0

    if rendered == current:
        print(f"{args.target} already up to date")
        return 0
    args.target.write_text(rendered)
    print(f"updated {args.target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
