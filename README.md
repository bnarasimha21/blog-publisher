# Blog Publisher - Super Whisper to WordPress

A simple desktop app that converts your dictated thoughts into polished blog posts and publishes them to your WordPress site.

## Features

- 🎤 Paste dictated text from Super Whisper (or any dictation tool)
- 🤖 Uses Claude AI to format your thoughts into a proper blog post
- 📝 Preview the generated blog post before publishing
- 🚀 One-click publishing to WordPress
- ✅ Posts are created as drafts for your review

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Claude API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

### 3. Set Up WordPress App Password

WordPress.com sites require an **Application Password** for API access:

1. Log in to your WordPress.com account
2. Go to https://wordpress.com/me/security/application-passwords
3. Enter an application name (e.g., "Blog Publisher")
4. Click "Add New Application Password"
5. Copy the generated password (it will look like: `xxxx xxxx xxxx xxxx xxxx xxxx`)
6. **Important**: Remove the spaces from the password when entering it in the app

Your username is your WordPress.com username (not your email).

### 4. Run the App

```bash
python blog_publisher.py
```

## How to Use

### Step 1: Configure
1. Enter your Claude API key
2. Enter your WordPress username
3. Enter your WordPress application password

### Step 2: Dictate
1. Use Super Whisper to dictate your blog post thoughts
2. Paste the dictated text into the "Your Dictated Thoughts" section

### Step 3: Convert
1. Click "Convert to Blog Post"
2. Claude will transform your dictation into a well-structured blog post
3. Review the generated content in the preview section

### Step 4: Publish
1. Make any edits if needed (directly in the preview box)
2. Click "Publish to WordPress"
3. Your post will be created as a **draft** on your WordPress site
4. Go to your WordPress dashboard to review and publish

## Tips for Better Results

### When Dictating with Super Whisper:
- Speak naturally about your topic
- Mention if you want specific sections or structure
- Don't worry about perfect grammar - Claude will fix it
- You can say "paragraph" or "new section" to indicate structure

### Example Dictation:
> "I want to write about my experience with llamaindex. Title should be something about building AI apps. So I've been working with llamaindex for a few months now and it's been really interesting. Paragraph. The main thing I've learned is that it makes it super easy to connect LLMs with your data. You can create indexes over your documents and then query them naturally. New section. Let me talk about the key features..."

## Troubleshooting

### "Failed to publish" Error
- Check that your WordPress credentials are correct
- Make sure you removed spaces from the application password
- Verify you're using an application password, not your account password
- For WordPress.com sites, ensure the site URL is correct

### "Failed to convert" Error
- Check that your Claude API key is valid
- Ensure you have API credits available
- Check your internet connection

### Publishing as Draft
By default, posts are created as **drafts**. If you want to publish immediately:
1. Open `blog_publisher.py`
2. Find the line: `'status': 'draft'`
3. Change it to: `'status': 'publish'`

## Customization

You can customize the conversion prompt by editing the `convert_to_blog()` function in `blog_publisher.py`. The prompt tells Claude how to format your blog post.

## Security Note

Your API keys and passwords are only stored in memory while the app is running. They are never saved to disk. You'll need to enter them each time you run the app.

For convenience, you could:
1. Use environment variables
2. Create a simple config file (add it to .gitignore!)

## Requirements

- Python 3.7+
- Internet connection
- Super Whisper (or any dictation tool)
- WordPress.com site or self-hosted WordPress with REST API enabled
- Claude API account
- WordPress application password

## License

MIT License - Feel free to modify and use as you wish!
