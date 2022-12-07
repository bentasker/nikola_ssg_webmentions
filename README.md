# webmention Plugin

This is a deployment plugin for Nikola which will look for links in deployed posts/pages and attempt to send a [WebMention](https://indieweb.org/Webmention-developer#Protocol_Summary) to pages that have been linked to.

It can only *send* WebMentions, it cannot *receive* because doing so requires a dynamic stack. A service like [webmentions.io](https://webmentions.io) can be used for this.


### Usage

The plugin simply needs to be installed.

Once you've run `nikola build` a `nikola deploy` will lead to the plugin being triggered.


### Notes

* Nikola's `deploy` command does not trigger for pages/posts with a date older than the last recorded deployment, so if you are updating old pages, remember to add `Updated` to the meta-info and keep it current.
* There isn't a (good) way to record state, so failed webmentions can't be retried on a later run


### Usage within posts/pages

To trigger a webmention, you simply need to include a link out to the destination as you normally would.

However, a lot of WebMention supporting software allow the *type* of mention to be adjusted based on attributes in the markup. A common way is to use [h-entry](https://indieweb.org/h-entry) markup.
