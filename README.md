# AI Trend Website Generator

A small Python script that looks at a website's HTML/CSS/JS, picks out the visual
patterns that make a site look "AI-generated", and builds a new scroll-driven
site based on what it found.

I started this because so many vibe-coded sites look alike: dark backgrounds,
blue/purple gradients, glassy transparent cards, the same techy fonts. I wanted
to see if those patterns could be used as a starting point for something
different, instead of just complaining about them.

## How it works

1. Reads the HTML, CSS and JS files in the input folder.
2. Uses regex to detect common patterns: colors, gradients, fonts,
   transparency/blur effects.
3. Fills a page template with what it found and writes the result to the
   output folder.

There's no machine learning here. It's just pattern matching and a template.

## Usage

    python trend_website_generator.py --input ./path/to/site --output ./path/to/output

Then open `./path/to/output/index.html` in your browser.

## What you get

- A static HTML/CSS/JS site
- Three full-screen sections with scroll snapping
- Small animations tied to scroll position
- A layout that works on mobile

## Limitations

- Detection is heuristic. It can miss patterns or pick up the wrong ones.
- Every generated site follows the same template, so the structure will look
  similar. Only colors, fonts and effects change.
- It only reads plain HTML/CSS/JS files, not sites built with a framework or bundler.

## Feedback

If you try it, I'd like to hear what worked and what didn't. Open an issue
with the input site and what you got.
