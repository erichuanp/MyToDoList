<!-- eslint-disable -->
<template>
  <div>
    <h2>Create Task</h2>
    <form @submit.prevent="createTask">
      <div>
        <label for="title">Title:</label>
        <input type="text" v-model="title" id="title" required />
      </div>
      <div>
        <label for="description">Description:</label>
        <input type="text" v-model="description" id="description" />
      </div>
      <div>
        <label for="priority">Priority:</label>
        <select v-model="priority" id="priority" required>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      <div>
        <label for="due_date">Due Date:</label>
        <input type="date" v-model="due_date" id="due_date" required />
      </div>
      <button type="submit">Create Task</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TaskForm',
  data() {
    return {
      title: '',
      description: '',
      priority: 'Medium',
      due_date: ''
    };
  },
  methods: {
    async createTask() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.$router.push('/login');
        return;
      }

      try {
        await axios.post('http://127.0.0.1:5000/tasks', {
          title: this.title,
          description: this.description,
          priority: this.priority,
          due_date: this.due_date
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.$emit('taskCreated');
        // 清空表单
        this.title = '';
        this.description = '';
        this.priority = 'Medium';
        this.due_date = '';
      } catch (error) {
        console.error('Error creating task:', error);
      }
    }
  }
};
</script>
