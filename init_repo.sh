
# init a new git repo in the current directory and call it remap
git init

# use gh cli to create a new repo on github
gh repo create remap --public -y

# set the remote url to the new repo
git remote add origin git@github.com:username/new_repo

# use gh cli to create a new remote and push to it
git remote add origin 
git push -u origin main


