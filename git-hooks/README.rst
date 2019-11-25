Apply git hooks in development workflow
--------
Bring the team on the same hooks:

The global hooks store in a normal foder in the repo called git-hooks. If you’re using Git version 2.9 or greater, you can simply run the below command to change the hooks folder to git-hooks instead of .git/hooks.

      * git config core.hooksPath git-hooks

You can also make above command to execute automatically by placing it in a setup file i.e Makefile, pom.xml , package.json etc. Husky is one of the best options for installing git hooks in node project. However, if you are using an earlier version of git, you need to create a symbolic link by executing -

      * ln -s -f ../../git-hooks/pre-recieve .git/hooks/pre-receive
