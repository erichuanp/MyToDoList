<!-- eslint-disable -->
<template>
  <div>
    <h1>Home</h1>
    <TaskForm @taskCreated="fetchTasks" />
    <TaskList ref="taskList" />
  </div>
</template>

<script>
import TaskForm from '@/components/TaskForm.vue';
import TaskList from '@/components/TaskList.vue';

export default {
  name: 'HomeView',
  components: {
    TaskForm,
    TaskList
  },
  methods: {
    fetchTasks() {
      this.$refs.taskList.fetchTasks();
    }
  }
};
</script>
