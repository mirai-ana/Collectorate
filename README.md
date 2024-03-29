# DBMS PROJECT #

**Warning: This repository is unfit for production usage due to several security flaws.**

This was a project I did in 2020 for my DBMS course at my university.

## Dependencies ##
- Flask
- Jinja
- Python3

## What it does? ##

It is a basic web form application that stores the responses to the database. No server-side input checks whatsoever. It is a security disaster and that's deliberate :) It has some hard-coded SQL to create and initialize the database because I could not get reading from file to work back in the days.

## What is this repo? ##

It's public to serve as an example of **how not to code Flask applications**. Please. Don't copy this for production. StackOverflow should have better ones :)


## Vulnerabilites known ##
- **Remote Code Execution**: The `debug` value of the app is set to `True` which allows for RCE on Flask apps as Flask opens a shell on the error page.
- **Any unchecked input vulnerability**: SQL Injection, Cross-site scripting, basically any user input point can be exploited.
- **Default admin password exposed**: I realized this after I committed the code here. No need to bother going through the code the default username is `el admino` and password is `Bruh`.

## I want to deploy it anyway ##

Directory structure required
```
|-app.py
|-templates
  |-agriculture.html
  |-civil.html
  |-cost.html
  |-dataview.html
  |-energy.html
  |-error.html
  |-home.html
  |-login.html
  |-signup.html
  |-update.html
  |-viewdata.html
  |-voterid.html
```
## To do ##
- Add version numbers
- Open security issues because why not :)
