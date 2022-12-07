# webmention Plugin

This is a deployment plugin for Nikola which will look for links in deployed posts/pages and attempt to send a [WebMention](https://indieweb.org/Webmention-developer#Protocol_Summary) to pages that have been linked to.

At time of writing, it only supports looking for WebMention endpoints in HTTP response headers (HTML meta-tag support coming soon)


### Usage

The plugin simply needs to be installed.

Once you've run `nikola build` a `nikola deploy` will lead to the plugin being triggered.


### Notes

* Nikola's `deploy` command does not trigger for pages/posts with a date older than the last recorded deployment, so if you are updating old pages, remember to add `Updated` to the meta-info and keep it current.
* There isn't a (good) way to record state, so failed webmentions can't be retried on a later run
