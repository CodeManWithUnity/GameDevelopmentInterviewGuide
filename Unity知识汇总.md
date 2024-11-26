## 代码

### **控制频繁调用GC**

1. 控制高频率的内存分配。
2. 控制大块的内存申请，可能会造成内存的碎片化，如果需要申请，尽可能在刚启动时申请。
3. 控制容易导致 GC alloc的函数调用
4. [Mono]控制字符串拼接/ToString/ToArray
5. [Mono]Boxing(拆装箱操作)/委托/匿名函数
6. [Mono]Tag/Name/Mesh.Vertices
7. [Lua]Vector等非基础类型的参数传递

### **脚本注意事项：**

1. 避免Update LateUpdate等函数频繁的gc alloc
2. 避免在Update()内GetComponent()
3. 避免在Update()内FindObjectsOfType()
4. 避免在Update()里赋值给栈上的数组，会触发堆内存的反复分配
5. 避免在Update()内使用GameObject.Tag和GameObject.Name，用CompareTag来进行比较
6. 避免频繁调用alloc-accessors(如Mesh.vertices/normals/uvs、SkinedMeshRenderer.bones)，如果一定需要，也尽量缓存起来
7. 避免频繁调用int.tostring()及其它类型的衍生
8. 避免OnGUI的调用
9. 频繁创建和更新的字符串尽量缓存，比如CD时间等
10. 尽量避免dict.Values操作，直接遍历取Value即可
11. 用RayCastNoAlloc替换RayCastAll/用yield return null代替yield return 0
12. 尽量少用lambda,创建带upvalue的lambda对象会产生124B的GC，禁止在Update或for循环中使用
13. 委托有+=务必要有-=，另外禁止有太长的委托调用链
14. 禁止通过new的方式实例化MonoBehavior的派生类，否则无法得到引擎的有效管理
15. 禁止在Update/FixedUpdate/LateUpdate/OnGUI等频繁调用的逻辑中使用携程
16. 尽量少用Resources.Load加载资源
17. 禁止使用Invoke("func",1)来实现延时调用
18. 尽可能避免使用携程。Unity的协程是使用迭代器实现的会分配堆内存
19. 使用网格导航时，尽可能避免使用Obstacle模拟动态障碍物，否则对CPU的冲击比较大，如有此类需求建议使用碰撞体替代
20. 禁止在MonoBehavior的派生类中存在被引擎高频调用的空方法，如Update里面没有方法内容就应该删掉
21. 禁止在MonoBehavior的派生类中存在Awake/Start/OnEnable/OnDestroy等空方法
22. 必须使用CompareTag接口比较GameObject的Tag。看到Unity源码，在使用CompareTag对比Tag时，是对比int类型。
23. 尽可能减少UnityEngine.Onject null 比较
24. 尽量避免使用Relection(反射)
25. 尽量避免使用可变参数(param object[] args),避免装箱拆箱操作il2cpp中会重载多个方法，导致生成的文件过大）
26. 禁止没有计算需求的变量赋值或者计算
27. 简单条件判断尽量使用三目运算符：b?x:y
28. 注意List等容器常用接口的复杂度，尽量从尾部移除/批量移除（RemoveRange）等
29. 在频繁查询数据列表时，建议使用HashSet/HashTable 查找时间复杂度低的数据结构，避免使用List
30. 使用可变长容器时，建议根据预估容器进行初始化
31. 循环中寻找到适合条件的后应该适时地使用break跳出循环
32. 尽可能将一些内存占用低但为数众多/功能简单的小对象定义为Struct（结构体）而非Class
33. 尽可能减少函数调用栈。如使用x= (x>0?x:-x)代替x= Mathf.Abs(x)
34. **Unity避免使用SetActive**

**开销问题：**

1. C#层到Native层的调用速度比C#层慢
2. 会导致Canvas抛弃其VBO（顶点缓存对象）数据。重启Canvas会使Vanvas（包含所有的子Canvas）强制进行rebuild和rebatch进程。如果比较频繁，增加CPU的使用会造成帧率卡顿
3. UI元素的网格定点数改变会造成堆内存分配，触发GC导致耗时（不过对UI元素进行位置移动不会造成堆内存分配）



**优化：**

1. C#层设置标识，判断是否隐藏
2. 将要频繁变化的UI元素与不频繁变动的UI元素分开（动静分离）
3. 通过将UI元素的坐标移动到Canvas的范围之外的方法来显示与隐藏，避免SetActive的耗时以及SendWillRenderCanvases的耗时。
4. 要更改单个UI的显隐可以通过GetComponent<CanvasRenderer>().SetAlpha(0);来实现，并且勾上CanvasRender.cullTransparentMesh使其不渲染网格，但是这样做还是会触发update等函数并且会触发点击事件
5. 要更改父物体的显隐可以通过添加CanvasGroup组件设置透明度的方式来进行显示与隐藏。



