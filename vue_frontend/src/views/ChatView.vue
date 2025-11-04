<template>
  <div class="chat-container">
    <!-- 原纯文本显示：<div class="message-content">{{ message.content }}</div> -->
    <!-- 新Markdown显示：引用自定义组件 -->
    <MarkdownRenderer :content="message.content" />
  </div>
</template>

<script setup>
// 导入Markdown渲染组件
import MarkdownRenderer from '@/components/MarkdownRenderer.vue';
// 其他原有逻辑（如对话数据请求、用户输入处理）保持不变
</script>
