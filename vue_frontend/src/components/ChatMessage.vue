<template>
  <div class="message" :class="{ 'user-message': isUser }">
    <div class="message-avatar">
      <div :class="isUser ? 'user-avatar' : 'bot-avatar'">
        {{ isUser ? '用户' : 'AI' }}
      </div>
    </div>
    <div class="message-content">
      <div class="message-text">
      <div v-if="isUser" class="plain-text">{{content }}</div>
      <div
          v-else 
          class="markdown-content" 
          v-html="renderedMarkdown"
        ></div>
      </div>
      <div class="message-time">
        {{ formatTime(timestamp) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps ,computed} from 'vue';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

const props = defineProps({
  isUser: {
    type: Boolean,
    required: true
  },
  content: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    required: true
  }
});

//Markdown配置选项
marked.setOptions ({
    gfm:true, //启用 GitHub flavored markdown
    break:true, //将换行符转化为<br>
    sanitize:false //不进行HTML转义
  }
);

//计算属性：将markdown转换为安全的html
const renderedMarkdown = computed(()=>{
  if(props.isUser) return props.content;
  try{
    const rawHtml = marked(props.content);
    return DOMPurify.sanitize(rawHtml);
  }catch(error){
    console.error('markdown渲染错误',error);
    return props.content;
  }
})

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString();
};
</script>

<style scoped>
.message {
  display: flex;
  margin-bottom: 1rem;
  max-width: 80%;
}

.message.user-message {
  margin-left: auto;
  flex-direction: row-reverse;
}

.message-avatar {
  margin-right: 0.5rem;
}

.user-message .message-avatar {
  margin-right: 0;
  margin-left: 0.5rem;
}

.user-avatar, .bot-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 0.875rem;
}

.user-avatar {
  background-color: var(--primary-color);
  color: white;
}

.bot-avatar {
  background-color: var(--secondary-color);
  color: white;
}

.message-content {
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  position: relative;
}

.message:not(.user-message) .message-content {
  background-color: var(--bot-message);
}

.user-message .message-content {
  background-color: var(--user-message);
}

.message-text {
  margin-bottom: 0.25rem;
  line-height: 1.5;
}

.message-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: right;
}
</style>

<style>
/* Markdown 内容样式 */
.markdown-content {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-content h1 {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-content h2 {
  font-size: 1.25em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-content h3 {
  font-size: 1.1em;
}

.markdown-content ul,
.markdown-content ol {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.markdown-content li {
  margin-bottom: 0.25em;
}

.markdown-content li > ul,
.markdown-content li > ol {
  margin-top: 0.25em;
  margin-bottom: 0;
}

.markdown-content code {
  background-color: rgba(175, 184, 193, 0.2);
  border-radius: 3px;
  padding: 0.2em 0.4em;
  font-size: 0.9em;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}

.markdown-content pre {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 1em;
  overflow: auto;
  margin: 1em 0;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.9em;
  line-height: 1.45;
}

.markdown-content pre code {
  background: none;
  padding: 0;
  font-size: 1em;
}

.markdown-content blockquote {
  border-left: 4px solid #dfe2e5;
  padding-left: 1em;
  margin: 1em 0;
  color: #6a737d;
}

.markdown-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.markdown-content table th,
.markdown-content table td {
  border: 1px solid #dfe2e5;
  padding: 0.5em 1em;
  text-align: left;
}

.markdown-content table th {
  background-color: #f6f8fa;
  font-weight: 600;
}

.markdown-content a {
  color: #0366d6;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

.markdown-content hr {
  border: none;
  border-top: 1px solid #eaecef;
  margin: 1.5em 0;
}

.plain-text {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>