**UI优化：**

1. 制作图集
2. 动静分离，子Canvas(但是会导致Canvas在子Canvas在子Canvas那边打断Batch，最好是不要使用多个Canvas)
3. 相同图集和材质的放在一起，减少DrawCall
4. 对Canvas下的所有CanvasRenderer深度优先遍历，生成一个队列如果在里面镶嵌Canvas，为空时不受影响，如果有任意元素会打断Batch
5. 计算Depth： 每个Instrunction和前面的Instrunction判断是否相交，主要是判断相交同时 材质/贴图信息不一样的Instruction，如果有depth+1两个CanvasRenderer相交，同时材质/贴图不同，就要保序相交是指网格相交，不是RectTransform相交（Text是Overflow）
6. Depth ->Material ID->Texture ID 渲染顺序（Depth表示这个元素能在第几步绘制）
7. 不能设置图集的 要设置成2的幂次方
8. 减少Mask的使用，如果需要可以优先考虑使用Rect Mask 2D（绘制完Mask所有节点之后 需要把Stencil复原，增加了一次DrawCall）
9. 降低层级，减少深度遍历生成的消耗
10. 非必要 关闭 MipMap Read/Write
11. 纹理格式：推荐使用ASTC和ETC2 
    1. ETC2：对应的纹理分辨率为4的倍数，在对应的纹理开启MipMap时更具有严格的要求其分辨率为2的幂次方。否则，该纹理将被解析成未压缩格式



1. 使用不同材质的实例化物体（instance）将会导致批处理失败。
2. 在不移动不缩放的物体可以使用静态批处理，使用静态批处理不要再移动，不然开销的内存很大
3. 禁止非图集贴图资源不合理的留白，会影响UGUI运行时自动和批
4. 禁止使用修改Alpha值的方式来隐藏界面
5. 尽可能降低图集留白，提高贴图利用率
6. 尽可能将图集中大的图片改为地图加载
7. 建议同一Canvas中使用到的图集数量控制在三个以内
8. Canvas下的UI节点过多导致算法（贪心策略）耗时过长。主要消耗在Rebatch和Rebuild如果节点都是动态切不怎么变动，问题不大，Rebatch之后结果会进行缓存复用知道下一次节点变化；如果节点经常变动，会引起Canvas的Rebeach和Rebuild，CPU耗时就会响应增加。
9. 在使用Layout时,不要去嵌套多的物体,这样在修改相关的一个Item时,所有的物体都会遍历,造成了大量的大量的计算浪费.
10. 在使用完Layout排序之后禁用掉。

## **资源规范**

### **音频**

1. 如果在音效不损失的情况下，可减少音频的Quality
2. 如果不需要的双声道，可以关掉（开启Force To Mono）
3. 较长的音乐，要设置成Streaming，不然整个资源会一次性加入内存中
   1. Decompress On Load：音频文件以压缩形式存放在磁盘中，解压后直接放在磁盘中，适合小音频。
   2. Streaming：音频放在磁盘中，加载时循环一下操作“从磁盘中读取一部分，解压到内存中，播放，卸载”存在占用较小，但是CPU消耗比较大
   3. Compressed In Memory： 音频文件已压缩形式放在内存中，加载时直接解压到内存中。CPU开销更大，加载速度和内存上更占优势，不适合大音频。



### **模型**

1. 重复的FBX的模型文件，可以把重复的网格丢弃。不然会重新加载到内存中
2. 控制骨骼的数量和复杂程度
3. Optimize Game Objects 勾选上：只有mesh，不会在出现骨骼，依然可以播放动画，如果是需要单独一个骨骼控制，可以在控制面版上 单独排除一个骨骼

### **Scene**

1. 搭建在Scene中的资源。不会被释放，除非切换场景。要尽可能把场景中的资源少放

### **Prefab**

1. 每一个Prefab不要过大，如果过大，尽可能去拆分，可以避免大内存的开销
2. 同一个Prefab，尽可能使用一张图集，如果要使用多张图集/图片，控制在3个图集以内

### **小心插件**

1. 可能插件有多个版本的Json 造成的资源的浪费

## **AssetBundle**

1. 如果开发版本不会发生变化，可以去除掉TypeTree,这个是版本开发兼容性
2. 大小尽量控制在1~2M，最大不要超过10M

## **IO** 

1. 必须是异步的 不然会造成卡顿