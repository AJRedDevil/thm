# README #

This README would normally document whatever steps are necessary to get your application up and running.

### To Create A Superuser ###
i) Signup first with http://url/signup
ii) Manually update the is_superuser field for the user in the database [ this is done on purpose ]

### For the API documentation, only superusers are allowed ###
* API docs are available at http://ur/api/v1/docs/ and requires a token to be accessible, ONLY ACCESSIBLE by Superusers
* To obtain the otken
** Do a post req with user,pass to http://url/api/v1/api-auth/
Use that token on the api_key section in the API docs

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
** Create Database for Development

```
gaumire=# create user thm with password 'thm';
CREATE ROLE
gaumire=# create database thm owner thm;
CREATE DATABASE
```

* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact