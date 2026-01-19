# Issue: Publish to WordPress button not working

## Bug Description

The "Publish to WordPress" button does not successfully publish blog posts to WordPress.

## Expected Behavior

After generating a blog post using the "Convert to Blog Post" button, clicking "Publish to WordPress" should create a draft post on the configured WordPress site.

## Current Behavior

The publish operation fails. Users report the button is not working as expected.

## Possible Causes

1. **WordPress.com API restrictions**: The hardcoded URL (`https://thecodeshell.wordpress.com`) is a WordPress.com hosted site. WordPress.com does not support Basic Auth for the REST API - it requires OAuth2 or Jetpack authentication.

2. **Button initially disabled**: The publish button is disabled by default (`state=tk.DISABLED` at line 80) and only enables after a successful conversion. Users may attempt to click it before converting.

3. **Credential handling**: The Basic Auth implementation may not work with WordPress.com's authentication requirements.

## Relevant Code

`blog_publisher.py:165-234` - The `publish_to_wordpress()` method handles the publishing logic using WordPress REST API with Basic Auth.

## Potential Fix

- For WordPress.com sites: Implement OAuth2 authentication or use the WordPress.com REST API instead of the generic WP REST API
- For self-hosted WordPress: Basic Auth should work but may require the "Application Passwords" feature (WordPress 5.6+) or a plugin
