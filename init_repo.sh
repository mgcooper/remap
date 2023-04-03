
# use conda list to create a requirements.txt file
conda list --export > requirements.txt

# init a new git repo in the current directory and call it remap
git init

# use gh cli to create a new repo on github
gh repo create remap --public -y

# set the remote url to the new repo
git remote add origin https://github.com/mgcooper/remap

# push to it
git push -u origin HEAD
