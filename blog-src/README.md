# Blog source

Quarto source for <https://ehrlinger.github.io/blog/>. It renders into `../blog/`,
which GitHub Pages serves from `main` alongside the hand-built homepage.
Nothing here touches `index.html` or the `sync-packages` workflow.

## Write a post

1. Make a folder under `posts/` named `YYYY-MM-DD-short-slug/` with an `index.qmd`.
2. Front matter needs `title`, `description`, `date` and `categories`. Add
   `rstats` to `categories` for anything R-related; that category has its own
   feed (`index-rstats.xml`) for R-bloggers and R Weekly.
3. Put figures in the post folder. The first image becomes the social preview
   card on LinkedIn and Bluesky unless `image:` names another; posts without an
   image fall back to `share-card.png`.
4. Start with `draft: true`. Drafts show in `quarto preview` and are left out of
   the rendered site, the listing, the feeds and search.

`posts/2026-10-13-style-check/` is a permanent draft that exercises every element
the theme styles. Preview it after any change to `styles/`.

## Preview and publish

```sh
cd blog-src
quarto preview          # live reload, drafts visible
quarto render           # writes ../blog/
```

Commit `blog-src/` and `blog/` together; Pages serves the rendered files as
committed. Posts are frozen (`freeze: true` in `posts/_metadata.yml`), so R
chunks run only when that post changes, and the `_freeze/` folder must be
committed with them.

## Styling

- `styles/base.scss` holds type, layout and component rules shared by both themes.
- `styles/light.scss` and `styles/dark.scss` hold colors only. Light uses the
  homepage's navy, blue and steel; dark is derived from the same navy.
- Body text is Newsreader; headings, captions, tables and navigation are
  Atkinson Hyperlegible Next; code is Atkinson Hyperlegible Mono. All three load
  from Google Fonts in `_quarto.yml`.
- The stepped rule under each title is a CSS mask, so it takes the theme color.

SAS-to-R translations use a `panel-tabset` with `group="language"`, so a reader's
choice of tab carries across the page. Pandoc has no SAS highlighter, so SAS
blocks render unhighlighted on the same code panel.
