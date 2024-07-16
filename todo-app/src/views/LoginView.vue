<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" id="username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '@/eventBus';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: this.username,
          password: this.password
        });
        localStorage.setItem('token', response.data.access_token);
        this.message = 'Login successful!';
        EventBus.emit('user-logged-in');
        this.$router.push('/');
      } catch (error) {
        console.error('Error:', error);
        if (error.response) {
          console.error('Error response data:', error.response.data);
          this.message = 'Error logging in: ' + error.response.data.message;
        } else {
          this.message = 'Unknown error';
        }
      }
    }
  }
};
</script>
