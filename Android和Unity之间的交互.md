# **Android和Unity之间的交互**

>    最近再研究项目APP的性能，特别是涉及到unity可视化相关的，所以调研了下Android和Unity之间的交互方式。Unity，是可以用来开发三维电子游戏、三维动画、建筑可视化模型等交互类内容的多平台开发工具，具有很强大的跨平台性，支持Android、iOS、MacOS、Windows phone、PC ...

  最近再研究项目APP的性能，特别是涉及到unity可视化相关的，所以调研了下Android和Unity之间的交互方式。Unity，是可以用来开发三维电子游戏、三维动画、建筑可视化模型等交互类内容的多平台开发工具，具有很强大的跨平台性，支持Android、iOS、MacOS、Windows phone、PC 等多个平台的版本。关于Unity的详细介绍，可以查看[官方网站](https://unity3d.com/cn)。

Android和Unity之间的交互方式主要有两种：

- 将Android编写的项目作为插件放到Unity中；
- 将Unity项目编译后放入Android项目中，让Android代码来调用Unity封装的API；

感觉这两句有点废话，但……我还是要说^-^。第一种方式主要是以Unity为核心的项目实现方式，而第二种自然就是以Android为核心了。我们的项目采用的是第二种实现方式，所以这里只介绍第二种交互方式。

   创建好Android项目后，我们首先要导入Unity提供的classes.jar包（Applications\Unity（右键选择显示包内容）PlaybackEngines\AndroidPlayer\Variations\Release\Classes），放在app/libs目录下。classes.jar包，主要为Android提供了这几个类文件：UnityPlayerActivity.class，UnityPlayerNativeActivity.class，UnityPlayerProxyActivity.class以及UnityPlayer.class。其中，UnityPlayerNativeActivity.class是继承于UnityPlayerActivity.class，并且被标记为弃用，推荐使用UnityPlayerActivity.class。而UnityPlayerProxyActivity.class继承于Activity.class，但是该类中只有onCreate函数，并且最后还是通过startActivity()去打开UnityPlayerActivity.class。因此，还是推荐使用UnityPlayerActivity.class。


![img](http://nos.netease.com/knowledge/fc12fa05-ebc4-4a94-8c9e-f3f6065a7669?imageView&thumbnail=980x0)

UnityPlayerNativeActivity.class源码

   接着创建业务相关涉及到Unity的Activity，并继承UnityPlayerActivity.class。同时，根据官方提供的demo，我们还需要在AndroidManifest.xml文件中为该Activity添加<meta-data>信息：

![img](http://nos.netease.com/knowledge/384d11a9-4099-460b-835a-26f0d6f020cc?imageView&thumbnail=980x0)

meta-data

   然后，编译Unity源码并将编译后的文件导入到Android项目中，存放在/src/main/assets目录下。这样，我们就可以调用Unity提供的API，将消息传递给Unity模型实现相关的操作。

![img](http://nos.netease.com/knowledge/7b89be94-bca3-44de-8c19-282b01ca67b7)

unity编译后的文件

   为了实现消息传递，Android需要用到Unity提供的另外一个类：UnityPlayer.class。在这个类中，有一个静态方法：UnitySendMessage(String var0，String var1，String var2)。通过调用这个静态方法可以实现将消息传递到Unity，Unity接着做出相应操作。其中，第一个参数var0是指接收消息的类对象，第二个参数var1是指接收消息的方法，最后一个参数var2是指需要传递的消息。

![img](http://nos.netease.com/knowledge/483fff8d-9036-4fdb-8580-ae108a948758)