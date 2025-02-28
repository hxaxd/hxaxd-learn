# Tax

## 参考资料

* [知乎教程](https://zhuanlan.zhihu.com/p/456055339) - 够用 - 4

## KaTex

* 一个兼容 Tex 的数学公式渲染库, 主要是 js 实现, 因此 md 常内嵌 KaTex
* `$...$` 表示行内公式, `$$...$$` 表示行间公式
* 其支持一些原生的数学符号, 但更多的符号需要使用 `\...` 的形式来输入

### 语法

* 记不住, 建议让 AI 帮忙写

## 配置环境

* [Tex Live](http://mirror.ctan.org/systems/texlive/Images/)+VSCode (插件 latex workshop/latex language support + 配置一下)

## 文档类型

* 英文, 可以用 `book article和beamer`
* 中文, 可以用 `ctexbook ctexart和ctexbeamer`, 这些类型自带了对中文的支持
* 不同的文件类型, 编写的过程中也会有一定的差异, 如果直接修改文件类型的话, 甚至会报错
* 以下统一选用 `ctexart` 在编辑框第一行

```tax
\documentclass[12pt(字体大小), a4paper(纸张大小), oneside(单面打印)]{ctexart}

\begin{document}

这里是正文.

\end{document}
```

## 宏包

* 与数学公式与定理环境相关的宏包为 `amsmath amsthm amssymb`
* 用于插入图片的宏包为 `graphicx`
* `\usepackage{amsmath, amsthm, amssymb, graphicx}`
* 另外, 在加载宏包时还可以设置基本参数, 如使用超链接宏包 hyperref, 可以设置引用的颜色为黑色等
* `\usepackage[bookmarks=true, colorlinks, citecolor=blue, linkcolor=black]{hyperref}`

## 标题

* 标题可以用 `\title{}` 设置, 作者可以用 `\author` 设置, 日期可以用 `\date{}` 设置, 这些都需要放在导言区
* 为了在文档中显示标题信息, 需要使用 `\maketitle`

```tax
\documentclass[12pt, a4paper, oneside]{ctexart}
\usepackage{amsmath, amsthm, amssymb, graphicx}
\usepackage[bookmarks=true, colorlinks, citecolor=blue, linkcolor=black]{hyperref}

% 导言区

\title{我的第一个\LaTeX 文档}
\author{Dylaaan}
\date{\today}

\begin{document}

\maketitle

这里是正文.

\end{document}
```

## 正文

* 正文可以直接在 document 环境中书写, 没有必要加入空格来缩进, 因为文档默认会进行首行缩进
* 相邻的两行在编译时仍然会视为同一段
* 在 LaTeX 中, 另起一段的方式是使用一行相隔

```tax
我是第一段.

我是第二段.
```

* 这样编译出来就是两个段落 在正文部分, 多余的空格 回车等等都会被自动忽略, 这保证了全文排版不会突然多出一行或者多出一个空格
* 另外, 另起一页的方式 `\newpage`

在正文中, 还可以设置局部的特殊字体:

| 字体   | 命令          |
| ---- | ----------- |
| 直立   | `\textup{}` |
| 意大利  | `\textit{}` |
| 倾斜   | `\textsl{}` |
| 小型大写 | `\textsc{}` |
| 加宽加粗 | `\textbf{}` |

## 章节

* 对于 ctexart 文件类型, 章节可以用 `\section {}` 和 `\subsection {}` 命令来标记

```tax
...
\begin{document}

\maketitle

\section{一级标题}

\subsection{二级标题}

这里是正文.

\subsection{二级标题}

这里是正文.

\end{document}
```

## 目录

* 在有了章节的结构之后, 使用 `\tableofcontents` 命令就可以在指定位置生成目录
* 通常带有目录的文件需要编译两次, 因为需要先在目录中生成 `.toc` 文件, 再据此生成目录

```tax
...
\begin{document}

\maketitle

\tableofcontents

\section{一级标题}

\subsection{二级标题}

这里是正文.

\subsection{二级标题}

这里是正文.

\end{document}
```

## 图片

```tax
\begin{figure}[htbp]
    \centering
    \includegraphics[width=8cm]{图片.jpg}
    \caption{图片标题}
\end{figure}
```

* `[htbp]` 的作用是自动选择插入图片的最优位置
* `\centering` 设置让图片居中
* `[width=8cm]` 设置了图片的宽度为 8cm
* `\caption{}` 用于设置图片的标题

## 表格

* LaTeX 中表格的插入较为麻烦, 可以直接使用 `Create LaTeX tables online – TablesGenerator.com` 来生成

```tax
\begin{table}[htbp]
    \centering
    \caption{表格标题}
    \begin{tabular}{ccc}
        1 & 2 & 3 \\
        4 & 5 & 6 \\
        7 & 8 & 9
    \end{tabular}
\end{table}
```

## 列表

* LaTeX 中的列表环境包含无序列表 `itemize`
* 有序列表 `enumerate`
* 描述 `description`

```tax
\begin{enumerate}
    \item 这是第一点;
    \item 这是第二点;
    \item 这是第三点.
\end{enumerate}
```

* 另外, 也可以自定义 `\item` 的样式

```tax
\begin{enumerate}
    \item[(1)] 这是第一点;
    \item[(2)] 这是第二点;
    \item[(3)] 这是第三点.
\end{enumerate}
```

## 定理环境

* 导言区加入以下代码
    * `\newtheorem{theorem}{定理}[section]`
    * 其中 `{theorem}` 是环境的名称
    * {定理} 设置了该环境显示的名称是 "定理"
    * `[section]` 的作用是让 theorem 环境在每个 section 中单独编号

```tax
\begin{theorem}[定理名称]
    这里是定理的内容.
\end{theorem}
```

* 其中 `[定理名称]` 不是必须的

## 页面

* 最开始选择文件类型时, 我们设置的页面大小是 a4paper
* 除此之外, 我们也可以修改页面大小为 b5paper 等等
* 为了让每一页显示的内容更多一些, 我们可以使用 geometry 宏包

```tax
\usepackage{geometry}
\geometry{left=2.54cm, right=2.54cm, top=3.18cm, bottom=3.18cm}
```

* 另外, 为了设置行间距, 可以 `\linespread{1.5}`

## 页码

* 默认的页码编码方式是阿拉伯数字, 用户也可以自己设置为小写罗马数字 `\pagenumbering{roman}`
* 另外,aiph 表示小写字母
* Aiph 表示大写字母
* Roman 表示大写罗马数字
* arabic 表示默认的阿拉伯数字
* 如果要设置页码的话, 可以用如下代码来设置页码从 0 开始 `\setcounter{page}{0}`
