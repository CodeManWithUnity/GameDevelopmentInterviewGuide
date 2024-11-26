# Addresable重复依赖下的自动打包

大蛇丸(旷野)

Posted on :2022-6-10 15:44

Pageviews :96

*This content expresses personal opinions and does not represent the views or opinions of NetEase Games. Intended for internal sharing and communication only. Do not disseminate in any form, or risk being held liable.

This article is only open to the following users, please protect content confidentiality

Viewing permission：UnityEngine、Unity技术培训、UnityTeam、UnrealEngine、互娱正式-公开、互娱实习生-公开、互娱外包-公开、运营中心-公开、张天羽、大蛇丸(旷野)、Kote(骆奕州)

**作者：引擎研究组 - 杨呈**；原KM地址：[Addresable重复依赖下的自动打包_KM (netease.com)](https://km.netease.com/article/413970)

### 问题描述

在打包时为了避免重复依赖，一般需要先运行以来分析，之后点击修复为Implicit
Assets 生成单独group，然后build 打包。因为Analyze Dependency会执行一个完整的构建过程。那么会产生大量的重复操作。
![image.png](./assets/624e5f2f9355994433faca90tii25AVu01.png)
如若产生重复依赖，生成bundle会多次打包asset到多个bundle中
![image.png](./assets/624e64416d46264dfbe25cd9AFcya0VC01.png)

依赖分析流程如下：
![image.png](./assets/624e60426d46265c5ebfed16IUJ1JaCo01.png)
build bundle流程如下：
![image.png](./assets/624e607fbab62f29b740d46cvLeb7fP401.png)

本文的目的是在尽量少的改动下，减少重复操作，提高打包效率.

### 解决步骤

新建一个BuildScriptDupPackedMode继承自BuildScriptPackedMode。
将build bundle的Tasks分为2个部分。
![image.png](./assets/624e61efbab62f14b09417f7FvWWaJsL01.png)
那么整个流程就变为
依赖分析-------构造ImplicitGroup--------Build Bundle
以下是task0和task1的截图:
![image.png](./assets/624e626a935599bf05c4f3c56PzYzSl901.png)

![image.png](./assets/624e6283bab62f57818ba146yv6io2Kb01.png)

### 结论及改进

![image.png](./assets/624e63036d4626134a7d38acWAw9cvh401.png)

![image.png](./assets/624e630bbab62f29b740d6c1Hs9F9cxp01.png)
因为去除了Impilict Asset，而使得bundle大小减少。

### Bug修复

bug1:
![image.png](./assets/624eee3acd05480a5c32491diy63cRRF01.png)
解决方案：取消Slim Write Results
![image.png](./assets/624eee45cd05489f9bfa667c6iN9dDYD01.png)