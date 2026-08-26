"""Tests for the site's package-card renderer.

Third and last sink for hvtiR's manifest. This one owns the HTML house style:
`<div class="pkg">` cards with `<span class="pkg-role">` badges, and &mdash;
entities where the README uses a literal em dash from the same input.
"""
import json
import re
import unittest

from render_packages import MARKER_BEGIN, MARKER_END, number_word, render_block, splice

MANIFEST = {
    "generated_from": "hvtiR 9.9.9",
    "counts": {"members": 4, "members_on_cran": 1, "members_github_only": 3},
    "cran_member_names": ["alpha"],
    "packages": [
        {"package": "alpha", "repo": "ehrlinger/alpha", "url": "https://github.com/ehrlinger/alpha",
         "family": "member", "blurb": "First -- on CRAN.", "cran": "alpha", "status": "stable", "role": None},
        {"package": "beta", "repo": "ehrlinger/beta-repo", "url": "https://github.com/ehrlinger/beta-repo",
         "family": "member", "blurb": "Second, GitHub only.", "cran": None, "status": "wip", "role": None},
        {"package": "gamma", "repo": "ehrlinger/gamma", "url": "https://github.com/ehrlinger/gamma",
         "family": "member", "blurb": "Third.", "cran": None, "status": "stable", "role": None},
        {"package": "delta", "repo": "ehrlinger/delta", "url": "https://github.com/ehrlinger/delta",
         "family": "member", "blurb": "Fourth.", "cran": None, "status": "stable", "role": None},
        {"package": "sassy", "repo": "ehrlinger/sassy", "url": "https://github.com/ehrlinger/sassy",
         "family": "standalone", "blurb": "Not an R package.", "cran": None, "status": "stable", "role": "Maintainer"},
        {"package": "The Book", "repo": "ehrlinger/book", "url": "https://example.org/book/",
         "family": "book", "blurb": "A book.", "cran": None, "status": "stable", "role": None},
    ],
}


def cards(block):
    """Split the block into per-card fragments, in document order."""
    return [c for c in block.split('<div class="pkg">')[1:]]


def names_in(fragment):
    """Linked package names in a fragment, in document order."""
    return re.findall(r'<a href="[^"]*">([^<]*)</a>', fragment)


class GridSplitTests(unittest.TestCase):
    def setUp(self):
        self.block = render_block(MANIFEST)

    def test_two_grids_are_emitted(self):
        self.assertEqual(self.block.count('<div class="pkg-grid">'), 2)

    def test_grids_are_balanced(self):
        self.assertEqual(self.block.count("<div"), self.block.count("</div>"))

    def test_first_grid_holds_cran_members_standalone_and_book(self):
        first = self.block.split('<div class="pkg-grid">')[1]
        self.assertEqual(names_in(first), ["alpha", "sassy", "The Book"])

    def test_second_grid_holds_only_github_only_members(self):
        second = self.block.split('<div class="pkg-grid">')[2]
        self.assertEqual(names_in(second), ["beta", "gamma", "delta"])


class BadgeTests(unittest.TestCase):
    def setUp(self):
        self.block = render_block(MANIFEST)

    def _card(self, needle):
        return next(c for c in cards(self.block) if needle in c)

    def test_a_cran_member_gets_a_cran_badge(self):
        self.assertIn('<span class="pkg-role">CRAN</span>', self._card("/alpha"))

    def test_a_wip_member_gets_a_wip_badge(self):
        self.assertIn('<span class="pkg-role">WIP</span>', self._card("/beta-repo"))

    def test_a_role_becomes_its_own_badge(self):
        self.assertIn('<span class="pkg-role">Maintainer</span>', self._card("/sassy"))

    def test_the_book_gets_a_book_badge(self):
        self.assertIn('<span class="pkg-role">Book</span>', self._card("example.org/book"))

    def test_a_plain_stable_member_gets_no_badge(self):
        self.assertNotIn("pkg-role", self._card("/gamma"))


