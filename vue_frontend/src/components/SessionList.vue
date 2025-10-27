<template>
  <div class="session-list">
    <div class="session-list-header">
      <h2>会话</h2>
      <div class="header-actions">
        <button
          class="toggle-btn"
          @click="$emit('toggle')"
          :title="isCollapsed ? '展开历史会话' : '收起历史会话'"
        >
          <chevron-up-icon v-if="!isCollapsed" class="icon" />
          <chevron-down-icon v-else class="icon" />
        </button>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="sessions.length === 0" class="empty-state">
      <div class="empty-icon">💬</div>
      <h3>还没有会话</h3>
      <p>开始创建第一个会话吧</p>
      <button class="primary" @click="showNewSessionDialog = true">
        新建会话
      </button>
    </div>

    <!-- 我想让这里这两个组件排列得当一点 -->
    <div class="session-content">
      <div class="newdialog">
        <button
          class="primary"
          @click="showNewSessionDialog = true"
          title="新建会话"
        >
          <plus-icon class="icon" />
        </button>
        <span>开启新对话</span>
      </div>
      <div v-if="!isCollapsed" class="session-items">
        <div
          v-for="session in sessions"
          :key="session"
          class="session-item"
          :class="{ active: session === currentSession }"
          @click="selectSession(session)"
        >
          <div class="session-name">{{ session }}</div>
          <button
            class="delete-btn"
            @click.stop="deleteSession(session)"
            title="删除会话"
          >
            <trash-icon class="icon" />
          </button>
        </div>
      </div>
    </div>

    <!-- 新建会话对话框 -->
    <div v-if="showNewSessionDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>新建会话</h3>
        <input
          type="text"
          v-model="newSessionName"
          placeholder="输入会话名称"
          @keyup.enter="createSession"
        />
        <div class="dialog-buttons">
          <button class="secondary" @click="showNewSessionDialog = false">
            取消
          </button>
          <button class="primary" @click="createSession">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import {
  PlusIcon,
  TrashIcon,
  ChevronUpIcon,
  ChevronDownIcon,
} from "vue-tabler-icons";

const props = defineProps({
  sessions: {
    type: Array,
    required: true,
  },
  currentSession: {
    type: String,
    required: true,
  },
  isCollapsed: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits(["select", "delete", "create", "toggle"]);

const showNewSessionDialog = ref(false);
const newSessionName = ref("");

const selectSession = (session) => {
  emits("select", session);
};

const deleteSession = (session) => {
  if (confirm(`确定要删除会话 "${session}" 吗？`)) {
    emits("delete", session);
  }
};

const createSession = () => {
  if (newSessionName.value.trim()) {
    emits("create", newSessionName.value.trim());
    newSessionName.value = "";
    showNewSessionDialog.value = false;
  }
};
</script>

<style scoped>
.session-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid var(--border-color);
}

.session-list.collapsed {
  width: 60px;
}

.session-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.session-list-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toggle-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: var(--radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.toggle-btn:hover {
  background-color: var(--bg-color);
}

.icon {
  width: 1.25rem;
  height: 1.25rem;
}

.session-items {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border-radius: var(--radius);
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.session-item:hover {
  background-color: var(--bg-color);
}

.session-item.active {
  background-color: var(--primary-color);
  color: white;
}

.delete-btn {
  background: none;
  padding: 0.25rem;
  opacity: 0.7;
  display: none;
}

.session-item:hover .delete-btn {
  display: block;
}

.session-item.active .delete-btn {
  color: white;
}

.delete-btn:hover {
  opacity: 1;
  background-color: rgba(0, 0, 0, 0.1);
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.dialog {
  background-color: var(--card-bg);
  border-radius: var(--radius);
  padding: 1.5rem;
  width: 100%;
  max-width: 400px;
}

.dialog h3 {
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.dialog input {
  width: 100%;
  margin-bottom: 1rem;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
  flex: 1;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary, #1f2937);
}

.empty-state p {
  margin: 0 0 1.5rem 0;
  color: var(--text-secondary, #6b7280);
}

/* 新建会话按钮区域 */
.new-session-section {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}
.newdialog {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.2s;
}
</style>
