---
layout: post
title: ArrayList 源码刨析
date: 2018-09-14 00:00:00
categories: 编程语言
tags: Java
---

ArrayList是List的是一个实现，是一个顺序容器，添加的时候如果容器不够，会自动扩容，值得注意的是ArrayList是不同不得，如果想同步可以自己手动实现，也可以使用Vector。

ArrayList底层使用的是数组。在源码中可以看到``transient Object[] elementData;``

被transient修饰的变量会被禁止序列化

### 源码追踪

#### set()

简明直意，将element 放到index位置set(),这里需要注意的一点是``elementData[index] = element;``赋值的是引用,将element的引用给了elemntData[index]

```java

public E set(int index, E element) {
    // 检查索引
    rangeCheck(index);
    
    E oldValue = elementData(index);
    elementData[index] = element;   // 这里赋值的是引用
    return oldValue;
}
```

#### get()

获取index位置的元素

```java
public E get(int index) {
        rangeCheck(index);

        return (E)elementData(index);
    }
```

#### add()

添加的方法有两种，``add(E e)``和``add(int index, E element)``，两个方法底层都是往数组中添加元素
```java
public boolean add(E e) {
    ensureCapacityInternal(size + 1);
    elementData[size++] = e;
    return true;
}

public void add(int index, E element) {
    rangeCheckForAdd(index);

    ensureCapacityInternal(size + 1);  // Increments modCount!!
    System.arraycopy(elementData, index, elementData, index + 1,
                        size - index);
    elementData[index] = element;
    size++;
}
```

在添加时如果空间不够会使用调用进行扩容， ``grow(minCapacity)``

```java
private void grow(int minCapacity) {
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + (oldCapacity >> 1); // 拓展空间为原来的1.5倍
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    // 
    elementData = Arrays.copyOf(elementData, newCapacity); // 拓展空间完成复制
}

```

#### remove()

```java
public E remove(int index) {
    rangeCheck(index);

    modCount++;
    E oldValue = elementData(index);

    int numMoved = size - index - 1;
    if (numMoved > 0)
        System.arraycopy(elementData, index+1, elementData, index,
                            numMoved);
    elementData[--size] = null; // 让GC 进行垃圾回收

    return oldValue;
}  
```



