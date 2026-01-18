#!/usr/bin/env python3
"""
Blog Publisher - Dictate thoughts and publish to WordPress
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import base64
import json
from anthropic import Anthropic
import os
from datetime import datetime

class BlogPublisher:
    def __init__(self, root):
        self.root = root
        self.root.title("Blog Publisher - Super Whisper to WordPress")
        self.root.geometry("1000x800")
        
        # Configuration
        self.wordpress_url = "https://thecodeshell.wordpress.com"
        self.wp_username = ""
        self.wp_app_password = ""
        self.anthropic_api_key = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Blog Publisher", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # API Key
        ttk.Label(config_frame, text="Claude API Key:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_key_entry = ttk.Entry(config_frame, width=40, show="*")
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # WordPress Username
        ttk.Label(config_frame, text="WordPress Username:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.wp_user_entry = ttk.Entry(config_frame, width=40)
        self.wp_user_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # WordPress App Password
        ttk.Label(config_frame, text="WordPress App Password:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.wp_pass_entry = ttk.Entry(config_frame, width=40, show="*")
        self.wp_pass_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Your Dictated Thoughts (paste from Super Whisper)", padding="10")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=10, wrap=tk.WORD)
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(0, 10))
        
        self.convert_btn = ttk.Button(button_frame, text="Convert to Blog Post", command=self.convert_to_blog)
        self.convert_btn.grid(row=0, column=0, padx=5)
        
        self.publish_btn = ttk.Button(button_frame, text="Publish to WordPress", command=self.publish_to_wordpress, state=tk.DISABLED)
        self.publish_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Output Section
        output_frame = ttk.LabelFrame(main_frame, text="Generated Blog Post (Preview)", padding="10")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def convert_to_blog(self):
        """Convert dictated thoughts to a blog post using Claude"""
        raw_text = self.input_text.get("1.0", tk.END).strip()
        
        if not raw_text:
            messagebox.showwarning("Empty Input", "Please paste your dictated thoughts first.")
            return
        
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Missing API Key", "Please enter your Claude API key.")
            return
        
        self.status_var.set("Converting to blog post...")
        self.convert_btn.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            client = Anthropic(api_key=api_key)
            
            prompt = f"""You are a professional blog editor. I've dictated my thoughts for a blog post, and I need you to convert them into a well-structured, engaging blog post.

Here are my dictated thoughts:

{raw_text}

Please:
1. Create an engaging title (just the title, no "Title:" prefix)
2. Structure the content with clear paragraphs
3. Fix any grammar or coherence issues from dictation
4. Maintain my voice and ideas
5. Add appropriate subheadings if needed
6. Make it ready to publish

Format the output as:
[TITLE]
Your Title Here

[CONTENT]
The blog post content here...

Keep it natural and conversational, as if I wrote it myself."""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            blog_post = message.content[0].text
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", blog_post)
            
            self.publish_btn.config(state=tk.NORMAL)
            self.status_var.set("Blog post generated! Review and publish when ready.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert: {str(e)}")
            self.status_var.set("Error during conversion")
        finally:
            self.convert_btn.config(state=tk.NORMAL)
    
    def publish_to_wordpress(self):
        """Publish the generated blog post to WordPress"""
        blog_content = self.output_text.get("1.0", tk.END).strip()
        
        if not blog_content:
            messagebox.showwarning("Empty Post", "No blog post to publish.")
            return
        
        username = self.wp_user_entry.get().strip()
        password = self.wp_pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Missing Credentials", "Please enter WordPress username and app password.")
            return
        
        # Parse title and content
        try:
            parts = blog_content.split("[CONTENT]")
            title_part = parts[0].replace("[TITLE]", "").strip()
            content = parts[1].strip() if len(parts) > 1 else blog_content
            
            # Extract actual title (first non-empty line)
            title = title_part.split('\n')[0].strip()
            
        except:
            # Fallback: use first line as title
            lines = blog_content.split('\n')
            title = lines[0].strip()
            content = '\n'.join(lines[1:]).strip()
        
        self.status_var.set("Publishing to WordPress...")
        self.publish_btn.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # WordPress REST API endpoint
            url = f"{self.wordpress_url}/wp-json/wp/v2/posts"
            
            # Credentials
            credentials = f"{username}:{password}"
            token = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {token}',
                'Content-Type': 'application/json'
            }
            
            # Post data
            post_data = {
                'title': title,
                'content': content,
                'status': 'draft'  # Change to 'publish' for immediate publishing
            }
            
            response = requests.post(url, headers=headers, json=post_data)
            
            if response.status_code in [200, 201]:
                post_info = response.json()
                post_url = post_info.get('link', '')
                messagebox.showinfo("Success", f"Blog post published as draft!\n\nURL: {post_url}")
                self.status_var.set(f"Published successfully as draft!")
            else:
                messagebox.showerror("Error", f"Failed to publish: {response.status_code}\n{response.text}")
                self.status_var.set("Publishing failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to publish: {str(e)}")
            self.status_var.set("Error during publishing")
        finally:
            self.publish_btn.config(state=tk.NORMAL)
    
    def clear_all(self):
        """Clear all text fields"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.publish_btn.config(state=tk.DISABLED)
        self.status_var.set("Cleared. Ready for new content.")

def main():
    root = tk.Tk()
    app = BlogPublisher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
