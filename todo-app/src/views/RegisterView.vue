<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div>
    <h1>Register</h1>
    <form @submit.prevent="register">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" id="username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required>
      </div>
      <button type="submit">Register</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '@/eventBus';

export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async register() {
      try {
        await axios.post('http://127.0.0.1:5000/register', {
          username: this.username,
          password: this.password
        });
        this.message = 'Registration successful!';
        EventBus.emit('user-logged-in');
        this.$router.push('/login');
      } catch (error) {
        console.error('Error:', error);
        if (error.response) {
          console.error('Error response data:', error.response.data);
          this.message = 'Error registering: ' + error.response.data.message;
        } else {
          this.message = 'Unknown error';
        }
      }
    }
  }
};
</script>
