---
title: JavaScript前端
date: 2023-05-03 22:36:08
categories:
    - 前端
tags:
    - JavaScript
---

这篇文章主要是记录我前端学习的内容。

<!--more-->

## 前端环境搭建

### Node.js（运行JavaScript）

想要编写前端项目需要安装{% post_link Node.js %}来运行JavaScript。

### WebStorm（前端最好用的编辑器）

WebStorm的安装破解方法在我的博客{% post_link JetBrains %}里。

## Vite 配置方法

### base

```js
export default defineConfig(({mode}) => {
    return {
        base: './',
        plugins: [vue()],
    }
})
```

### alias

```js
export default defineConfig(({mode}) => {
    return {
        plugins: [vue()],
        resolve: {
            alias: {
                '@': resolve(__dirname, 'src')
            }
        }
    }
})
```

### 生产环境移除console

```js
export default defineConfig(({mode}) => {
    return {
        plugins: [vue()],
        build: {
            minify: "terser",
            terserOptions: {
                compress: {
                    // 生产环境移除console
                    drop_console: true,
                    drop_debugger: true
                }
            }
        }
    }
})
```

### 配置proxy代理

```js
export default defineConfig(({mode}) => {
    return {
        plugins: [vue()],
        server: {
            proxy: {
                '/api': {
                    target: loadEnv(mode, process.cwd()).VITE_BASE_API,
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, ''),
                },
            }
        },
    }
})

```

### env环境变量配置

创建`.env.development`和`.env.production`两个文件。

在文件中用VITE_XXX作为变量。

## TypeScript

### 引入js组件

当使用ts时引入js组件时，可以同时引入@types/xxx达到使用ts的目的。

## highlight

使用最新的marked时无法显示highlight高亮，需要搭配marked-highlight使用highlight

这是[marked-highlight的GitHub链接](https://github.com/markedjs/marked-highlight)在README中有使用样例，可以复制使用。

## 前端网站

### 前端工具文档

[Vue官方文档](https://cn.vuejs.org/)，[Vite官方文档](https://cn.vitejs.dev/)

[Vue Router官方文档](https://router.vuejs.org/zh/)，[Pinia官方文档](https://pinia.vuejs.org/zh/)

[Element Plus官方文档](https://element-plus.gitee.io/zh-CN/)

[Axios官方文档](https://www.axios-http.cn/)，[Fetch文档](https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch)

[ECharts文档](https://echarts.apache.org/handbook/zh/get-started/)

[marked.js文档](http://www.dagoogle.cn/n/745.html)，[highlight.js下载地址](https://highlightjs.org/)，[highlight.js预览效果](https://highlightjs.org/static/demo/)

### 图标网站

[阿里巴巴矢量图标](https://www.iconfont.cn/)，[标志客网址](https://www.logomaker.com.cn/)，[标小智网址](https://www.logosc.cn/logo/favicon)

### Api接口网站

[聚合数据网址](https://www.juhe.cn/)