class HtmlTests(unittest.TestCase):
    def test_ascii_dash_becomes_an_mdash_entity_not_a_literal(self):
        block = render_block(MANIFEST)
        self.assertIn("First &mdash; on CRAN.", block)
        self.assertNotIn(" -- ", block)

    def test_markup_characters_in_a_blurb_are_escaped(self):
        m = json.loads(json.dumps(MANIFEST))
        m["packages"][2]["blurb"] = 'Uses <b> & "quotes".'
        card = next(c for c in cards(render_block(m)) if "/gamma" in c)
        self.assertIn("&lt;b&gt;", card)
        self.assertIn("&amp;", card)
        self.assertNotIn("<b>", card)

    def test_a_package_name_is_escaped_too(self):
        m = json.loads(json.dumps(MANIFEST))
        m["packages"][2]["package"] = "gam<ma"
        self.assertIn("gam&lt;ma", render_block(m))

    def test_the_book_uses_its_homepage_not_the_repo(self):
        card = next(c for c in cards(render_block(MANIFEST)) if "The Book" in c)
        self.assertIn('href="https://example.org/book/"', card)
        self.assertNotIn("github.com/ehrlinger/book", card)


class FamilySentenceTests(unittest.TestCase):
    def test_counts_are_derived_and_spelled_out(self):
        self.assertIn("four member packages, the three below", render_block(MANIFEST))

    def test_cran_members_are_named_in_code_tags(self):
        self.assertIn("<code>alpha</code>", render_block(MANIFEST))

    def test_number_word_matches_the_other_renderers(self):
        self.assertEqual(number_word(11), "eleven")
        self.assertEqual(number_word(9), "nine")
        self.assertEqual(number_word(97), "97")

    def test_no_dangling_plus_when_no_member_is_on_cran(self):
        m = json.loads(json.dumps(MANIFEST))
        for p in m["packages"]:
            p["cran"] = None
        m["cran_member_names"] = []
        m["counts"] = {"members": 4, "members_on_cran": 0, "members_github_only": 4}
        block = render_block(m)
        self.assertIn("four member packages, listed below.", block)
        self.assertNotIn(" above.", block)


class CountDriftTests(unittest.TestCase):
    def test_a_contradictory_member_count_is_an_error(self):
        m = json.loads(json.dumps(MANIFEST))
        m["counts"]["members"] = 99
        with self.assertRaises(ValueError):
            render_block(m)

    def test_a_cran_name_absent_from_the_packages_is_an_error(self):
        m = json.loads(json.dumps(MANIFEST))
        m["cran_member_names"] = ["ghost"]
        with self.assertRaises(ValueError) as ctx:
            render_block(m)
        self.assertIn("ghost", str(ctx.exception))


class SpliceTests(unittest.TestCase):
    DOC = f"<section>\n{MARKER_BEGIN}\nOLD\n{MARKER_END}\n</section>\n"

    def test_only_the_marked_region_is_replaced(self):
        out = splice(self.DOC, "NEW")
        self.assertIn("<section>", out)
        self.assertIn("</section>", out)
        self.assertNotIn("OLD", out)

    def test_a_missing_marker_is_an_error_naming_it(self):
        with self.assertRaises(ValueError) as ctx:
            splice("<p>nothing</p>", "NEW")
        self.assertIn(MARKER_BEGIN, str(ctx.exception))

    def test_rendering_twice_is_idempotent(self):
        once = splice(self.DOC, render_block(MANIFEST))
        self.assertEqual(once, splice(once, render_block(MANIFEST)))


class NetworkFailureTests(unittest.TestCase):
    def test_exhausted_retries_raise_network_error(self):
        import render_packages as rp
        rp.fetch_text = lambda url, timeout=0: (_ for _ in ()).throw(OSError("down"))
        try:
            with self.assertRaises(rp.NetworkError):
                rp.load_manifest("https://example.org/m.json")
        finally:
            rp.fetch_text = rp._fetch_text

    def test_a_malformed_manifest_is_not_a_network_problem(self):
        import render_packages as rp
        rp.fetch_text = lambda url, timeout=0: json.dumps({"packages": []})
        try:
            with self.assertRaises(ValueError):
                rp.load_manifest("https://example.org/m.json")
        finally:
            rp.fetch_text = rp._fetch_text


if __name__ == "__main__":
    unittest.main()
