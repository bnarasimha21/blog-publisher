# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Blog Publisher is a desktop GUI application (tkinter) that converts dictated text into polished blog posts using Claude AI and publishes them to WordPress as drafts.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python blog_publisher.py
```

## Architecture

Single-file application (`blog_publisher.py`) with one main class:

- **BlogPublisher**: Manages the tkinter GUI and all functionality
  - `convert_to_blog()`: Sends dictated text to Claude API (claude-sonnet-4-20250514) with a formatting prompt, expects `[TITLE]` and `[CONTENT]` markers in response
  - `publish_to_wordpress()`: Posts to WordPress REST API (`/wp-json/wp/v2/posts`) using Basic Auth with application password
  - WordPress URL is hardcoded to `https://thecodeshell.wordpress.com`

## Key Implementation Details

- Posts are created as drafts by default (configurable via `'status': 'draft'` in `publish_to_wordpress()`)
- Credentials are stored only in memory, never persisted to disk
- The Claude prompt instructs output formatting with `[TITLE]` and `[CONTENT]` markers for parsing
