# websearchcopy(others)

#### 介绍
通过websearchcopy(others)，您可以快速的将PR链接中的多个文档取到指定PC目录下。本工具适用于OpenHarmony非docs仓以及不符合如下目录结构要求的其他仓：docs下直接分为zh-cn和en路径（如下截图所示）。

![](figures/websearchcopynotlocal-6.png)

#### 操作步骤

1. 双击**dist**目录下的**websearchcopynotdocs.exe**，打开对应的操作界面。

2. 输入PR路径（以**.json**结尾），再回车。

   打开gitee网站，复制PR路径，在白色所示的输入区域右键即可粘贴所复制的路径。粘贴成功后，加上**.json**后缀，再回车即可。

   例如，对于编号为1079的PR，切换到**文件**页签，拷贝地址栏的路径https://gitee.com/openeuler/docs/pulls/1079/files，再加上**.json**后缀，即`https://gitee.com/openeuler/docs/pulls/1079/files.json`。

   ![](figures/websearchcopynotdocs-1.png)

   工具将提示读取到的路径，包括文档数量。

   ![](figures/websearchcopynotdocs-2.png)

3. 输入原文存在的根目录（即本地工作区），且以反斜杠（\）结尾，再回车。

   假设待翻译件所在的仓为D:\Euler\docs，则在白色所示的输入区域输入`D:\Euler\docs\`，再回车。

   在进行该操作之前，请确保根目录下的文档和上游仓库一致。
   
   ![](figures/websearchcopynotdocs-3.png)

4. 输入翻译目录，以反斜杠（\）结尾，再回车。

   假设想把待翻译文件复制到**D:\TR\1079 EulerSP2之前的修改**目录下，则输入 `D:\TR\1079 EulerSP2之前的修改\`，再回车。

   此时工具自动提示复制成功的文档数。如果有文档未能获取到，也会有相应的提示信息。

   ![](figures/websearchcopynotdocs-4.png)

   在对应的目录下，也可以看到工具取出的待翻译文件。例如：**D:\TR\1079 EulerSP2之前的修改**目录

   ![](figures/websearchcopynotdocs-5.png)

   待翻译文档已经复制到相应的路径，您可开始翻译。

#### Tips

1. 在白色输入区域，右键即可粘贴所复制的内容。

2. 通过上下方向键可以选择之前输入的命令。

#### FAQs

   Q：部分待翻译件未能获取到。

   A：可能原因：

    1. 分支不正确，本地工作区（workspace）无文档。
    2. 该文档在PR中是一个被删除的文档，即需要且已经从本地工作区（workspace）删除。

#### 代码贡献者

周宇
