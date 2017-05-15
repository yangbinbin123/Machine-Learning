************************************************************************************************************************
*                                                     Git 使用心得                                                     *
*                                                                                                                      *
*                                                      Author:Bean                                                     *
*                                                                                                                      *
************************************************************************************************************************

如何提交文件到目录repository：
$ git clone https://github.com/yangbinbin123/Assembly-Language.git
$ cd Assembly-Language
$ git commit -m "Assembly-Laguage"
$ git push origin master (master是默认的分支)
或者可以用这个命令来提交到分支上
$ git push -u origin master:master

创建新的分支，更新目录repository

$ git checkout master 切换分支
$ git branch update 创建update分支
$ git checkout -b update 切换并创建新的分支update
$ git branch 查看当前分支
$ git branch -d update 删除update分支
$ git status 查看更新的情况
$ git add -A 把新增修改的文件到缓存列表
把分支合并到master分支上

$ git checkout master
$ git merge update



