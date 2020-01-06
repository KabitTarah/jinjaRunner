# Jinja Runner

## Description

This is a very simple runner for Jinja templating. Run in python, it supports multiple "sites" and very basic (not super secure) secrets keeping.

## Running Jinja Runner

Basic usage out of the box: `python jinja_runner.py sitecode template.txt` changes template.txt into:

```
This is just a regular text file...
but it has some Jinja2 mixed in.

For example, each site is different and has a name, e.g. Site Name

I might want to use an IP address like:
    10.10.10.0/24

I might also want to use the next /24 following this one:
    10.10.11.0/24

Maybe that site name looks better in all caps: SITE NAME

... this is pretty basic Jinja with a pretty basic runner to show how things work.
but it also includes some secrets!!

If you don't KNOW the {{ secrets.SecretVar }}, it'll just put the Jinja code back in (this is 1-for-1 -- don't do math with this simple example).

oh... and don't name a site "secrets" - or anything else that overlaps your secrets.json! You'll get confused even if Python won't.
```

Running without arguments, or with `-h`, `--help`:

```
jinja_runner.py requires two arguments:
   (1) site-code (e.g. xmpl1)
   (2) template file
```

To include secrets, create a directory and file in `~/.secrets/secrets.json` (using ./secrets.json as a template) then run as before:

```
This is just a regular text file...
but it has some Jinja2 mixed in.

For example, each site is different and has a name, e.g. Site Name

I might want to use an IP address like:
    10.10.10.0/24

I might also want to use the next /24 following this one:
    10.10.11.0/24

Maybe that site name looks better in all caps: SITE NAME

... this is pretty basic Jinja with a pretty basic runner to show how things work.
but it also includes some secrets!!

If you don't KNOW the ===SECRET INFO===, it'll just put the Jinja code back in (this is 1-for-1 -- don't do math with this simple example).

oh... and don't name a site "secrets" - or anything else that overlaps your secrets.json! You'll get confused even if Python won't.
```
