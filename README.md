# Hello Construction Group — design preview

A static review site so the client can pick a design direction by clicking through it.
Built from the Claude Design package in `design/` (spec, copy, tokens). The theme control in the
corner switches between Direction A · Orange, Direction A · Deep blue, and Direction B · Quiet.

This is scaffolding, not the production site. Every page carries `noindex` and `robots.txt`
disallows crawling. The production site is built in Wix Studio from `design/styles/tokens.css`.

`tools/gen.py` regenerates the pages from the copy and the templates it contains.
