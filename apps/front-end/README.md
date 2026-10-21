# Provision only

Folder `front-end` with file package-lock.json is provision only to satisfy workflow
`ci-npm-audit`. Without this setup. the workflow will fail. See login in `ci-npm-audit`

This provision `front-end/*` will be removed as the first step in module `Angular` and
replaced with regulare Angular scaffold.  
